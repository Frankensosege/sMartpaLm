from django.db import models
from django.apps import apps


class SensorData(models.Model):
    timestamp = models.DateTimeField()
    ch0 = models.FloatField()
    ch1 = models.FloatField()

    class Meta:
        db_table = 'sensor_data'

    def __str__(self):
        return f"SensorData {self.timestamp}"

