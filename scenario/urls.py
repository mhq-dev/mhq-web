from django.urls import path
from . import viewsets

urlpatterns = [
    path('collection/<int:collection_id>/', viewsets.scenarios_list),
    path('create_scenario', viewsets.create_scenario),
    path('<int:pk>/', viewsets.scenario_detail),
    path('<int:collection_id>/<int:scenario_id>', viewsets.specific_scenario_edges),
    path('all_modules/<int:scenario_id>', viewsets.all_modules_scenario),
]
