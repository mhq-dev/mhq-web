from django.urls import path
from . import viewsets

urlpatterns = [
    path('collection/<int:collection_id>/', viewsets.scenarios_list),
    path('', viewsets.create_scenario),
    path('<int:pk>/', viewsets.scenario_detail),
    path('<int:pk>/schedule/', viewsets.scenario_schedule),
    path('<int:pk>/execute/', viewsets.execute),
    path('history/<int:pk>/', viewsets.scenario_history_delete),
    path('history/alls/<int:collection_id>/', viewsets.scenario_history_get_list),
]
