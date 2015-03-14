from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from ..models import Club
from ..views import ClubViewSet

class ClubViewSetTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1')
        self.user2 = User.objects.create_user('user2')
        self.client = APIClient()

        club = Club(
            owner=self.user1,
            name='my club',
            website='http://myclub.org/',
            description='This is my club.',
            location='Somewhere',
            latitude=5,
            longitude=6
        )
        club.save()
        self.club = club

    def test_list_clubs_works(self):
        response = self.client.get('/api/clubs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{
            'url': 'http://testserver/api/clubs/1/',
            'name': 'my club',
            'website': 'http://myclub.org/',
            'description': 'This is my club.',
            'location': 'Somewhere',
            'latitude': 5,
            'longitude': 6
        }])

    def test_list_clubs_only_shows_active_clubs(self):
        self.club.is_active = False
        self.club.save()
        response = self.client.get('/api/clubs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_patch_clubs_without_auth_fails(self):
        response = self.client.patch('/api/clubs/1/', {'name': 'u'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Club.objects.get(pk=1).name, 'my club')

    def test_patch_clubs_with_auth_from_non_owner_fails(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch('/api/clubs/1/', {'name': 'u'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Club.objects.get(pk=1).name, 'my club')

    def test_patch_clubs_with_auth_from_owner_works(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch('/api/clubs/1/', {'name': 'u'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Club.objects.get(pk=1).name, 'u')