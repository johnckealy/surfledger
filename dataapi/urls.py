from django.urls import path
from dataapi.views import ForecastAPIView, SpotsListAPIView, SpotDetailAPIView


urlpatterns = [
    path("spots/<int:pk>/forecast/", ForecastAPIView.as_view(), name="get-forecast"),
    path("spots/", SpotsListAPIView.as_view(), name="spots-list"),
    path("spots/<int:pk>/", SpotDetailAPIView.as_view(), name="spot-detail")
] 