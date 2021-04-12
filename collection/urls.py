from django.urls import path

from .viewsets import *

urlpatterns = [
    path('user/<str:username>/', collection_list),
    path('', collection_create),
    path('<int:pk>/', collection_detail),
    path('add_user/', collection_add_user),
    path('remove_user/', collection_remove_user),
    path('promote_user/', collection_promote_user),
    path('left/', collection_left)
]
