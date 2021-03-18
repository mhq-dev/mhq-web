from django.http import JsonResponse
from rest_framework import viewsets

from request.models import Request
from request.serializers import RequestFullSerializer, RequestSerializer


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer

    def get_queryset(self):
        return Request.objects.all()

    def list(self, request, *args, **kwargs):
        collection_id = kwargs.get('collection_id')
        requests = Request.objects.all().filter(collection__id=collection_id)
        return JsonResponse(RequestFullSerializer(requests, many=True).data, safe=False)
