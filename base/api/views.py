from django.http import JsonResponse
#nao e necessario usar o json pois da rpar usar :
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room
from .serializers import RoomSerializer
#usar rest framework para ciar a api "https://www.django-rest-framework.org/"
@api_view(['GET'])
def getRoutes(request):
    routes =[
        'GET /api/',
        'GET /api/rooms', 
        'GET /api/rooms/:id'
    ]

    # safe -> transformar lista em json
    #return JsonResponse(routes, safe=False)
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    #query para rooms
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    #objects nao podem ser convertidos em json por api->serializator
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):
    #query para rooms
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    #objects nao podem ser convertidos em json por api->serializator
    return Response(serializer.data)

