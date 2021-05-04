from django.urls import path
from .viewsets import create_module, details_module

urlpatterns = [
    path('', create_module),
    path('<int:pk>/', details_module),
]
