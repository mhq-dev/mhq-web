from django.urls import path

from .viewsets import *

urlpatterns = [
    path('user/<str:username>/', collection_list),
    path('', collection_create),
    path('<int:pk>/', collection_detail),
    path('<int:pk>/add_user/<str:username>', collection_add_user),
    path('<int:pk>/remove_user/<str:username>', collection_remove_user),
    path('<int:pk>/promote_user/<str:username>', collection_promote_user),
    path('<int:pk>/left/', collection_left)
]
