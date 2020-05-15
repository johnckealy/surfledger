from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime
from django.utils import timezone




# class Spot(models.Model):
#     name = models.CharField(max_length=200)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     description =  models.TextField()
#
#
#     def __str__(self):
#         return self.name
#
#
#
# # Create your models here.
# class Forecast(models.Model):
#     reference_time = models.DateTimeField('reference time')
#     valid_time = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
#     sig_wave_ht = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
#     prim_swell_ht = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
#     prim_wave_dir = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
#     sec_swell_ht = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
#     sec_swell_period = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
#     max_wave = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
#     wind_dir = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
#     wind_speed = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
#     forecast = models.ForeignKey(Forecast, on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return self.name
