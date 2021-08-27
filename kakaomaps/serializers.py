from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Map, Point


class MapSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    strokeWeight = serializers.SerializerMethodField()
    strokeOpacity = serializers.SerializerMethodField()
    fillOpacity = serializers.SerializerMethodField()

    class Meta:
        model = Map
        fields = "__all__"

    def get_points(self, obj):
        point = Point.objects.filter(map_id=obj).order_by('sequence')
        point_arr = [[0] * 2 for _ in range(len(point))]

        for p in point:
            point_arr[int(p.sequence)][0] = p.x
            point_arr[int(p.sequence)][1] = p.y

        return point_arr

    def get_strokeWeight(self, obj):
        return int(obj.strokeWeight)

    def get_strokeOpacity(self, obj):
        return float(obj.strokeOpacity)

    def get_fillOpacity(self, obj):
        if obj.type == "polygon":
            return float(obj.fillOpacity)
        else:
            return obj.fillOpacity