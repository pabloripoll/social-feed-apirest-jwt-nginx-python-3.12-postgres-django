from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("member", "0007_create_members_notification_types_table"),
        ("user", "0001_create_users_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="MemberNotification",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "notification_type_id",
                    models.ForeignKey(
                        to="member.MemberNotificationType",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="notification_type_id",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="user_id",
                    ),
                ),
                ("is_opened", models.BooleanField(default=False)),
                ("opened_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("message", models.CharField(max_length=512)),
                (
                    "last_member_user_id",
                    models.ForeignKey(
                        to="user.User",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="last_member_user_id",
                        related_name="+",
                    ),
                ),
                ("last_member_nickname", models.CharField(max_length=32)),
                ("last_member_avatar", models.TextField(null=True, blank=True)),
            ],
            options={
                "db_table": "members_notifications",
            },
        ),
        migrations.AddIndex(
            model_name="membernotification",
            index=models.Index(fields=["opened_at"], name="idx_members_notifications_opened_at"),
        ),
        migrations.AddIndex(
            model_name="membernotification",
            index=models.Index(fields=["created_at"], name="idx_members_notifications_created_at"),
        ),
    ]
