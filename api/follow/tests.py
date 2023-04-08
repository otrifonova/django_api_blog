from urllib.parse import urljoin
from django.test import TestCase
from rest_framework.test import APIClient

from core.models import User, Follow


class FollowUnfollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url_to_follow = '/api/follow/'
        cls.url_to_unfollow = '/api/unfollow/'
        cls.token_url = '/api/auth/token/'

        cls.user_auth_data = {"username": "TestUser1",
                              "password": "te$tPswd"}
        cls.user_does_not_exist_id = 0

        cls.user_auth = User.objects.create_user(username=cls.user_auth_data['username'],
                                                 password=cls.user_auth_data['password'])
        cls.user_followed = User.objects.create_user(username='TestUser2')
        cls.user_to_follow = User.objects.create_user(username='TestUser3')
        cls.user_not_followed = User.objects.create_user(username='TestUser4')
        Follow.objects.create(from_user=cls.user_auth, to_user=cls.user_followed)

        cls.client = APIClient()
        cls.token = cls.client.post(
            cls.token_url,
            cls.user_auth_data
        ).json()['access']

    @classmethod
    def tearDownClass(cls):
        pass

    def test_follow_self_authorized(self):
        response = self.client.post(urljoin(self.url_to_follow, f'{self.user_auth.id}/'),
                                    headers={'Authorization': " ".join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'message': 'Cannot follow yourself.'})

    def test_follow_followed_authorized(self):
        response = self.client.post(urljoin(self.url_to_follow, f'{self.user_followed.id}/'),
                                    headers={'Authorization': " ".join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'message': f'User with id {self.user_followed.id} is already followed.'})

    def test_follow_not_followed_authorized(self):
        response = self.client.post(urljoin(self.url_to_follow, f'{self.user_to_follow.id}/'),
                                    headers={'Authorization': " ".join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['from_user'], self.user_auth.id)
        self.assertEqual(response.json()['to_user'], self.user_to_follow.id)

    def test_follow_user_does_not_exist_authorized(self):
        response = self.client.post(urljoin(self.url_to_follow, f'{self.user_does_not_exist_id}/'),
                                    headers={'Authorization': " ".join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 404)

    def test_follow_user_exists_unauthorized(self):
        response = self.client.post(urljoin(self.url_to_follow, f'{self.user_not_followed.id}/'))
        self.assertEqual(response.status_code, 401)

    def test_follow_user_does_not_exist_unauthorized(self):
        response = self.client.post(urljoin(self.url_to_follow, f'{self.user_does_not_exist_id}/'))
        self.assertEqual(response.status_code, 401)

    def test_unfollow_self_authorized(self):
        response = self.client.post(urljoin(self.url_to_unfollow, f'{self.user_auth.id}/'),
                                    headers={'Authorization': " ".join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'message': 'Cannot unfollow yourself.'})

    def test_unfollow_followed_authorized(self):
        response = self.client.post(urljoin(self.url_to_unfollow, f'{self.user_followed.id}/'),
                                    headers={'Authorization': " ".join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.headers['Content-Length'], '0')

    def test_unfollow_not_followed_authorized(self):
        response = self.client.post(urljoin(self.url_to_unfollow, f'{self.user_not_followed.id}/'),
                                    headers={'Authorization': " ".join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'message': f'User with id {self.user_not_followed.id} is already not followed.'})

    def test_unfollow_user_does_not_exist_authorized(self):
        response = self.client.post(urljoin(self.url_to_unfollow, f'{self.user_does_not_exist_id}/'),
                                    headers={'Authorization': " ".join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 404)

    def test_unfollow_user_exists_unauthorized(self):
        response = self.client.post(urljoin(self.url_to_unfollow, f'{self.user_not_followed.id}/'))
        self.assertEqual(response.status_code, 401)

    def test_unfollow_user_does_not_exist_unauthorized(self):
        response = self.client.post(urljoin(self.url_to_unfollow, f'{self.user_does_not_exist_id}/'))
        self.assertEqual(response.status_code, 401)
