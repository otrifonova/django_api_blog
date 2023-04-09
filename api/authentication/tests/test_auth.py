from urllib.parse import urljoin
from django.test import TestCase
from rest_framework.test import APIClient


# smoke tests only as djoser and simplejwt is used
class UserAuthenticationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = '/api/auth/'
        cls.user_data = {"username": "test_user",
                         "password": "te$tPswd"}
        cls.client = APIClient()
        cls.response = cls.client.post(cls.url, cls.user_data)
        cls.refresh_token = cls.client.post(
            urljoin(cls.url, 'token/'),
            cls.user_data
        ).json()['refresh']

    @classmethod
    def tearDownClass(cls):
        pass

    def test_sign_up(self):
        self.assertEqual(self.response.status_code, 201)

    def test_login(self):
        url = urljoin(self.url, 'token/')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, 200)

    def test_token_refresh(self):
        url = urljoin(self.url, 'token/refresh/')
        response = self.client.post(url,
                                    {'refresh': self.refresh_token})
        self.assertEqual(response.status_code, 200)
