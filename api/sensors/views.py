from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Sensors
from .serializers import SensorsSerializer
from django.views.generic.list import ListView
from django.utils import timezone


class SensorsView(ListView):
    
    model = Sensors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class SensorsListApiView(APIView):

    def get(self, request, *args, **kwargs):
        sensors = Sensors.objects.all()
        serializer = SensorsSerializer(sensors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        data = {
            'temperature': round(request.data.get('temperature'), 2),
            'humidity': round(request.data.get('humidity'), 2),
            'pressure': round(request.data.get('pressure'), 2),
            'light': round(request.data.get('light'), 2),
            'moisture': request.data.get('moisture'),
            'slave_ip': request.data.get('slave_ip')
            # 'author': request.data.get('author')
        }
        serializer = SensorsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
