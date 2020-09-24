from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL
class Energy_Data(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE, null = True)
    date_created = models.DateField(auto_now_add = True, null = True)
    building_id = models.IntegerField(null = True)
    precip_depth = models.FloatField(null = True)
    air_temeprature = models.FloatField(null = True)
    dew_temperature = models.FloatField(null = True)
    building_size = models.IntegerField(null = True)
    year_built = models.IntegerField(null = True)
    floor_count = models.IntegerField(null = True)
    meter_reading = models.FloatField(null=True)

    
