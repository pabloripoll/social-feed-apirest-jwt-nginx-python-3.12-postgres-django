from django.db import models
from api.domain.user.models.user import User

class MemberFollowing(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="following")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="following_user_id", related_name="followed_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members_following"
        indexes = [
            models.Index(fields=["user", "following_user"]),
        ]

