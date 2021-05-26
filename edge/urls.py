from django.urls import path
from . import viewsets

urlpatterns = [
    path('', viewsets.create_edge),
    path('<int:pk>', viewsets.edge_details),
]
