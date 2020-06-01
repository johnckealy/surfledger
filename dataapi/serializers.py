from rest_framework import serializers
from .models import Forecast

class ForecastSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    reference_time = serializers.DateTimeField()
    valid_times = serializers.ListField(child=serializers.DateTimeField())
    sig_ht_comb = serializers.ListField(child=serializers.DecimalField(max_digits=7, decimal_places=2))
    prim_wave_period = serializers.ListField(child=serializers.DecimalField(max_digits=7, decimal_places=2))
    prim_wave_dir = serializers.ListField(child=serializers.DecimalField(max_digits=7, decimal_places=2))
    swellwave1_dir = serializers.ListField(child=serializers.DecimalField(max_digits=7, decimal_places=2))
    spot = serializers.CharField()
    



class SpotSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField()
    region = serializers.CharField()
    country = serializers.CharField()
