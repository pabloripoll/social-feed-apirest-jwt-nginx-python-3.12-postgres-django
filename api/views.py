from django.contrib.auth import get_user_model
from django.db import connection
from django.utils import timezone
from django.core.mail import send_mail

# pyright: reportMissingImports=false
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

class APIRootView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            "message": "API root",
            "auth": {
                "public": "/api/v1/auth/",
                "admin": "/api/v1/admin/auth/",
            },
        })

# Public registration/login/logout/refresh/whoami
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Expects: { "refresh": "<refresh_token>" }
        Blacklists the refresh token.
        """
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as exc:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

# Account/Profile endpoints for members (authenticated non-admin)
class MemberAccountView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class MemberProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profile = getattr(request.user, "profile", None)
        if profile is None:
            return Response({"profile": None})
        return Response({"bio": profile.bio})

# Admin account/profile endpoints (IsAdminUser)
class AdminAccountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class AdminProfileView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        profile = getattr(request.user, "profile", None)
        if profile is None:
            return Response({"profile": None})
        return Response({"bio": profile.bio})

# Admin register/login that only issues tokens for staff users
class AdminRegisterView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(
            username=data["username"],
            email=data.get("email", ""),
            password=data["password"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            is_staff=True,
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # ensure user is staff before issuing admin token
        if not self.user.is_staff:
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed("Admin credentials required")
        return data

class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

# Admin whoami — require IsAdminUser
class AdminWhoAmIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return Response(UserSerializer(request.user).data)
