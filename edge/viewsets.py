from .views import EdgeViewSet, StatementViewSet

edge_create = EdgeViewSet.as_view({
    'post': 'create'
})

edge_details = EdgeViewSet.as_view({
    'delete': 'destroy',
    'put': 'update',
})

statement_create = StatementViewSet.as_view({
    'post': 'create'
})

statement_details = StatementViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})
