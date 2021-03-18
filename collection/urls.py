from django.urls import path

from .viewsets import collection_list, collection_detail, collection_create

urlpatterns = [
    path('collections/<str:username>', collection_list),
    path('collection/', collection_create),
    path('collection/<int:pk>', collection_detail)
]
