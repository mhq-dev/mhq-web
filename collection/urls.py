from django.urls import path

from .viewsets import collection_list, collection_detail, collection_create

urlpatterns = [
    path('user/<int:user_id>/', collection_list),
    path('', collection_create),
    path('<int:pk>/', collection_detail)
]
