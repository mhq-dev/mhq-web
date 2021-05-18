from django.urls import path
from . import viewsets

urlpatterns = [
    path('', viewsets.create_module),
    path('<int:pk>/', viewsets.details_module),
    path('request/<int:module_id>/', viewsets.module_complete_data),
]
