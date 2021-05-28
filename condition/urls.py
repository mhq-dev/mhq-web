from django.urls.conf import path
from . import viewsets

urlpatterns = [
    path('available_condition/', viewsets.available_cond),
    path('<int:pk>', viewsets.detail_cond),
    path('', viewsets.create_cond),

]
