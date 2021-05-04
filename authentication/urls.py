from django.urls import path

from authentication.viewsets import *

urlpatterns = [
    path('profile/user/<str:username>/', get_user_profile),
    path('profile/update/', update_user_profile),
    path('search_users/<str:useranme_search>', search_by_username),
]
