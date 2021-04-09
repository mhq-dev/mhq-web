from django.urls import path

from authentication.viewsets import *

urlpatterns = [
    path('profile/<int:pk>/', get_user_profile),
    path('profile/update/', update_user_profile)
]
