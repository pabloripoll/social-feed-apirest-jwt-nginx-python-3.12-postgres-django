from django.db import models
from api.domain.user.models.user import User
from api.domain.member.models.member_moderation import MemberModeration
from .feed_post import FeedPost
from .feed_report_type import FeedReportType

class FeedReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.ForeignKey(FeedReportType, on_delete=models.PROTECT, db_column="type_id", related_name="reports")
    reporter_user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, db_column="reporter_user_id", related_name="reports_made")
    reporter_message = models.CharField(max_length=512, null=True, blank=True)
    in_review = models.BooleanField(default=False)
    in_review_since = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    moderation_id = models.ForeignKey(MemberModeration, null=True, blank=True, on_delete=models.SET_NULL, db_column="moderation_id", related_name="reports")
    member_user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="member_user_id", related_name="reports_received")
    member_feed_post_id = models.ForeignKey(FeedPost, null=True, blank=True, on_delete=models.SET_NULL, db_column="member_feed_post_id", related_name="reports_on_post")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feed_reports"
        indexes = [
            models.Index(fields=["created_at"]),
        ]
