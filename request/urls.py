from django.urls import path

from request.viewsets import request_list, request_detail, request_create

urlpatterns = [
    path('collection/<int:collection_id>/', request_list),
    path('', request_create),
    path('<int:pk>/', request_detail)
]
