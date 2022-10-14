from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Sensors
from .serializers import SensorsSerializer

class SensorsListApiView(APIView):

    def get(self, request, *args, **kwargs):
        sensors = Sensors.objects.all()
        serializer = SensorsSerializer(sensors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        data = {
            'temperature': request.data.get('task'),
            'humidity': request.data.get('task'),
            'pressure': request.data.get('task'),
            'light': request.data.get('task'),
            'moisture': request.data.get('task'),
            'slave_ip': request.data.get('task'),
            'author': request.data.get('author')
        }
        serializer = SensorsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
