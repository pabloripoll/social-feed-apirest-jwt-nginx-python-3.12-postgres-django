from django.db import migrations


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("member", "0001_create_members_table"),
        ("member", "0002_create_members_profile_table"),
        ("member", "0003_create_members_access_logs_table"),
        ("member", "0004_create_members_following_table"),
        ("member", "0005_create_members_followers_table"),
        ("member", "0006_create_members_activation_codes_table"),
        ("member", "0007_create_members_notification_types_table"),
        ("member", "0008_create_members_notifications_table"),
        ("member", "0009_create_members_moderation_types_table"),
        ("member", "0010_create_members_moderations_table"),
    ]

    operations = []
