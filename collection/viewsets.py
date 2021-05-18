from collection.views import CollectionViewSet, UserCollectionViewSet

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

user_collection_add = UserCollectionViewSet.as_view({
    'post': 'add_user',
})

user_collection_remove = UserCollectionViewSet.as_view({
    'delete': 'remove_user',
})

user_collection_promote = UserCollectionViewSet.as_view({
    'put': 'promote_user',
})

user_collection_left = UserCollectionViewSet.as_view({
    'delete': 'left',
})
