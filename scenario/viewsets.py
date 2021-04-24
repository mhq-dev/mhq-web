from .views import ScenarioViewSets

scenarios_list = ScenarioViewSets.as_view({
    'get': 'list',
})

create_scenario = ScenarioViewSets.as_view({
    'post': 'create'
})

scenario_detail = ScenarioViewSets.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'put': 'update',
})
