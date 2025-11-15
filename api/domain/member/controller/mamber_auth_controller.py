from django.db import transaction, IntegrityError
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from api.domain.user.model.user import User
from api.domain.geo.model.geo_region import GeoRegion
from api.domain.member.model.member import Member
from api.domain.member.model.member_activation_code import MemberActivationCode
from api.domain.member.model.member_profile import MemberProfile
from api.domain.member.model.member_access_log import MemberAccessLog

from api.domain.member.request.member_register_request import MemberRegisterRequest
from api.domain.member.request.member_activation_code_request import MemberActivationCodeRequest
from api.domain.member.request.member_login_request import MemberLoginRequest
from api.domain.member.request.member_refresh_token_request import MemberRefreshTokenRequest
from api.domain.member.request.member_logout_request import MemberLogoutRequest


class MemberRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = MemberRegisterRequest(data=request.data)
        if not serializer.is_valid():
            # return first error
            field = next(iter(serializer.errors))

            return Response({"message": serializer.errors[field][0], "error": field}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = serializer.validated_data

        try:
            with transaction.atomic():
                # create user
                user = User.objects.create(
                    role=getattr(request, "ROLE_MEMBER_KEY", "member"),
                    email=data["email"].lower(),
                    password=make_password(data["password"]),
                )

                # create member
                # Note: your FK field is named `user_id` on Member, so we pass the instance to that kwarg.
                # If you rename the field to `user`, prefer user=user instead.
                region = data.get("region_id", None)
                member = Member.objects.create(
                    user_id=user,   # pass instance because field is user_id
                    region_id=(region if isinstance(region, GeoRegion) else region),
                    # do NOT set uid here if Member.save() auto-generates it
                )

                # create activation code using model helper (ensures uniqueness and atomicity)
                activation = MemberActivationCode.create_for_user(user)

                # create profile
                profile = MemberProfile.objects.create(
                    user_id=user,
                    nickname=data["nickname"],
                )

            # payload response
            payload = {
                "uid": member.uid,
                "email": user.email,
                "nickname": profile.nickname,
                "activation_code": activation.code,
            }

            # Optional: send email via configured mail / queue; placeholder only
            if getattr(settings, "MAIL_SEND", False):
                # If you have a background job / queue configured you can push payload to it here.
                # Keep this as a placeholder; do not assume presence of Laravel mail helpers.
                pass

            return Response(payload, status=status.HTTP_201_CREATED)

        except IntegrityError as exc:
            # unique constraint violation or other DB error
            return Response({"message": "Database error creating account.", "detail": str(exc)},
                            status=status.HTTP_409_CONFLICT)


class MemberActivationCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = MemberActivationCodeRequest(data=request.data)
        if not serializer.is_valid():
            field = next(iter(serializer.errors))
            return Response({"message": serializer.errors[field][0], "error": field}, status=status.HTTP_406_NOT_ACCEPTABLE)

        email = serializer.validated_data["email"].lower()
        code = serializer.validated_data["code"]

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        activation = MemberActivationCode.objects.filter(user=user, code=code).first()
        if not activation:
            return Response({"message": "Activation code not found."}, status=status.HTTP_404_NOT_FOUND)

        activation.is_active = True
        activation.save()

        return Response({"email": user.email, "status": "Account activation has been activated."}, status=status.HTTP_202_ACCEPTED)


class MemberLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    # jwt_time in minutes (smaller/alternate expiration time)
    jwt_time = getattr(settings, "JWT_TIME_MINUTES", 60)

    def post(self, request):
        serializer = MemberLoginRequest(data=request.data)
        if not serializer.is_valid():
            field = next(iter(serializer.errors))
            return Response({"message": serializer.errors[field][0], "error": field}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = serializer.validated_data
        email = data["email"].lower()
        raw_password = data["password"]

        # Find user with the MEMBER role (adjust role key if you keep a Role model)
        user = User.objects.filter(email=email, role=getattr(settings, "ROLE_MEMBER_KEY", "member")).first()
        if not user:
            return Response({"message": "Invalid credentials."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not check_password(raw_password, user.password):
            return Response({"message": "Invalid credentials."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Check activation if configured
        if bool(getattr(settings, "LOGIN_ACTIVATION_CODE", False)):
            member_activation = MemberActivationCode.objects.filter(user=user, is_active=True).first()
            if not member_activation:
                return Response({"message": "Access requires activation."}, status=status.HTTP_401_UNAUTHORIZED)

        # Create JWT tokens (refresh + access)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # create an access log record (store refresh token so you can rotate/blacklist later)
        expires_at = timezone.now() + timedelta(minutes=self.jwt_time)
        MemberAccessLog.objects.create(
            user=user,
            token=refresh_token,
            expires_at=expires_at,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            requests_count=1,
            payload={},
        )

        # Calculate expires_in (seconds) based on SIMPLE_JWT ACCESS_TOKEN_LIFETIME if available
        access_lifetime = getattr(settings, "SIMPLE_JWT", {}).get("ACCESS_TOKEN_LIFETIME", None)
        if access_lifetime is not None:
            try:
                expires_in = int(access_lifetime.total_seconds())
            except Exception:
                expires_in = self.jwt_time * 60
        else:
            expires_in = self.jwt_time * 60

        return Response({"token": access_token, "refresh": refresh_token, "expires_in": expires_in}, status=status.HTTP_200_OK)


class MemberRefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    jwt_time = getattr(settings, "JWT_TIME_MINUTES", 60)

    def post(self, request):
        serializer = MemberRefreshTokenRequest(data=request.data)
        if not serializer.is_valid():
            field = next(iter(serializer.errors))
            return Response({"message": serializer.errors[field][0], "error": field}, status=status.HTTP_406_NOT_ACCEPTABLE)

        refresh_token = serializer.validated_data["refresh"]

        try:
            refresh = RefreshToken(refresh_token)
        except Exception:
            return Response({"message": "Token invalid or expired.", "error": "token_invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        # Rotate / create a new access token
        new_access = str(refresh.access_token)

        # Update access log: find the access log by the stored refresh token
        access_log = MemberAccessLog.objects.filter(token=refresh_token, is_terminated=False).first()
        if access_log:
            access_log.expires_at = timezone.now() + timedelta(minutes=self.jwt_time)
            access_log.refresh_count = (access_log.refresh_count or 0) + 1
            # store the same refresh token string (or optionally rotate store to new refresh)
            access_log.token = refresh_token
            access_log.save()
        else:
            # optional: create a new access log if none exists
            MemberAccessLog.objects.create(
                user_id=getattr(refresh, "user_id", None),
                token=refresh_token,
                expires_at=timezone.now() + timedelta(minutes=self.jwt_time),
                requests_count=0,
                payload={},
            )

        access_lifetime = getattr(settings, "SIMPLE_JWT", {}).get("ACCESS_TOKEN_LIFETIME", None)
        if access_lifetime is not None:
            try:
                expires_in = int(access_lifetime.total_seconds())
            except Exception:
                expires_in = self.jwt_time * 60
        else:
            expires_in = self.jwt_time * 60

        return Response({"token": new_access, "expires_in": expires_in, "token_expired": None}, status=status.HTTP_202_ACCEPTED)


class MemberLogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = MemberLogoutRequest(data=request.data)
        if not serializer.is_valid():
            field = next(iter(serializer.errors))
            return Response({"message": serializer.errors[field][0], "error": field}, status=status.HTTP_406_NOT_ACCEPTABLE)

        refresh_token = serializer.validated_data["refresh"]

        # Blacklist the refresh token if token blacklisting is enabled
        try:
            token = RefreshToken(refresh_token)
            # blacklist (requires rest_framework_simplejwt.token_blacklist app installed)
            try:
                token.blacklist()
            except AttributeError:
                # token.blacklist may not exist if blacklist app isn't enabled
                pass
        except Exception:
            # Token invalid -> still proceed to mark server-side access log if present
            pass

        access_log = MemberAccessLog.objects.filter(token=refresh_token, is_terminated=False).first()
        if access_log:
            access_log.is_terminated = True
            access_log.save()

        return Response({"token_expired": refresh_token}, status=status.HTTP_202_ACCEPTED)


class MemberWhoAmIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Attempt to get the related Member (first one)
        member = getattr(user, "members", None)
        uid = None
        if member is not None:
            try:
                first_member = user.members.first()
                if first_member:
                    uid = first_member.uid
            except Exception:
                uid = None

        # Attempt to get profile (if related_name 'member_profile' used)
        nickname = None
        avatar = None
        try:
            profile = getattr(user, "member_profile", None)
            if profile:
                nickname = profile.nickname
                avatar = profile.avatar
        except Exception:
            nickname = None
            avatar = None

        # Find current access log by Authorization header (Bearer <refresh> or <access>)
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        token_str = None
        if auth_header.startswith("Bearer "):
            token_str = auth_header.split(" ", 1)[1].strip()

        access = None
        if token_str:
            access = MemberAccessLog.objects.filter(token=token_str, is_terminated=False).first()

        if not access:
            # If token not found/invalid, return 401 similar to Laravel
            return Response({"message": "Token invalid or expired.", "error": "token_invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "email": user.email,
            "uid": uid,
            "nickname": nickname,
            "avatar": avatar,
            "token": access.token,
        }, status=status.HTTP_200_OK)
