from django.db import models
from api.domain.user.models import User
from api.domain.geo.models import GeoRegion

class Admin(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="admin_records")
    region = models.ForeignKey(GeoRegion, on_delete=models.PROTECT, db_column="region_id", related_name="admins")
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "admins"
