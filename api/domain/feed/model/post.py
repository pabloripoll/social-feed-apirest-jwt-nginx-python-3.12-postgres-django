from django.db import models
from apirest.api.domain.users.models import User
from apirest.api.domain.geo.models import Region

class PostCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=64)
    visits_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    posts_votes_up_count = models.IntegerField(default=0)
    posts_votes_down_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts_categories"

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="posts")
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.PROTECT, db_column="region_id", related_name="posts")
    # NOTE: schema had category_id -> users.id which looks like a typo.
    category = models.ForeignKey(PostCategory, on_delete=models.PROTECT, db_column="category_id", related_name="posts")
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
        db_table = "posts"
        indexes = [
            models.Index(fields=["uid"]),
            models.Index(fields=["created_at"]),
        ]

class PostVisit(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="post_visits")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column="post_id", related_name="visits")
    visitor_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, db_column="visitor_user_id", related_name="visits_as_visitor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts_visits"

class PostVote(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="post_votes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column="post_id", related_name="votes")
    up = models.BooleanField(default=False)
    down = models.BooleanField(default=False)
    refresh_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts_votes"
        indexes = [
            models.Index(fields=["created_at"]),
        ]

class PostReportType(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, null=True, blank=True)
    level = models.SmallIntegerField(default=0)
    position = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts_report_types"

class PostReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.ForeignKey(PostReportType, on_delete=models.PROTECT, db_column="type_id", related_name="reports")
    reporter_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, db_column="reporter_user_id", related_name="reports_made")
    reporter_message = models.CharField(max_length=256, null=True, blank=True)
    in_review = models.BooleanField(default=False)
    in_review_since = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    moderation = models.ForeignKey("apirest.api.domain.member.models.MemberModeration", null=True, blank=True, on_delete=models.SET_NULL, db_column="moderation_id", related_name="reports")
    member_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="member_user_id", related_name="reports_received")
    member_post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL, db_column="member_post_id", related_name="reports_on_post")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts_reports"
        indexes = [
            models.Index(fields=["created_at"]),
        ]
