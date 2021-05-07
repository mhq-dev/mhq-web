from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
import requests
from rest_framework.response import Response

from collection.models import Collection
from request.models import Request
from request.permissions import RequestPermission
from request.serializers import RequestFullSerializer


def get_key_value_dict(key_values):
    kv_dict = dict()
    for kv in key_values:
        kv_dict[kv.key] = kv.value
    return kv_dict


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestFullSerializer
    permission_classes = [RequestPermission, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Request.objects.all().filter(Q(collection__type=Collection.PUBLIC)
                                                | Q(collection__usercollection__user=self.request.user)).distinct()
        return Request.objects.all().filter(Q(collection__type=Collection.PUBLIC))

    def get_collection_queryset(self):
        if self.request.user.is_authenticated:
            return Collection.objects.all().filter(Q(type=Collection.PUBLIC)
                                                   | Q(usercollection__user=self.request.user)).distinct()
        return Collection.objects.all().filter(Q(type=Collection.PUBLIC))

    def list(self, request, *args, **kwargs):
        collection_id = kwargs.get('collection_id')
        collection = get_object_or_404(self.get_collection_queryset(), id=collection_id)
        mhq_requests = self.get_queryset().filter(collection=collection)
        return JsonResponse(RequestFullSerializer(mhq_requests, many=True).data, safe=False)

    def execute(self, request, pk):
        mhq_request = self.get_object()
        result = ""
        if mhq_request.http_method == Request.GET:
            try:
                result = requests.get(mhq_request.url,
                                      headers=get_key_value_dict(mhq_request.get_headers()),
                                      params=get_key_value_dict(mhq_request.get_params())
                                      )
            except:
                return Response({"msg": "Error: Could not send request"}, status=status.HTTP_400_BAD_REQUEST)

        if mhq_request.http_method == Request.POST:
            try:
                result = requests.post(mhq_request.url,
                                       json=mhq_request.body,
                                       headers=get_key_value_dict(mhq_request.get_headers())
                                       )
            except:
                return Response({"msg": "Error: Could not send request"}, status=status.HTTP_400_BAD_REQUEST)

        if mhq_request.http_method == Request.PUT:
            try:
                result = requests.put(mhq_request.url,
                                      data=mhq_request.body,
                                      headers=get_key_value_dict(mhq_request.get_headers())
                                      )
            except:
                return Response({"msg": "Error: Could not send request"}, status=status.HTTP_400_BAD_REQUEST)

        if mhq_request.http_method == Request.DELETE:
            try:
                print(get_key_value_dict(mhq_request.get_headers()))
                result = requests.delete(mhq_request.url,
                                         headers=get_key_value_dict(mhq_request.get_headers()))
            except:
                return Response({"msg": "Error: Could not send request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result_body = result.json()
        except ValueError:
            result_body = result.text

        return Response({
            "status": result.status_code,
            "headers": result.headers,
            "cookies": result.cookies,
            "body": result_body,
        }, status=status.HTTP_200_OK)
