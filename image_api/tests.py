from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient
import json
import os
import shutil

from family_tree.models.family import Family
from family_tree.models.person import Person
from custom_user.models import User
from gallery.models import Image, Gallery, Tag

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class ImageApiTestCase(TestCase):
    '''
    Tests for the Image API
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='philcollins@example.com',
                                        password='easylover',
                                        name='Phil Collins',
                                        family = self.family)

        self.person = Person(name='Phil Collins',
                        gender='M',
                        email='philcollins@example.com',
                        family_id=self.family.id,
                        language='en',
                        user_id=self.user.id)
        self.person.save()

        self.gallery = Gallery.objects.create(title="test_gallery", family_id=self.family.id)
        self.test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        self.image = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))
        self.image.save()

        #Tag person 1 in image
        self.tag = Tag.objects.create(image=self.image, person=self.person, x1=1, x2=2, y1=3, y2=4)

        self.gallery2 = Gallery.objects.create(title="test_gallery2", family_id=self.family.id)
        self.test_image2 = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image.jpg')
        self.test_image2_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery2.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery2.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image2, self.test_image2_destination)

        self.image2 = Image(gallery=self.gallery2, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery2.id), '/test_image.jpg']))
        self.image2.save()

        self.family2 = Family()
        self.family2.save()

        self.user2 = User.objects.create_user(email='phillipbailey@example.com',
                                        password='BetterForgetIt',
                                        name='Phillip Bailey',
                                        family = self.family2)

        self.person2 = Person(name='Phillip Bailey',
                        gender='M',
                        email='phillipbailey@example.com',
                        family_id=self.family2.id,
                        language='en',
                        user_id=self.user2.id)
        self.person2.save()

        super(ImageApiTestCase, self).setUp()


    def test_list_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        response = client.get('/api/image/?page=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_list_page1(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        # Check this works with JWT token
        auth_details = {
            'email': 'philcollins@example.com',
            'password': 'easylover'
        }
        auth_response = client.post('/api/auth/obtain_token/', auth_details, format='json')
        token = json.loads(auth_response.content)["access"]

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/api/image/?page=1', format='json')

        # Check it contains both images
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(self.image.thumbnail).encode() in response.content)
        self.assertTrue(str(self.image2.thumbnail).encode() in response.content)


    def test_list_page1_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        # Login with other user
        auth_details = {
            'email': 'phillipbailey@example.com',
            'password': 'BetterForgetIt'
        }
        auth_response = client.post('/api/auth/obtain_token/', auth_details, format='json')
        token = json.loads(auth_response.content)["access"]

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/api/image/?page=1', format='json')

        # Check it contains neither images
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(str(self.image.thumbnail).encode() in response.content)
        self.assertFalse(str(self.image2.thumbnail).encode() in response.content)


    def test_list_by_gallery(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/image/?gallery_id={0}'.format(self.gallery2.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(str(self.image.thumbnail).encode() in response.content)
        self.assertTrue(str(self.image2.thumbnail).encode() in response.content)


    def test_list_by_tagged_person(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/image/?person_id={0}'.format(self.person.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(self.image.thumbnail).encode() in response.content)
        self.assertFalse(str(self.image2.thumbnail).encode() in response.content)


    def test_retrieve_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/image/{0}/'.format(self.image.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_retrieve(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/image/{0}/'.format(self.image.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(self.image.thumbnail).encode() in response.content)


    def test_retrieve_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user2)
        url = '/api/image/{0}/'.format(self.image.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)