from django.http import JsonResponse
from rest_framework import viewsets

from collection.models import Collection, UserCollection
from collection.serializers import CollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.all()

    def list(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user_collections = UserCollection.objects.all().filter(user__username=username)
        collections = []
        for user_collection in user_collections:
            collections.append(user_collection.collection)
        return JsonResponse(CollectionSerializer(collections, many=True).data, safe=False)
