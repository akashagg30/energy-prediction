from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL
class Energy_Data(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE, null = True)
    date_created = models.DateField(auto_now_add = True, null = True)
    building_id = models.IntegerField(null = True)
    air_temperature = models.FloatField(null = True)
    cloud_coverage = models.FloatField(null = True)
    dew_temperature = models.FloatField(null = True)
    floor_count = models.IntegerField(null = True)
    precip_depth_1_hr = models.FloatField(null = True)
    sea_level_pressure = models.FloatField(null = True)
    building_size = models.FloatField(null = True)
    wind_direction = models.FloatField(null=True)
    wind_speed = models.FloatField(null = True)
    year_built = models.IntegerField(null = True)
    primary_use = models.CharField(max_length=200,null=True)
    timestamp = models.DateTimeField(null = True)
    meter_type = models.CharField(max_length=200, null=True)
    meter_reading = models.FloatField(null = True)
