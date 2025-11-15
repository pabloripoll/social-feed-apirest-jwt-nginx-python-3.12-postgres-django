from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore
from .feature.shared import CheckController
from .domain.member.controller.mamber_auth_controller import *

# /api/v1/ routes
urlpatterns = [
    # check installation endpoints
    path("", CheckController.CheckV1View.as_view(), name="check-v1"),
    path("check/database", CheckController.CheckDatabaseView.as_view(), name="check-database"),
    path("check/send-mail", CheckController.CheckSendMailView.as_view(), name="check-send-mail"),

    # Member auth endpoints (api/v1/auth/)
    path("auth/register", MemberRegisterView(), name="auth-register"),
    path("auth/login", MemberLoginView(), name="auth-login"),
    path("auth/activation-code", MemberActivationCodeView(), name="auth-activation-code"),
    path("auth/refresh", MemberRefreshTokenView(), name="auth-refresh-token"),
    path("auth/logout", MemberLogoutView(), name="auth-logout"),
    path("auth/whoami", MemberWhoAmIView(), name="auth-whoami"),

]
