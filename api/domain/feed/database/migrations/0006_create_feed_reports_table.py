from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("feed", "0002_create_feed_posts_table"),
        ("feed", "0005_create_feed_report_types_table"),
        ("user", "0001_create_users_table"),
        ("member", "0010_create_members_moderations_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedReport",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "type_id",
                    models.ForeignKey(
                        to="feed.FeedReportType",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="type_id",
                    ),
                ),
                (
                    "reporter_user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="reporter_user_id",
                    ),
                ),
                ("reporter_message", models.CharField(max_length=256, null=True, blank=True)),
                ("in_review", models.BooleanField(default=False)),
                ("in_review_since", models.DateTimeField()),
                ("is_closed", models.BooleanField(default=False)),
                ("closed_at", models.DateTimeField()),
                (
                    "moderation_id",
                    models.ForeignKey(
                        to="member.MemberModeration",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="moderation_id",
                    ),
                ),
                (
                    "member_user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="member_user_id",
                        related_name="+",
                    ),
                ),
                (
                    "member_feed_post_id",
                    models.ForeignKey(
                        to="feed.FeedPost",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="member_feed_post_id",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "feed_reports"},
        ),
        migrations.AddIndex(
            model_name="feedreport",
            index=models.Index(fields=["created_at"], name="idx_feed_reports_created_at"),
        ),
    ]
