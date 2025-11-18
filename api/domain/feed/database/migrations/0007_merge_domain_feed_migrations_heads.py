from django.db import migrations


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("feed", "0001_create_feed_categories_table"),
        ("feed", "0002_create_feed_posts_table"),
        ("feed", "0003_create_feed_posts_visits_table"),
        ("feed", "0004_create_feed_posts_votes_table"),
        ("feed", "0005_create_feed_report_types_table"),
        ("feed", "0006_create_feed_reports_table"),
    ]

    operations = []
