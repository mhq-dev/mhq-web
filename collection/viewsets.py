from collection.views import CollectionViewSet

collection_list = CollectionViewSet.as_view({
    'get': 'list',
})

collection_create = CollectionViewSet.as_view({
    'post': 'create'
})

collection_detail = CollectionViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'put': 'update',
})
