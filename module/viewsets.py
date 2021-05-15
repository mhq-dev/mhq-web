from .views import ModuleViewSet

create_module = ModuleViewSet.as_view({
    'post': 'create'
})

details_module = ModuleViewSet.as_view({
    'delete': 'destroy',
    'put': 'update',
})

module_complete_data = ModuleViewSet.as_view({
    'get': 'retrieve',
})
