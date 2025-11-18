from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user", "0001_create_users_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserPasswordResetToken",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_token_active", models.BooleanField(default=False)),
                ("token", models.TextField()),
            ],
            options={
                "db_table": "user_password_reset_tokens",
            },
        ),
    ]
