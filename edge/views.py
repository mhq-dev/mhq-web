from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import EdgeCreateSerializer, StatementSerializer
from .models import Edge, Statement
from .permissions import EdgePermissions


class EdgeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, EdgePermissions]
    serializer_class = EdgeCreateSerializer

    def get_queryset(self):
        return Edge.objects.all()


class StatementViewSet(ModelViewSet):
    # TODO add permission
    permission_classes = [IsAuthenticated, ]
    serializer_class = StatementSerializer

    def get_queryset(self):
        return Statement.objects.all()
