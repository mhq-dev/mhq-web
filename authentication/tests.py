from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class AccountAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='anonymous', email='test@gmail.com',
                                             first_name='first', last_name='last')
        self.users = [User.objects.create_user(username='anonymous' + str(i), password=6 * 't') for i in range(5)]

    def test_api_get_user_profile(self):
        # UNAUTHORIZED
        response = self.client.get(reverse('get_user_profile', kwargs={'username': 'anonymous'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # OK
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_user_profile', kwargs={'username': 'anonymous'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_other_user_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_user_profile', kwargs={'username': 'anonymous1'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_update_profile(self):
        # UNAUTHORIZED
        response = self.client.put(reverse('update_user_profile'), data={"first_name": "ahmad"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # OK
        self.client.force_login(self.user)
        response = self.client.put(reverse('update_user_profile'), data={"first_name": "string"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), "string")

        # ok
        response = self.client.put(reverse('update_user_profile'), data={"bio": "string"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), "string")

    def test_api_search(self):
        # UNAUTHORIZED
        response = self.client.get(reverse('search_by_username', kwargs={"username": "anonymous"}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # OK
        self.client.force_login(self.user)
        response = self.client.get(reverse('search_by_username', kwargs={"username": "anonymous"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), len(self.users) + 1)

        # ok
        response = self.client.get(reverse('search_by_username', kwargs={"username": "noname"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
