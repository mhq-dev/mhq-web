from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from authentication.models import User
from collection.models import Collection, UserCollection


class CollectionViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="amirh")
        self.generate_basic_database()
        self.token = Token.objects.create(user=self.user)

    def generate_basic_database(self):
        sadra = User.objects.create_user(username="sadra")
        self.col1 = Collection.objects.create(type='public', name='col1')
        UserCollection.objects.create(user=sadra, collection=self.col1, role=UserCollection.OWNER)
        self.col2 = Collection.objects.create(type='private', name='col2')
        UserCollection.objects.create(user=sadra, collection=self.col2, role=UserCollection.OWNER)
        self.col3 = Collection.objects.create(type='public', name='col3')
        UserCollection.objects.create(user=self.user, collection=self.col3, role=UserCollection.OWNER)
        self.col4 = Collection.objects.create(type='private', name='col4')
        UserCollection.objects.create(user=self.user, collection=self.col4, role=UserCollection.OWNER)

    def test_collection_list(self):
        response = self.client.get(reverse('collection-list', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        response = self.client.get(reverse('collection-list', kwargs={'username': 'sadra'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('collection-list', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        response = self.client.get(reverse('collection-list', kwargs={'username': 'sadra'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_collection_create(self):
        response = self.client.post(reverse('collection-create'), {"type": "public", "name": "col5"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('collection-create'), {"type": "public", "name": "col5"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('collection-create'), {"type": "private", "name": "col5"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('collection-create'), {"type": "private", "name": "col5-private"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('collection-create'), {"type": "asdfgsdfasd", "name": "col5-invalid-type"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('collection-create'), {"type": "public"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('collection-create'), {"name": "col5-without-type"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['type'], 'public')

    def test_collection_detail(self):
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.col3.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.col4.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.put(reverse('collection-detail', kwargs={'pk': self.col3.id}), {'name': 'col3-renamed'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(reverse('collection-detail', kwargs={'pk': self.col3.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.col2.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(reverse('collection-detail', kwargs={'pk': self.col4.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('collection-detail', kwargs={'pk': self.col3.id}), {'name': 'col3-renamed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('collection-detail', kwargs={'pk': self.col4.id}), {'name': 'col4-renamed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('collection-detail', kwargs={'pk': self.col1.id}), {'name': 'col1-renamed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(reverse('collection-detail', kwargs={'pk': self.col3.id}), {'type': 'private'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.delete(reverse('collection-detail', kwargs={'pk': self.col3.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse('collection-detail', kwargs={'pk': self.col4.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse('collection-detail', kwargs={'pk': self.col1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserCollectionViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="amirh")
        self.generate_basic_database()
        self.token = Token.objects.create(user=self.user)

    def generate_basic_database(self):
        sadra = User.objects.create_user(username='sadra')
        owner_user = User.objects.create_user(username='owner_user')
        editor_user = User.objects.create_user(username='editor_user')
        visitor_user = User.objects.create_user(username='visitor_user')
        self.col1 = Collection.objects.create(type='private', name='col1')
        UserCollection.objects.create(user=self.user, collection=self.col1, role=UserCollection.OWNER)
        UserCollection.objects.create(user=owner_user, collection=self.col1, role=UserCollection.OWNER)
        UserCollection.objects.create(user=editor_user, collection=self.col1, role=UserCollection.EDITOR)
        UserCollection.objects.create(user=visitor_user, collection=self.col1, role=UserCollection.VISITOR)
        self.col2 = Collection.objects.create(type='private', name='col2')
        UserCollection.objects.create(user=self.user, collection=self.col2, role=UserCollection.EDITOR)
        UserCollection.objects.create(user=owner_user, collection=self.col2, role=UserCollection.OWNER)
        UserCollection.objects.create(user=editor_user, collection=self.col2, role=UserCollection.EDITOR)
        UserCollection.objects.create(user=visitor_user, collection=self.col2, role=UserCollection.VISITOR)
        self.col3 = Collection.objects.create(type='private', name='col3')
        UserCollection.objects.create(user=self.user, collection=self.col3, role=UserCollection.VISITOR)
        UserCollection.objects.create(user=owner_user, collection=self.col3, role=UserCollection.OWNER)
        UserCollection.objects.create(user=editor_user, collection=self.col3, role=UserCollection.EDITOR)
        UserCollection.objects.create(user=visitor_user, collection=self.col3, role=UserCollection.VISITOR)
        self.col4 = Collection.objects.create(type='private', name='col4')
        UserCollection.objects.create(user=owner_user, collection=self.col4, role=UserCollection.OWNER)
        UserCollection.objects.create(user=editor_user, collection=self.col4, role=UserCollection.EDITOR)
        UserCollection.objects.create(user=visitor_user, collection=self.col4, role=UserCollection.VISITOR)

    def test_add_user(self):
        response = self.client.post(reverse('user-collection-add',
                                            kwargs={'pk': self.col1.id, 'username': 'sadra'}),
                                    {'role': 'visitor'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('user-collection-add',
                                            kwargs={'pk': self.col1.id, 'username': 'sadra'}),
                                    {'role': 'visitor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('user-collection-add',
                                            kwargs={'pk': self.col1.id, 'username': 'sadra'}),
                                    {'role': 'chert'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('user-collection-add',
                                            kwargs={'pk': self.col2.id, 'username': 'sadra'}),
                                    {'role': 'visitor'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('user-collection-add',
                                            kwargs={'pk': self.col3.id, 'username': 'sadra'}),
                                    {'role': 'visitor'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('user-collection-add',
                                            kwargs={'pk': self.col4.id, 'username': 'sadra'}),
                                    {'role': 'visitor'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_user(self):
        response = self.client.delete(reverse('user-collection-remove',
                                              kwargs={'pk': self.col1.id, 'username': 'visitor_user'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.delete(reverse('user-collection-remove',
                                              kwargs={'pk': self.col1.id, 'username': 'visitor_user'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('user-collection-remove',
                                              kwargs={'pk': self.col1.id, 'username': 'editor_user'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('user-collection-remove',
                                              kwargs={'pk': self.col1.id, 'username': 'owner_user'}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(reverse('user-collection-remove',
                                              kwargs={'pk': self.col2.id, 'username': 'visitor_user'}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(reverse('user-collection-remove',
                                              kwargs={'pk': self.col4.id, 'username': 'visitor_user'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_promote_user(self):
        response = self.client.put(reverse('user-collection-promote',
                                           kwargs={'pk': self.col1.id, 'username': 'visitor_user'}),
                                   {'role': 'editor'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.put(reverse('user-collection-promote',
                                           kwargs={'pk': self.col1.id, 'username': 'visitor_user'}),
                                   {'role': 'editor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('user-collection-promote',
                                           kwargs={'pk': self.col1.id, 'username': 'visitor_user'}),
                                   {'role': 'chert'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(reverse('user-collection-promote',
                                           kwargs={'pk': self.col1.id, 'username': 'editor_user'}),
                                   {'role': 'visitor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('user-collection-promote',
                                           kwargs={'pk': self.col1.id, 'username': 'owner_user'}),
                                   {'role': 'editor'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(reverse('user-collection-promote',
                                           kwargs={'pk': self.col2.id, 'username': 'visitor_user'}),
                                   {'role': 'editor'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(reverse('user-collection-promote',
                                           kwargs={'pk': self.col3.id, 'username': 'visitor_user'}),
                                   {'role': 'editor'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(reverse('user-collection-promote',
                                           kwargs={'pk': self.col4.id, 'username': 'visitor_user'}),
                                   {'role': 'editor'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_left(self):
        response = self.client.delete(reverse('user-collection-left', kwargs={'pk': self.col1.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.delete(reverse('user-collection-left', kwargs={'pk': self.col1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('user-collection-left', kwargs={'pk': self.col2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('user-collection-left', kwargs={'pk': self.col3.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('user-collection-left', kwargs={'pk': self.col4.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
