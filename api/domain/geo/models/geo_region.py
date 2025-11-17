from django.db import models
from .geo_continent import GeoContinent

class GeoRegion(models.Model):
    id = models.BigAutoField(primary_key=True)
    continent = models.ForeignKey(GeoContinent, on_delete=models.PROTECT, db_column="continent_id", related_name="regions")
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "geo_regions"
        indexes = [
            models.Index(fields=["continent"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.continent})"