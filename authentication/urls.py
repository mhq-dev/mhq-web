from django.urls import path

from authentication.viewsets import *

urlpatterns = [
    path('profile/user/<str:username>/', get_user_profile, name='get_user_profile'),
    path('profile/update/', update_user_profile, name='update_user_profile'),
    path('search_users/<str:username>', search_by_username, name='search_by_username'),
    path('follow/', user_follow, name='user_follow'),
    path('follow/', user_unfollow, name='user_unfollow'),
    path('followers/<str:username>', user_get_follower, name='user_followers'),
    path('followings/<str:username>', user_get_following, name='user_followings'),
]
