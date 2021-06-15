from django.urls import path
from . import viewsets

urlpatterns = [
    path('collection/<int:collection_id>/', viewsets.scenarios_list),
    path('', viewsets.create_scenario),
    path('<int:pk>/', viewsets.scenario_detail),
    path('<int:pk>/schedule/', viewsets.scenario_schedule),
    path('<int:pk>/execute/', viewsets.execute),
    path('<int:pk>/history/', viewsets.scenario_history),
    path('collection/<int:collection_id>/history/', viewsets.scenario_collection_history),
    path('history/', viewsets.scenario_history_list)
]
