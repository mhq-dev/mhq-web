from django.urls import path

from request.viewsets import request_list, request_detail, request_create

urlpatterns = [
    path('requests/<str:collection_id>', request_list),
    path('request/', request_create),
    path('request/<int:pk>', request_detail)
]
