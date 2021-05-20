from authentication.views import UserProfileViewSet, UserFollowViewSet

get_user_profile = UserProfileViewSet.as_view({
    'get': 'retrieve'
})

update_user_profile = UserProfileViewSet.as_view({
    'put': 'update'
})

search_by_username = UserProfileViewSet.as_view({
    'get': 'search'
})

user_follow = UserFollowViewSet.as_view({
    'post': 'create'
})

user_unfollow = UserFollowViewSet.as_view({
    'delete': 'destroy'
})

user_get_following = UserFollowViewSet.as_view({
    'get': 'get_user_followings'
})

user_get_follower = UserProfileViewSet.as_view({
    'get': 'get_user_followers'
})
