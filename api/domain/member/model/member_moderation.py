# Member moderation model (separate file because PostReport referenced it earlier)
from django.db import models
from api.domain.user.model.user import User
from api.domain.feed.model.post import Post

class MemberModeration(models.Model):
    id = models.BigAutoField(primary_key=True)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="admin_user_id", related_name="moderations")
    # NOTE: original schema had type_id referencing members_notification_types — likely a typo.
    # If you have a separate moderation types table, change this FK accordingly.
    type = models.ForeignKey("apirest.api.domain.member.models.ModerationType", on_delete=models.PROTECT, db_column="type_id", related_name="moderations")
    is_applied = models.BooleanField(default=False)
    expires_at = models.DateTimeField(db_index=True, null=True, blank=True)
    is_on_member = models.BooleanField(default=False)
    is_on_post = models.BooleanField(default=False)
    member_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="member_user_id", related_name="moderations_on_member")
    member_post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL, db_column="member_post_id", related_name="moderations_on_post")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members_moderations"
        indexes = [
            models.Index(fields=["expires_at"]),
        ]
