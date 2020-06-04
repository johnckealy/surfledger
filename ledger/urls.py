from django.urls import path, re_path
from .views import HomeView, search

app_name = 'ledger'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
   
    re_path(r'^search/$',search),
]
