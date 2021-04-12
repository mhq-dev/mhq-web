from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from authentication.models import User
from collection.models import Collection, UserCollection
from collection.permissions import CollectionPermission, has_add_user_permission, has_remove_or_promote_user_permission
from collection.serializers import CollectionFullSerializer, UserCollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionFullSerializer
    permission_classes = [CollectionPermission, ]

    def get_queryset(self):
        return Collection.objects.all().filter(Q(type=Collection.PUBLIC)
                                               | Q(usercollection__user=self.request.user)).distinct()

    def get_user_collection_queryset(self):
        return UserCollection.objects.all().filter(Q(collection__type=Collection.PUBLIC)
                                                   | Q(collection__usercollection__user=self.request.user))

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

    def add_user(self, request, *args, **kwargs):
        username = kwargs.get('username')
        role = request.data['role']
        user = get_object_or_404(User, username=username)
        collection = self.get_object()
        role = UserCollectionSerializer().validate_role(role)
        self.check_add_user_permission(request, UserCollection.objects.get(user=request.user, collection=collection))
        UserCollection.objects.create(user=user, role=role, collection=collection).save()
        return Response({'msg': 'added successfully'}, status=status.HTTP_200_OK)

    def check_add_user_permission(self, request, applicant_user_collection):
        if not has_add_user_permission(applicant_user_collection):
            self.permission_denied(request, message='You are not allowed to add new users!')

    def remove_user(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        collection = self.get_object()
        self.check_remove_or_promote_user_permission(request,
                                                     UserCollection.objects.get(user=request.user,
                                                                                collection=collection),
                                                     UserCollection.objects.get(user=user, collection=collection))
        UserCollection.objects.get(user=user, collection=collection).delete()
        return Response({'msg': 'removed successfully'}, status=status.HTTP_200_OK)

    def promote_user(self, request, *args, **kwargs):
        username = kwargs.get('username')
        role = request.data['role']
        user = get_object_or_404(User, username=username)
        collection = self.get_object()
        role = UserCollectionSerializer().validate_role(role)
        self.check_remove_or_promote_user_permission(request,
                                                     UserCollection.objects.get(user=request.user,
                                                                                collection=collection),
                                                     UserCollection.objects.get(user=user, collection=collection))
        user_collection = UserCollection.objects.get(user=user, collection=collection)
        user_collection.role = role
        user_collection.save()
        return Response({'msg': 'promoted successfully'}, status=status.HTTP_200_OK)

    def check_remove_or_promote_user_permission(self, request, applicant_user_collection, requested_user_collection):
        if not has_remove_or_promote_user_permission(applicant_user_collection, requested_user_collection):
            self.permission_denied(request, message='You are not allowed to remove or promote this users!')

    def left(self, request, *args, **kwargs):
        collection = self.get_object()
        UserCollection.objects.get(user=request.user, collection=collection).delete()
        return Response({'msg': 'left successfully'}, status=status.HTTP_200_OK)
