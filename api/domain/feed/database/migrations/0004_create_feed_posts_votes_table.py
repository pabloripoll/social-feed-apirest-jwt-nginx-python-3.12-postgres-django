from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("user", "0001_create_users_table"),
        ("feed", "0002_create_feed_posts_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedPostVote",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="user_id",
                    ),
                ),
                (
                    "post_id",
                    models.ForeignKey(
                        to="feed.FeedPost",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="post_id",
                    ),
                ),
                ("up", models.BooleanField(default=False)),
                ("down", models.BooleanField(default=False)),
                ("refresh_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "feed_posts_votes"},
        ),
    ]
