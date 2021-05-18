from django.urls import path

from .viewsets import *

urlpatterns = [
    path('user/<str:username>/', collection_list, name='collection-list'),
    path('', collection_create, name='collection-create'),
    path('<int:pk>/', collection_detail, name='collection-detail'),
    path('<int:pk>/add_user/<str:username>', user_collection_add, name='user-collection-add'),
    path('<int:pk>/remove_user/<str:username>', user_collection_remove, name='user-collection-remove'),
    path('<int:pk>/promote_user/<str:username>', user_collection_promote, name='user-collection-promote'),
    path('<int:pk>/left/', user_collection_left, name='user-collection-left')
]
