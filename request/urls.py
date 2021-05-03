from django.urls import path

from request.viewsets import request_list, request_detail, request_create, request_execute

urlpatterns = [
    path('collection/<int:collection_id>/', request_list),
    path('', request_create),
    path('<int:pk>/', request_detail),
    path('<int:pk>/execute/', request_execute),
]
