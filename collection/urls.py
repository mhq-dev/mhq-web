from django.urls import path

from .viewsets import collection_list, collection_detail, collection_create

urlpatterns = [
    path('user/<str:username>/', collection_list),
    path('', collection_create),
    path('<int:pk>/', collection_detail)
]
