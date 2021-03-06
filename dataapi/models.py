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
        return "id: {}\n    name: {}\n    latitude, longitude: [{}, {}]\n".format(self.id, self.name, self.latitude, self.longitude)



# Create your models here.
class Forecast(models.Model):
    reference_time = models.DateTimeField('reference time', null=True)
    valid_times = ArrayField(models.DateTimeField('valid time'), default=list, size=40)
    sig_ht_comb = ArrayField(models.DecimalField(max_digits=6, decimal_places=2), default=list, size=40)
    prim_wave_period = ArrayField(models.IntegerField(), default=list, size=40)
    prim_wave_dir = ArrayField(models.IntegerField(), default=list, size=40)
    sig_ht_windwaves = ArrayField(models.DecimalField(max_digits=6, decimal_places=2), default=list, size=40)
    sig_ht_swellwaves1 = ArrayField(models.DecimalField(max_digits=6, decimal_places=2), default=list, size=40)
    sig_ht_swellwaves2 = ArrayField(models.DecimalField(max_digits=6, decimal_places=2), default=list, size=40)
    mean_windwave_period = ArrayField(models.IntegerField(), default=list, size=40)
    mean_swellwave_period1 = ArrayField(models.IntegerField(), default=list, size=40)
    mean_swellwave_period2 = ArrayField(models.IntegerField(), default=list, size=40)
    windwave_dir = ArrayField(models.IntegerField(), default=list, size=40)
    swellwave1_dir = ArrayField(models.IntegerField(), default=list, size=40)
    swellwave2_dir = ArrayField(models.IntegerField(), default=list, size=40)
    wind_speed = ArrayField(models.DecimalField(max_digits=6, decimal_places=2), default=list, size=40)
    wind_dir = ArrayField(models.IntegerField(), default=list, size=40)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

    def __str__(self):
        return "\n\nForecast ----------------------------------------------\n \
         id: {}\n \
         spot_id: {}\n \
         reference_time: {}\n \
         valid_times: {}\n \
         sig_ht_comb: {}\n \
         prim_wave_period: {}\n \
         prim_wave_dir: {}\n \
         sig_ht_windwaves: {}\n \
         sig_ht_swellwaves1: {}\n \
         sig_ht_swellwaves2: {}\n \
         mean_windwave_period: {}\n \
         mean_swellwave_period1: {}\n \
         mean_swellwave_period2: {}\n \
         windwave_dir: {}\n \
         swellwave1_dir: {}\n \
         swellwave2_dir: {}\n \
         wind_speed: {}\n \
         wind_dir: {}\n \
         ".format(self.id, self.spot.id, self.reference_time, self.valid_times, self.sig_ht_comb,
         self.prim_wave_period, self.prim_wave_dir, self.sig_ht_windwaves, self.sig_ht_swellwaves1,
         self.sig_ht_swellwaves2, self.mean_windwave_period, self.mean_swellwave_period1,
         self.mean_swellwave_period2, self.windwave_dir, self.swellwave1_dir, self.windwave_dir,
         self.swellwave1_dir, self.swellwave2_dir, self.wind_speed, self.wind_dir,)
