from django.db import models
from api.domain.user.models.user import User
from api.domain.feed.models.feed_post import FeedPost

class FeedPostVote(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="post_votes")
    post_id = models.ForeignKey(FeedPost, on_delete=models.CASCADE, db_column="post_id", related_name="votes")
    up = models.BooleanField(default=False)
    down = models.BooleanField(default=False)
    refresh_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feed_posts_votes"
        indexes = [
            models.Index(fields=["created_at"]),
        ]
