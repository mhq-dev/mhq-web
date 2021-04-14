from django.urls import path
from .viewsets import all_scenarios

urlpatterns = [
    path('<str:username>/<int:id>', all_scenarios),
]
