from django.urls import path
from . import viewsets

urlpatterns = [
    path('', viewsets.create_module),
    path('<int:pk>/', viewsets.details_module),
]
