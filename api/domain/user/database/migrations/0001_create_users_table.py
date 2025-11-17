from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("role", models.CharField(max_length=16)),
                ("email", models.CharField(max_length=64, unique=True)),
                ("email_verified_at", models.DateTimeField(null=True, blank=True, default=None)),
                ("password", models.CharField(max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "users",
            },
        ),
    ]
