from django.urls import path
from . import viewsets

urlpatterns = [
    path('collection/<int:collection_id>/', viewsets.scenarios_list),
    path('', viewsets.create_scenario),
    path('<int:pk>/', viewsets.scenario_detail),
    path('<int:pk>/schedule/', viewsets.scenario_schedule),
]
