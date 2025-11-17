from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("geo", "0001_create_geo_continents_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="GeoRegion",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "continent_id",
                    models.ForeignKey(
                        to="geo.GeoContinent",
                        on_delete=django.db.models.deletion.CASCADE,
                        db_column="continent_id",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "geo_regions",
            },
        ),
    ]
