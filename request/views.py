from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from collection.models import Collection
from request.models import Request
from request.permissions import RequestPermission
from request.serializers import RequestFullSerializer


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestFullSerializer
    permission_classes = [RequestPermission, ]

    def get_queryset(self):
        return Request.objects.all().filter(Q(collection__type=Collection.PUBLIC)
                                            | Q(collection__usercollection__user=self.request.user))

    def list(self, request, *args, **kwargs):
        collection_id = kwargs.get('collection_id')
        collection = get_object_or_404(Collection, id=collection_id)
        requests = Request.objects.all().filter(collection=collection)
        return JsonResponse(RequestFullSerializer(requests, many=True).data, safe=False)
