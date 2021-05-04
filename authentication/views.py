from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from authentication.models import User
from authentication.serializer import UserProfileSerializer

from django.http import HttpResponse
from rest_framework.decorators import api_view
import mhq_web.celery as clry


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
        search_key = kwargs.get('useranme_search').lower()
        if len(search_key) == 0:
            return Response({'msg': 'send something ...'}, status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.all().filter(username__icontains=search_key)
        return JsonResponse(UserProfileSerializer(users, many=True).data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_celery(request):
    clry.test_task.delay()
    clry.test_task.delay()
    clry.test_task.delay()
    clry.test_task.delay()
    return HttpResponse()
