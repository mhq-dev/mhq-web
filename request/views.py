from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets

from collection.models import Collection
from request.models import Request
from request.serializers import RequestFullSerializer


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestFullSerializer

    def get_queryset(self):
        return Request.objects.all().filter(Q(collection__type=Collection.PUBLIC)
                                            | Q(collection__usercollection__user=self.request.user))

    def list(self, request, *args, **kwargs):
        collection_id = kwargs.get('collection_id')
        requests = Request.objects.all().filter(collection__id=collection_id)
        return JsonResponse(RequestFullSerializer(requests, many=True).data, safe=False)
