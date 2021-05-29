from .views import ScenarioViewSets

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
