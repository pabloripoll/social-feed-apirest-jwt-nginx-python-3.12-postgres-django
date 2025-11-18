from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("user", "0001_create_users_table"),
        ("geo", "0002_create_geo_regions_table"),
        ("feed", "0001_create_feed_categories_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedPost",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("uid", models.BigIntegerField(unique=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="user_id",
                    ),
                ),
                (
                    "region_id",
                    models.ForeignKey(
                        to="geo.GeoRegion",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="region_id",
                    ),
                ),
                (
                    "category_id",
                    models.ForeignKey(
                        to="feed.FeedCategory",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="category_id",
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("is_draft", models.BooleanField(default=False)),
                ("is_banned", models.BooleanField(default=False)),
                ("visits_count", models.IntegerField(default=0)),
                ("reports_count", models.IntegerField(default=0)),
                ("votes_up_count", models.IntegerField(default=0)),
                ("votes_down_count", models.IntegerField(default=0)),
                ("title", models.CharField(max_length=128, null=True, blank=True)),
                ("slug", models.CharField(max_length=128, null=True, blank=True)),
                ("summary", models.CharField(max_length=256, null=True, blank=True)),
                ("article", models.TextField(null=True, blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "feed_posts"},
        ),
    ]
