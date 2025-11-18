from django.db import migrations


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("admin", "0001_create_admins_table"),
        ("admin", "0002_create_admins_profile_table"),
        ("admin", "0003_create_admins_access_logs_table"),
    ]

    operations = []
