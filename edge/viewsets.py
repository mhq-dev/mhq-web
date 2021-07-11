from .views import EdgeViewSet

edge_create = EdgeViewSet.as_view({
    'post': 'create'
})

edge_detail = EdgeViewSet.as_view({
    'delete': 'destroy',
    'put': 'update',
    'get': 'retrieve'
})
