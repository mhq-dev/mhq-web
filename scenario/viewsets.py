from .views import ScenarioViewSets, ScheduleViewSet, ScenarioHistoryViewSet

scenarios_list = ScenarioViewSets.as_view({
    'get': 'list',
})

create_scenario = ScenarioViewSets.as_view({
    'post': 'create'
})

scenario_detail = ScenarioViewSets.as_view({
    'delete': 'destroy',
    'put': 'update',
    'get': 'retrieve',
})

scenario_schedule = ScheduleViewSet.as_view({
    'get': 'get_schedule',
    'put': 'set_schedule',
})

execute = ScenarioViewSets.as_view({
    'get': 'execute',
})

scenario_history = ScenarioHistoryViewSet.as_view({
    'get': 'retrieve'
})

scenario_history_with_id = ScenarioHistoryViewSet.as_view({
    'get': 'retrieve_with_history_id'
})

scenario_collection_history = ScenarioHistoryViewSet.as_view({
    'get': 'list_with_collection',
})

scenario_history_list = ScenarioHistoryViewSet.as_view({
    'get': 'list',
})
