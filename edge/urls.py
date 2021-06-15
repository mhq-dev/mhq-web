from django.urls import path
from . import viewsets

urlpatterns = [
    path('', viewsets.edge_create),
    path('<int:pk>', viewsets.edge_details),
]
