from django.db import models
from api.domain.user.models.user import User
from api.domain.geo.models.geo_region import GeoRegion
from api.domain.feed.models.feed_category import FeedCategory

class FeedPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField(unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="posts")
    region_id = models.ForeignKey(GeoRegion, null=True, blank=True, on_delete=models.PROTECT, db_column="region_id", related_name="posts")
    category_id = models.ForeignKey(FeedCategory, on_delete=models.PROTECT, db_column="feed_category_id", related_name="posts")
    is_active = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    visits_count = models.IntegerField(default=0)
    reports_count = models.IntegerField(default=0)
    votes_up_count = models.IntegerField(default=0)
    votes_down_count = models.IntegerField(default=0)
    title = models.CharField(max_length=128, null=True, blank=True)
    slug = models.CharField(max_length=128, null=True, blank=True)
    summary = models.CharField(max_length=256, null=True, blank=True)
    article = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feed_posts"
        indexes = [
            models.Index(fields=["uid"]),
            models.Index(fields=["created_at"]),
        ]
