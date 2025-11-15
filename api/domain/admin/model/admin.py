from django.db import models
from apirest.api.domain.users.models import User
from apirest.api.domain.geo.models import Region

class Admin(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="admin_records")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, db_column="region_id", related_name="admins")
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "admins"

class AdminProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column="user_id", related_name="admin_profile")
    nickname = models.CharField(max_length=255, unique=True)
    avatar = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "admins_profile"

class AdminAccessLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="admin_access_logs")
    is_terminated = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    expires_at = models.DateTimeField(db_index=True)
    refresh_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    requests_count = models.IntegerField(default=0)
    payload = models.JSONField(null=True, blank=True)
    token = models.TextField(db_index=True)

    class Meta:
        db_table = "admins_access_logs"
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["created_at"]),
        ]
