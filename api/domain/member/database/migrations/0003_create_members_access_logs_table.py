from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("user", "0001_create_users_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="MemberAccessLog",
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
                ("is_terminated", models.BooleanField(default=False)),
                ("is_expired", models.BooleanField(default=False)),
                ("expires_at", models.DateTimeField()),
                ("refresh_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("ip_address", models.CharField(max_length=45, null=True, blank=True)),
                ("user_agent", models.TextField(null=True, blank=True)),
                ("requests_count", models.IntegerField(default=0)),
                ("payload", models.JSONField(null=True, blank=True)),
                ("token", models.TextField()),
            ],
            options={
                "db_table": "members_access_logs",
            },
        ),
        migrations.AddIndex(
            model_name="memberaccesslog",
            index=models.Index(fields=["expires_at"], name="idx_members_access_logs_expires_at"),
        ),
        migrations.AddIndex(
            model_name="memberaccesslog",
            index=models.Index(fields=["token"], name="idx_members_access_logs_token"),
        ),
    ]
