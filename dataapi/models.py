from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime
from django.utils import timezone




class Spot(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description =  models.TextField()
    region =  models.CharField(max_length=200)
    country =  models.CharField(max_length=200)

    def __str__(self):
        return self.name



# Create your models here.
class Forecast(models.Model):
    reference_time = models.DateTimeField('reference time')
    valid_time = ArrayField(models.DateTimeField('valid time'), null=True, blank=True, size=40)
    sig_ht_comb = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
    # prim_wave_period = ArrayField(models.IntegerField(), blank=True, size=40)
    # prim_wave_dir = ArrayField(models.IntegerField(), blank=True, size=40)
    # sig_ht_windwaves = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
    # sig_ht_swellwaves1 = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
    # sig_ht_swellwaves2 = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
    # mean_windwave_period = ArrayField(models.IntegerField(), blank=True, size=40)
    # mean_swellwave_period1 = ArrayField(models.IntegerField(), blank=True, size=40)
    # mean_swellwave_period2 = ArrayField(models.IntegerField(), blank=True, size=40)
    # windwave_dir = ArrayField(models.IntegerField(), blank=True, size=40)
    # swellwave1_dir = ArrayField(models.IntegerField(), blank=True, size=40)
    # swellwave2_dir = ArrayField(models.IntegerField(), blank=True, size=40)
    # wind_speed = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), blank=True, size=40)
    # wind_dir = ArrayField(models.IntegerField(), blank=True, size=40)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

    def __str__(self):
        return "forecast starting at {}".format(self.reference_time)
