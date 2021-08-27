from django.contrib import admin
from .models import Map, Point

# Register your models here.
class MapAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'type',
        'coordinate',
        'strokeColor',
        'strokeStyle',
        'strokeWeight',
        'strokeOpacity',
        'fillColor',
        'fillOpacity',
    ]


class PointAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'map_id',
        'sequence',
        'x',
        'y',
    ]


admin.site.register(Map, MapAdmin)
admin.site.register(Point, PointAdmin)