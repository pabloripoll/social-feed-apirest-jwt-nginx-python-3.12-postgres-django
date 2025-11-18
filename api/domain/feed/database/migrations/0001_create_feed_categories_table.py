from django.db import migrations, models


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        # no cross-app dependency for categories
    ]

    operations = [
        migrations.CreateModel(
            name="FeedCategory",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=64)),
                ("title", models.CharField(max_length=64)),
                ("visits_count", models.IntegerField(default=0)),
                ("feed_posts_count", models.IntegerField(default=0)),
                ("feed_posts_votes_up_count", models.IntegerField(default=0)),
                ("feed_posts_votes_down_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "feed_categories"},
        ),
        migrations.AddConstraint(
            model_name="feedcategory",
            constraint=models.UniqueConstraint(fields=("key",), name="uniq_feed_categories_key"),
        ),
    ]
