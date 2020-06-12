from django.views.generic import TemplateView
from dataapi.models import Spot, Forecast 
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = "ledger/home.html"



def search(request):
    if request.method == 'GET':
        spotid = int(request.GET['spotid'])
        print(spotid)
        spot = Spot.objects.get(pk=spotid)
        
        # breakpoint()
        forecast = spot.forecast_set.order_by('-reference_time')
    return render(request,'ledger/spot_detail.html',{'spot': spot, 'forecast': forecast})