from django.urls import path

from .viewsets import user_collection_list, user_collection_detail

urlpatterns = [
    path('collections/<str:username>', user_collection_list),
    path('collection/<int:pk>', user_collection_detail)
]
