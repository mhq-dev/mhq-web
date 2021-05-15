from .serializers import ModuleCreateSerializer, ModuleCompleteSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Module
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from rest_framework import status
from .permissions import ModulePermission


class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleCreateSerializer
    permission_classes = [IsAuthenticated, ModulePermission, ]

    def get_queryset(self):
        return Module.objects.all()

    def retrieve(self, request, *args, **kwargs):
        module_id = kwargs.get('module_id')
        module = get_object_or_404(Module, id=module_id)
        return JsonResponse(ModuleCompleteSerializer(module, many=False).data, safe=False, status=status.HTTP_200_OK)

    def execute(self, request, *args, **kwargs):
        pass

    def get_dist_modules(self, request, *args, **kwargs):
        pass

    def get_source_modules(self, request, *args, **kwargs):
        pass

    def get_module_response(self, request, *args, **kwargs):
        pass
