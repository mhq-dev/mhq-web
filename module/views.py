from django.db.models import Q

from collection.models import Collection
from .serializers import ModuleSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Module
from .permissions import ModulePermission


class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, ModulePermission, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Module.objects.all().filter(Q(scenario__collection__type=Collection.PUBLIC)
                                               | Q(scenario__collection__usercollection__user=self.request.user)).distinct()
        return Module.objects.all().filter(scenario__collection__type=Collection.PUBLIC)

    def execute(self, request, *args, **kwargs):
        pass

    def get_dist_modules(self, request, *args, **kwargs):
        pass

    def get_source_modules(self, request, *args, **kwargs):
        pass

    def get_module_response(self, request, *args, **kwargs):
        pass
