from request.views import RequestViewSet, RequestHistoryViewSet

request_list = RequestViewSet.as_view({
    'get': 'list',
})

request_create = RequestViewSet.as_view({
    'post': 'create'
})

request_detail = RequestViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'put': 'update',
})

request_execute = RequestViewSet.as_view({
    'get': 'execute',
})

request_history_list = RequestHistoryViewSet.as_view({
    'get': 'list',
})
