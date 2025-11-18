from django.db import migrations, models


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        # no cross-app dependencies required for report types
    ]

    operations = [
        migrations.CreateModel(
            name="MemberNotificationType",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=64)),
                ("title", models.CharField(max_length=64)),
                ("message_singular", models.CharField(max_length=512)),
                ("message_multiple", models.CharField(max_length=512)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "members_notification_types",
            },
        ),
        migrations.AddConstraint(
            model_name="membernotificationtype",
            constraint=models.UniqueConstraint(fields=("key",), name="uniq_members_notification_types_key"),
        ),
    ]
