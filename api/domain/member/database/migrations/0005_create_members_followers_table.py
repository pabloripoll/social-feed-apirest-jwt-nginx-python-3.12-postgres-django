from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("user", "0001_create_users_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="MemberFollower",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers_owner",
                        db_column="user_id",
                    ),
                ),
                (
                    "follower_user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers_source",
                        db_column="follower_user_id",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "members_followers",
            },
        ),
    ]
