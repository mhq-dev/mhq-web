from collection.views import CollectionViewSet

user_collection_list = CollectionViewSet.as_view({
    'get': 'list',
})

user_collection_detail = CollectionViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'put': 'update',
})
