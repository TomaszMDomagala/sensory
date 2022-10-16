from rest_framework import serializers
from sensors.models import Sensors


class SensorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensors
        fields = ['temperature', 'humidity', 
                  'pressure', 'light', 'moisture', 
                  'slave_ip', 'author'
                  ]
        
