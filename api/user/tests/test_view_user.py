from django.test import TestCase
from rest_framework.test import APIClient

from core.models import User, Post


class ViewUserTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = '/api/user/'

        cls.user_1 = User.objects.create_user(username="test_user_user_1")
        cls.user_2 = User.objects.create_user(username="test_user_user_2")
        cls.user_3 = User.objects.create_user(username="test_user_user_3")
        cls.user_4 = User.objects.create_user(username="test_user_user_4")

        for i in range(1):
            Post.objects.create(title="TextTitle", text="TestText", author=cls.user_3)

        for i in range(2):
            Post.objects.create(title="TextTitle", text="TestText", author=cls.user_1)

        for i in range(3):
            Post.objects.create(title="TextTitle", text="TestText", author=cls.user_4)

        for i in range(4):
            Post.objects.create(title="TextTitle", text="TestText", author=cls.user_2)

        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_view_all_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_all_users_sorted_by_number_of_posts_desc(self):
        response = self.client.get(self.url, {"sorting": "posts_desc"})
        is_sorted = True
        number_of_posts = []
        for user in response.json():
            number_of_posts.append(user['number_of_posts'])
        for i in range(len(number_of_posts) - 1):
            if number_of_posts[i] < number_of_posts[i + 1]:
                is_sorted = False
                break
        self.assertTrue(is_sorted)

    def test_view_all_users_sorted_by_number_of_posts_asc(self):
        response = self.client.get(self.url, {"sorting": "posts_asc"})
        is_sorted = True
        number_of_posts = []
        for user in response.json():
            number_of_posts.append(user['number_of_posts'])
        for i in range(len(number_of_posts) - 1):
            if number_of_posts[i] > number_of_posts[i + 1]:
                is_sorted = False
                break
        self.assertTrue(is_sorted)
