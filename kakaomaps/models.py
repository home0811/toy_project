from django.db import models

# Create your models here.
class Map(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=100, null=False, default="polyline")
    coordinate = models.CharField(max_length=100, null=False, default="wgs84")
    strokeColor = models.CharField(max_length=100, null=True)
    strokeStyle = models.CharField(max_length=100, null=True)
    strokeWeight = models.CharField(max_length=100, null=True)
    strokeOpacity = models.CharField(max_length=100, null=True)
    fillColor = models.CharField(max_length=100, null=True)
    fillOpacity = models.CharField(max_length=100, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Point(models.Model):
    id = models.AutoField(primary_key=True)
    map_id = models.ForeignKey("Map", related_name="map", on_delete=models.CASCADE, db_column="map_id")
    sequence = models.IntegerField(null=False)
    x = models.FloatField(null=False)
    y = models.FloatField(null=False)
