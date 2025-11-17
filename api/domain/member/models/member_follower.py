from django.db import models
from api.domain.user.models.user import User

class MemberFollower(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="followers"
    )
    follower_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="follower_user_id",
        related_name="following_of"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members_followers"
        indexes = [
            models.Index(fields=["user", "follower_user"]),
        ]
