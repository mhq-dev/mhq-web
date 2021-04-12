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

collection_add_user = CollectionViewSet.as_view({
    'post': 'add_user',
})

collection_remove_user = CollectionViewSet.as_view({
    'delete': 'remove_user',
})

collection_promote_user = CollectionViewSet.as_view({
    'put': 'promote_user',
})

collection_left = CollectionViewSet.as_view({
    'delete': 'left',
})
