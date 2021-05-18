from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import EdgeCreateSerializer
from .models import Edge
from .permissions import EdgePermissions


class EdgeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, EdgePermissions]
    serializer_class = EdgeCreateSerializer

    def get_queryset(self):
        return Edge.objects.all()
