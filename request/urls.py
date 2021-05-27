from django.urls import path

from request.viewsets import request_list, request_detail, request_create, request_execute, request_history_list

urlpatterns = [
    path('collection/<int:collection_id>/', request_list, name='request-list'),
    path('', request_create, name='request-create'),
    path('<int:pk>/', request_detail, name='request-detail'),
    path('<int:pk>/execute/', request_execute, name='request-execute'),
    path('history/', request_history_list, name='request-history'),
]
