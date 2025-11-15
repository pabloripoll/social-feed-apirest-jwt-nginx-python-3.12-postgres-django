from django.db import models
from api.domain.user.model.user import User

class ModerationType(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    position = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members_moderation_types"