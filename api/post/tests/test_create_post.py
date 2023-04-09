from django.test import TestCase
from rest_framework.test import APIClient

from core.models import User, Post


class CreatePostTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = '/api/post/'
        cls.token_url = '/api/auth/token/'

        cls.user_data = {"username": "test_user_post",
                         "password": "te$tPswd"}

        cls.valid_post_data = {'title': "TextTitle", 'text': "TestText"}
        cls.invalid_post_data = {}
        cls.invalid_post_json_response = {"title": ["This field is required."],
                                          "text": ["This field is required."]}

        cls.user = User.objects.create_user(username=cls.user_data['username'],
                                            password=cls.user_data['password'])
        cls.client = APIClient()
        cls.token = cls.client.post(
            cls.token_url,
            cls.user_data
        ).json()['access']

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_valid_post_unauthorized(self):
        response = self.client.post(self.url, self.valid_post_data)
        self.assertEqual(response.status_code, 401)

    def test_create_valid_post_authorized(self):
        response = self.client.post(self.url,
                                    self.valid_post_data,
                                    headers={'Authorization': " " .join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['author_id'], self.user.id)

    def test_create_invalid_post_authorized(self):
        response = self.client.post(self.url,
                                    self.invalid_post_data,
                                    headers={'Authorization': " " .join(["Bearer ", self.token])})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), self.invalid_post_json_response)
