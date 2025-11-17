# Member moderation model (separate file because PostReport referenced it earlier)
from django.db import models
from api.domain.user.models.user import User
from api.domain.feed.models.feed_post import FeedPost
from api.domain.member.models.member_moderation_type import MemberModerationType

class MemberModeration(models.Model):
    id = models.BigAutoField(primary_key=True)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="admin_user_id", related_name="moderations")
    # NOTE: original schema had type_id referencing members_notification_types — likely a typo.
    # If you have a separate moderation types table, change this FK accordingly.
    type_id = models.ForeignKey(MemberModerationType, on_delete=models.PROTECT, db_column="type_id", related_name="moderations")
    is_applied = models.BooleanField(default=False)
    expires_at = models.DateTimeField(db_index=True, null=True, blank=True)
    is_on_member = models.BooleanField(default=False)
    is_on_feed_post = models.BooleanField(default=False)
    member_user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="member_user_id", related_name="moderations_on_member")
    member_feed_post_id = models.ForeignKey(FeedPost, null=True, blank=True, on_delete=models.SET_NULL, db_column="member_feed_post_id", related_name="moderations_on_post")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members_moderations"
        indexes = [
            models.Index(fields=["expires_at"]),
        ]
