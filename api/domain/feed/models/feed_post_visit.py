from django.db import models
from api.domain.user.models.user import User
from api.domain.feed.models.feed_post import FeedPost

class FeedPostVisit(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="post_visits")
    post_id = models.ForeignKey(FeedPost, on_delete=models.CASCADE, db_column="post_id", related_name="visits")
    visitor_user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, db_column="visitor_user_id", related_name="visits_as_visitor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feed_posts_visits"
