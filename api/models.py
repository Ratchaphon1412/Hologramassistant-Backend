from django.db import models

# Create your models here.
class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    

class DHT22(models.Model):
   
    temperature = models.FloatField()
    humidity = models.FloatField()


