from django.db import migrations, models


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        # no cross-app dependencies required for report types
    ]

    operations = [
        migrations.CreateModel(
            name="MemberModerationType",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=64)),
                ("title", models.CharField(max_length=64)),
                ("description", models.CharField(max_length=256)),
                ("position", models.SmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "members_moderation_types",
            },
        ),
        migrations.AddConstraint(
            model_name="membermoderationtype",
            constraint=models.UniqueConstraint(fields=("key",), name="uniq_members_moderation_types_key"),
        ),
    ]
