from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import User
from collection.models import Collection, UserCollection
from collection.permissions import CollectionPermission, has_add_user_permission, has_remove_or_promote_user_permission
from collection.serializers import CollectionFullSerializer, UserCollectionSerializer, UserCollectionUpdateSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionFullSerializer
    permission_classes = [CollectionPermission, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Collection.objects.all().filter(Q(type=Collection.PUBLIC)
                                                   | Q(usercollection__user=self.request.user)).distinct()
        return Collection.objects.all().filter(Q(type=Collection.PUBLIC))

    def get_user_collection_queryset(self):
        if self.request.user.is_authenticated:
            return UserCollection.objects.all().filter(Q(collection__type=Collection.PUBLIC)
                                                       | Q(collection__usercollection__user=self.request.user))
        return UserCollection.objects.all().filter(Q(collection__type=Collection.PUBLIC))

    def list(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user_collections = self.get_user_collection_queryset().filter(user__username=username)
        collections = []
        for user_collection in user_collections:
            if user_collection.collection not in collections:
                collections.append(user_collection.collection)
        return JsonResponse(CollectionFullSerializer(collections, many=True).data, safe=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = serializer.save()

        UserCollection.objects.create(user=request.user, role=UserCollection.OWNER, collection=collection).save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserCollectionViewSet(viewsets.GenericViewSet):
    permission_classes = [CollectionPermission, IsAuthenticated, ]
    serializer_class = UserCollectionSerializer
    update_serializer_class = UserCollectionUpdateSerializer

    def get_queryset(self):
        pass

    def add_user(self, request, pk, username):
        role = request.data['role']
        user = get_object_or_404(User, username=username)
        collection = get_object_or_404(Collection, id=pk)
        user_collection = get_object_or_404(UserCollection, user=request.user, collection=collection)
        self.check_add_user_permission(request, user_collection)
        serializer = self.update_serializer_class(data={'role': role, 'user': user.id, 'collection': collection.id})
        serializer.is_valid(raise_exception=True)
        x = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_add_user_permission(self, request, applicant_user_collection):
        if not has_add_user_permission(applicant_user_collection):
            self.permission_denied(request, message='You are not allowed to add new users!')

    def remove_user(self, request, pk, username):
        user = get_object_or_404(User, username=username)
        collection = get_object_or_404(Collection, id=pk)
        applicant_user_collection = get_object_or_404(UserCollection, user=request.user, collection=collection)
        requested_user_collection = get_object_or_404(UserCollection, user=user, collection=collection)
        self.check_remove_or_promote_permission(request, applicant_user_collection, requested_user_collection)
        requested_user_collection.delete()
        return Response({'msg': 'removed successfully'}, status=status.HTTP_200_OK)

    def promote_user(self, request, pk, username):
        role = request.data['role']
        user = get_object_or_404(User, username=username)
        collection = get_object_or_404(Collection, id=pk)
        applicant_user_collection = get_object_or_404(UserCollection, user=request.user, collection=collection)
        requested_user_collection = get_object_or_404(UserCollection, user=user, collection=collection)
        self.check_remove_or_promote_permission(request, applicant_user_collection, requested_user_collection)
        serializer = self.update_serializer_class(instance=requested_user_collection,
                                                  data={'role': role, 'user': user.id, 'collection': collection.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_remove_or_promote_permission(self, request, applicant_user_collection, requested_user_collection):
        if not has_remove_or_promote_user_permission(applicant_user_collection, requested_user_collection):
            self.permission_denied(request, message='You are not allowed to remove or promote this users!')

    def left(self, request, pk):
        collection = get_object_or_404(Collection, id=pk)
        get_object_or_404(UserCollection, user=request.user, collection=collection).delete()
        return Response({'msg': 'left successfully'}, status=status.HTTP_200_OK)
