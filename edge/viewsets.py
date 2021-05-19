from .views import EdgeViewSet

create_edge = EdgeViewSet.as_view({
    'post': 'create'
})

edge_details = EdgeViewSet.as_view({
    'delete': 'destroy',
    'put': 'update',
})
