from .views import ConditionViewSet

available_cond = ConditionViewSet.as_view({
    'get': 'get_available_conditions'
})

detail_cond = ConditionViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})

create_cond = ConditionViewSet.as_view({
    'post': 'create'
})
