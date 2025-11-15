from django.db import migrations

SQL = """
-- paste your CREATE TABLE statements here (the SQL you already have)
"""

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(SQL)
    ]
