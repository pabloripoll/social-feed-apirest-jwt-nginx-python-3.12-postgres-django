from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore
from . import views
from .feature import testController

urlpatterns = [
    # API root and versioning
    path("", views.APIRootView.as_view(), name="api-root"),

    # Public auth endpoints (api/v1/auth/)
    path("auth/register", views.RegisterView.as_view(), name="auth-register"),
    path("auth/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout", views.LogoutView.as_view(), name="auth-logout"),
    path("auth/whoami", views.WhoAmIView.as_view(), name="auth-whoami"),

    # Member account/profile
    path("account", views.MemberAccountView.as_view(), name="member-account"),
    path("account/profile", views.MemberProfileView.as_view(), name="member-profile"),

    # Admin auth (admin-only login/register; login will only issue tokens for staff users)
    path("admin/auth/login", views.AdminTokenObtainPairView.as_view(), name="admin-token-obtain"),
    path("admin/auth/refresh", TokenRefreshView.as_view(), name="admin-token-refresh"),
    path("admin/auth/logout", views.LogoutView.as_view(), name="admin-logout"),
    path("admin/auth/register", views.AdminRegisterView.as_view(), name="admin-register"),
    path("admin/auth/whoami", views.AdminWhoAmIView.as_view(), name="admin-whoami"),

    # Admin endpoints (api/v1/admin/)
    path("admin/account", views.AdminAccountView.as_view(), name="admin-account"),
    path("admin/account/profile", views.AdminProfileView.as_view(), name="admin-profile"),

    # test endpoints
    path("test/database", testController.TestDatabaseView.as_view(), name="test-database"),
    path("test/send-mail", testController.SendMailTestView.as_view(), name="test-send-mail"),
]
