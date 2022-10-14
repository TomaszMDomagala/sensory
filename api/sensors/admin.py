from django.contrib import admin
from sensors.models import Sensors

class SensorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sensors, SensorAdmin)