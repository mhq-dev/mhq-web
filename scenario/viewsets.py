from .views import ScenarioViewSets

all_scenarios = ScenarioViewSets.as_view({
    'get': 'list',
})