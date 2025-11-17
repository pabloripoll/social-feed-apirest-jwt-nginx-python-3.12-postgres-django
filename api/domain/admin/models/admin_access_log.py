from django.db import models
from api.domain.user.models import User

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
