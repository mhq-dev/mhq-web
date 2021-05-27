from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from authentication.models import User, UserFollow
from authentication.serializer import UserProfileSerializer, UserFollowCreateSerializer, UserLiteSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(User, username=kwargs.get('username'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def search(self, request, *args, **kwargs):
        search_key = kwargs.get('username').lower()
        if len(search_key) == 0:
            return Response({'msg': 'send something ...'}, status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.all().filter(username__icontains=search_key)
        return JsonResponse(UserProfileSerializer(users, many=True).data, safe=False, status=status.HTTP_200_OK)

    def get_followers(self, request, *args, **kwargs):
        uname = kwargs.get('username').lower()
        user = get_object_or_404(User, username=uname)
        return JsonResponse(UserLiteSerializer(user.get_user_followers(), many=True).data, safe=False,
                            status=status.HTTP_200_OK)

    def get_followings(self, request, *args, **kwargs):
        uname = kwargs.get('username').lower()
        user = get_object_or_404(User, username=uname)
        return JsonResponse(UserLiteSerializer(user.get_user_followings(), many=True).data, safe=False,
                            status=status.HTTP_200_OK)


class UserFollowViewSet(viewsets.ModelViewSet):
    serializer_class = UserFollowCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return UserFollow.objects.all()

    def create(self, request, *args, **kwargs):
        dist_username = kwargs.get('username')
        dist_user = get_object_or_404(User, username=dist_username)
        serializer = UserFollowCreateSerializer(
            data={'follower': request.user.id, 'followed': dist_user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ## TODO {return the username of validated data}
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        username = kwargs.get('username')
        dist_user = get_object_or_404(User, username=username)
        user_follow = get_object_or_404(UserFollow, follower=request.user, followed=dist_user)
        user_follow.delete()
        return Response({'msg': 'delete successfully'}, status=status.HTTP_200_OK)
