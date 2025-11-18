from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("user", "0001_create_users_table"),
        ("geo", "0002_create_geo_regions_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="Member",
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
                ("is_active", models.BooleanField(default=False)),
                ("is_banned", models.BooleanField(default=False)),
                ("following_count", models.IntegerField(default=0)),
                ("followers_count", models.IntegerField(default=0)),
                ("feed_posts_count", models.IntegerField(default=0)),
                ("feed_gain_votes_up_count", models.IntegerField(default=0)),
                ("feed_gain_votes_down_count", models.IntegerField(default=0)),
                ("feed_send_votes_up_count", models.IntegerField(default=0)),
                ("feed_send_votes_down_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "members",
            },
        ),
    ]
