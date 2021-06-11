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
})

specific_scenario_edges = ScenarioViewSets.as_view({
    'get': 'retrieve',
})

all_modules_scenario = ScenarioViewSets.as_view({
    'get': 'get_module_of_scenario'
})

scenario_starter_module = ScenarioViewSets.as_view({
    'put': 'set_starter_module',
})

scenario_schedule = ScheduleViewSet.as_view({
    'get': 'get_schedule',
    'put': 'set_schedule',
})

execute = ScenarioViewSets.as_view({
    'get': 'execute',
})
