from django.db import models
from django.conf import settings
import uuid

class Sensors(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pressure = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    light = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    moisture = models.PositiveIntegerField(blank=True, null=True)

    date_time = models.DateTimeField(auto_now=True)
    slave_ip = models.GenericIPAddressField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.id

    class Meta:
        ordering = ['date_time', 'slave_ip', 'author']
        verbose_name = "Sensor"
