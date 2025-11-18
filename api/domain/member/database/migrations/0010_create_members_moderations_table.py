from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("user", "0001_create_users_table"),
        ("member", "0009_create_members_moderation_types_table"),
        ("feed", "0002_create_feed_posts_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="MemberModeration",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "admin_user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="admin_user_id",
                        related_name="moderations_administered",
                    ),
                ),
                (
                    "type_id",
                    models.ForeignKey(
                        to="member.MemberModerationType",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="type_id",
                    ),
                ),
                ("is_applied", models.BooleanField(default=False)),
                ("expires_at", models.DateTimeField()),
                ("is_on_member", models.BooleanField(default=False)),
                ("is_on_post", models.BooleanField(default=False)),
                (
                    "member_user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        null=True,
                        blank=True,
                        db_column="member_user_id",
                        related_name="moderations_targeting_member",
                    ),
                ),
                (
                    "member_feed_post_id",
                    models.ForeignKey(
                        to="feed.FeedPost",
                        on_delete=django.db.models.deletion.CASCADE,
                        null=True,
                        blank=True,
                        db_column="member_feed_post_id",
                        related_name="moderations_targeting_post",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "members_moderations",
            },
        ),
        migrations.AddIndex(
            model_name="membermoderation",
            index=models.Index(fields=["expires_at"], name="idx_members_moderations_expires_at"),
        ),
    ]
