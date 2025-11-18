from django.db import migrations


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("user", "0001_create_users_table"),
        ("user", "0002_create_user_password_reset_tokens_table"),
    ]

    operations = []
