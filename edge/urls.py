from django.urls import path
from . import viewsets

urlpatterns = [
    path('', viewsets.edge_create, name='edge-create'),
    path('<int:pk>', viewsets.edge_detail, name='edge_detail'),
]
