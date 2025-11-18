from django.db import migrations, models


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        # no cross-app dependencies required for report types
    ]

    operations = [
        migrations.CreateModel(
            name="FeedReportType",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=64)),
                ("title", models.CharField(max_length=64)),
                ("description", models.CharField(max_length=256, null=True, blank=True)),
                ("level", models.SmallIntegerField(default=0)),
                ("position", models.SmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "feed_report_types"},
        ),
    ]
