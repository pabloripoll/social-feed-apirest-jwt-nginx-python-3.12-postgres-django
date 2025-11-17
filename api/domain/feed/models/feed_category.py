from django.db import models

class FeedCategory(models.Model):
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
        db_table = "feed_categories"
