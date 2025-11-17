from django.db import models
from api.domain.user.models import User

class AdminProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column="user_id", related_name="admin_profile")
    nickname = models.CharField(max_length=255, unique=True)
    avatar = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "admins_profile"
