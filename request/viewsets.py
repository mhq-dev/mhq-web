from request.views import RequestViewSet

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
