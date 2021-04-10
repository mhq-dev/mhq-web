from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from authentication.models import User
from collection.models import Collection, UserCollection
from collection.serializers import CollectionFullSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionFullSerializer

    def get_queryset(self):
        return Collection.objects.all().filter(Q(type=Collection.PUBLIC) | Q(usercollection__user=self.request.user))

    def list(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user_collections = UserCollection.objects.all().filter(user__username=username)
        collections = []
        for user_collection in user_collections:
            collections.append(user_collection.collection)
        return JsonResponse(CollectionFullSerializer(collections, many=True).data, safe=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = serializer.save()

        UserCollection.objects.create(user=request.user, role=UserCollection.OWNER, collection=collection).save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def add_user(self, request, *args, **kwargs):
        username = kwargs.get('username')
        collection_id = kwargs.get('collection_id')
        role = kwargs.get('role')

        user = get_object_or_404(User, username=username)
        collection = get_object_or_404(Collection, id=collection_id)
        UserCollection.objects.create(user=user, role=role, collection=collection).save()
        return Response({'msg': 'added successfully'}, status=status.HTTP_200_OK)

    def remove_user(self, request, *args, **kwargs):
        username = kwargs.get('username')
        collection_id = kwargs.get('collection_id')
        UserCollection.objects.get(user__username=username, collection__id=collection_id).save()
        return Response({'msg': 'removed successfully'}, status=status.HTTP_200_OK)
