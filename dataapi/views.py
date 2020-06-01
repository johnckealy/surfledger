from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

from dataapi.models import Forecast, Spot
from dataapi.serializers import ForecastSerializer, SpotSerializer
from rest_framework.generics import get_object_or_404




# Create your views here.
class ForecastAPIView(APIView):
    def get(self, request, pk):
        spot = get_object_or_404(Spot, pk=pk)
        forecast = spot.forecast_set.latest('reference_time')
        serializer = ForecastSerializer(forecast)
        return Response(serializer.data) 


class SpotsListAPIView(APIView):
    def get(self, request):
        spots = Spot.objects.all()
        serializer = SpotSerializer(spots, many=True)
        return Response(serializer.data) 


class SpotDetailAPIView(APIView):
    def get(self, request, pk):
        spot = get_object_or_404(Spot, pk=pk)
        serializer = SpotSerializer(spot)
        return Response(serializer.data) 
