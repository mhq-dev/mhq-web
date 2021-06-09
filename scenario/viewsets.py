from .views import ScenarioViewSets, ScheduleViewSet

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