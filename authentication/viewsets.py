from authentication.views import UserProfileViewSet

get_user_profile = UserProfileViewSet.as_view({
    'get': 'retrieve'
})

update_user_profile = UserProfileViewSet.as_view({
    'put': 'update'
})
