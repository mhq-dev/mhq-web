from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from collection.models import Collection
from .serializers import StatementSerializer, EdgeSerializer
from .models import Edge, Statement


class EdgeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = EdgeSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Edge.objects.all().filter(
                Q(source__scenario__collection__type=Collection.PUBLIC)
                | Q(source__scenario__collection__usercollection__user=self.request.user)
            ).distinct()
        return Edge.objects.all().filter(source__scenario__collection__type=Collection.PUBLIC)
