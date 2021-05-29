from django.urls import path
from . import viewsets

urlpatterns = [
    path('', viewsets.edge_create),
    path('<int:pk>', viewsets.edge_details),
    path('statement', viewsets.statement_create),
    path('statement/<int:pk>', viewsets.statement_details)
]
