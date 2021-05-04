from .serializers import ModuleCreateSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Module


class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Module.objects.all()
