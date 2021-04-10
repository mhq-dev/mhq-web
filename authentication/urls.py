from django.urls import path

from authentication.viewsets import *

urlpatterns = [
    path('profile/<str:username>/', get_user_profile),
    path('profile/update/', update_user_profile)
]
