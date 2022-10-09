from django.db import models
import uuid

class Sensors(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # BME280

    # BH1750

    # MOD-01588

    