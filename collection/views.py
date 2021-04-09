from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets

from collection.models import Collection, UserCollection
from collection.serializers import CollectionFullSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionFullSerializer

    def get_queryset(self):
        return Collection.objects.all().filter(Q(type=Collection.PUBLIC) | Q(usercollection__user=self.request.user))

    def list(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user_collections = UserCollection.objects.all().filter(user__id=user_id)
        collections = []
        for user_collection in user_collections:
            collections.append(user_collection.collection)
        return JsonResponse(CollectionFullSerializer(collections, many=True).data, safe=False)
