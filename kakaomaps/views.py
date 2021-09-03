from django.shortcuts import render,  redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Map, Point
from .serializers import MapSerializer

def main_introduction(req):
    """
        '' url 소개 페이지
    """
    return render(req, 'main_introduction.html')

def kakaomaps(req):
    """
        kakaomaps page
    """
    return render(req, 'kakaomap.html')

class CrudMapView(APIView):
    def get(self, req):
        page = int(req.GET.get("page"))
        count = int(req.GET.get("count"))
        map = Map.objects.all().order_by('id')[(page-1)*count:page*count]
        total = Map.objects.count()
        total_page = int(total/count)
        if total % count > 0 : total_page += 1
        if total_page < page : page = total_page

        serializers = MapSerializer(map, many=True).data
        for i in range(len(serializers)):
            serializers[i] = dict(serializers[i])
            if serializers[i]["type"] == "polyline":
                del serializers[i]["fillColor"]
                del serializers[i]["fillOpacity"]

        data = {"map":serializers, "total":total_page}
        return Response(data=data)

    def post(self, req):
        """
            kakaomap data create
        """        
        try:
            datas = req.data
            name = req.GET.get("name")
            map = Map.objects.create(name=name)

            for key in datas:
                field = get_field(key)
                if field : setattr(map, field, datas[key])
            map.save()
            
            for key in datas:
                sequence_xy = get_sequence_xy(key)
                if sequence_xy : 
                    if sequence_xy["xy"] == "x" :
                        point = Point.objects.create(map_id=map, sequence=sequence_xy["sequence"], x=datas[key])
                        point.save()
                    else:
                        point = Point.objects.filter(map_id=map).get(sequence=sequence_xy["sequence"])
                        setattr(point, sequence_xy["xy"], datas[key])
                        point.save()
                
        except Exception as e:
            print(e)
        
        return HttpResponse(status=201)

    
    def put(self,req):
        """
            kakaomap data update
        """
        datas = req.data
        id = req.GET.get("id")
        name = req.GET.get("name")

        try:
            map = Map.objects.get(id=id)
            setattr(map, 'name', name)
            map.save()
            
            points = Point.objects.filter(map_id=map)
            for point in points:
                point.delete()

            for key in datas:
                sequence_xy = get_sequence_xy(key)
                if sequence_xy : 
                    if sequence_xy["xy"] == "x" :
                        point = Point.objects.create(map_id=map, sequence=sequence_xy["sequence"], x=datas[key])
                        point.save()
                    else:
                        point = Point.objects.filter(map_id=map).get(sequence=sequence_xy["sequence"])
                        setattr(point, sequence_xy["xy"], datas[key])
                        point.save()
        except Exception as e:
            print(e)

        return HttpResponse("")

    def delete(self, req):
        """
            kakaomap data delete
        """        
        id = req.GET.get("id")
        try:
            map = Map.objects.get(id=id)
            map.delete()
        except Exception as e:
            print(e)

        return redirect('kakaomap')


# res -> polygon, 0, points
def divide_data(data : str):
    """
        - input data
            ex)
            'data[polygon][0][type]',
            'data[polygon][0][points][0][x]', 
            'data[polygon][0][points][0][y]',
            'data[polygon][0][options][strokeColor]', 
        - output
            ex)
            res -> polygon,0,type
    """
    arr = data.replace('data[', '').replace('][', ',').replace(']','').split(',')
    return arr



def get_field(keys : str):
    """
        - input data 
            ex)
            'data[polygon][0][type]': ['polygon'], 
            'data[polygon][0][points][0][x]': ['126.5684017969731'], 
            'data[polygon][0][points][0][y]': ['33.45302806477297'], 
            'data[polygon][0][points][1][x]': ['126.5720582386904'], 
            'data[polygon][0][points][1][y]': ['33.45313089868531'], 
            'data[polygon][0][points][2][x]': ['126.56680169026187'], 
            'data[polygon][0][points][2][y]': ['33.45036276092556'], 
            'data[polygon][0][points][3][x]': ['126.57096169322682'], 
            'data[polygon][0][points][3][y]': ['33.45083704161905'], 
            'data[polygon][0][coordinate]': ['wgs84'], 
            'data[polygon][0][options][strokeColor]': ['#39f'], 
            'data[polygon][0][options][strokeWeight]': ['3'], 
            'data[polygon][0][options][strokeStyle]': ['solid'], 
            'data[polygon][0][options][strokeOpacity]': ['1'], 
            'data[polygon][0][options][fillColor]': ['#39f'], 
            'data[polygon][0][options][fillOpacity]': ['0.5']
        - output data
            key
    """
    arr_key = divide_data(keys)
    type = arr_key[2]
    if type == "type" or type == "coordinate" : return type
    elif type == "options": return arr_key[3]
    return False

def get_sequence_xy(keys : str):
    """
        - input data 
            ex)
            'data[polygon][0][type]': ['polygon'], 
            'data[polygon][0][points][0][x]': ['126.5684017969731'], 
            'data[polygon][0][points][0][y]': ['33.45302806477297'], 
            'data[polygon][0][points][1][x]': ['126.5720582386904'], 
            'data[polygon][0][points][1][y]': ['33.45313089868531'], 
            'data[polygon][0][points][2][x]': ['126.56680169026187'], 
            'data[polygon][0][points][2][y]': ['33.45036276092556'], 
            'data[polygon][0][points][3][x]': ['126.57096169322682'], 
            'data[polygon][0][points][3][y]': ['33.45083704161905'], 
            'data[polygon][0][coordinate]': ['wgs84'], 
            'data[polygon][0][options][strokeColor]': ['#39f'], 
            'data[polygon][0][options][strokeWeight]': ['3'], 
            'data[polygon][0][options][strokeStyle]': ['solid'], 
            'data[polygon][0][options][strokeOpacity]': ['1'], 
            'data[polygon][0][options][fillColor]': ['#39f'], 
            'data[polygon][0][options][fillOpacity]': ['0.5']
        - output data
            sequence, x or y
    """
    arr_key = divide_data(keys)
    type = arr_key[2]
    if type == "points": return {"sequence":arr_key[3], "xy":arr_key[4]}
    else: return False