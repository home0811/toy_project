from django.shortcuts import render,  redirect
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.views import APIView
from .models import Map, Point
from .serializers import MapSerializer
from collections import OrderedDict


def main_introduction(req):
    """
        '' url 소개 페이지
    """
    return render(req, 'main_introduction.html')

def kakaomaps(req):
    """
        kakaomaps toy page
    """
    map = Map.objects.all().order_by("id")
    mapSerializer = MapSerializer(map, many=True).data

    for i in range(len(mapSerializer)):
        mapSerializer[i] = dict(mapSerializer[i])
        if mapSerializer[i]["type"] == "polyline":
            del mapSerializer[i]["fillColor"]
            del mapSerializer[i]["fillOpacity"]

    context = { "map": mapSerializer }
    return render(req, 'kakaomap.html', context)

class StorageView(APIView):
    def post(self, req):
        """
            카카오맵 데이터 저장
        """        
        try:
            data = req.data
            name = req.GET.get("name")
            map = Map.objects.create(name=name)
            point_arr = []
            for i in data:
                data_arr = i.replace('data[', '').replace('][', ',').replace(']','').split(',')
                if len(data_arr) == 3:
                    # data_arr[3] == "type"
                    setattr(map, data_arr[2], data[i])
                elif len(data_arr) == 4:
                    # data_arr[3] == "coordinate"
                    setattr(map, data_arr[3], data[i])
                else:
                    # data_arr[3] == sequence number
                    if len(point_arr) <= int(data_arr[3]) : point_arr.append([])
                    point_arr[int(data_arr[3])].append(data[i])  
            map.save()
            
            sequence = 0
            for point in point_arr:
                point = Point.objects.create(map_id=map, sequence=sequence, x=point[0], y=point[1])
                point.save()
                sequence += 1
                        
        except Exception as e:
            print(e)
        
        return HttpResponse(status=201)

    
    def put(self,req):
        data = req.data
        id = req.GET.get("id")
        name = req.GET.get("name")

        try:
            map = Map.objects.get(id=id)
            setattr(map, 'name', name)
            
            points = Point.objects.filter(map_id=map)
            print(points)
            for point in points:
                point.delete()

            point_arr = []
            for i in data:
                data_arr = i.replace('data[', '').replace('][', ',').replace(']','').split(',')
                if len(data_arr) == 5:
                    # data_arr[3] == sequence number
                    if len(point_arr) <= int(data_arr[3]) : point_arr.append([])
                    point_arr[int(data_arr[3])].append(data[i])  
                    
            map.save()
            
            sequence = 0
            for point in point_arr:
                point = Point.objects.create(map_id=map, sequence=sequence, x=point[0], y=point[1])
                point.save()
                sequence += 1

        except Exception as e:
            print(e)

        return HttpResponse("")

    def delete(self, req):
        """
            카카오맵 데이터 삭제
        """        
        id = req.GET.get("id")
        try:
            map = Map.objects.get(id=id)
            map.delete()
        except Exception as e:
            print(e)

        return redirect('kakaomap')