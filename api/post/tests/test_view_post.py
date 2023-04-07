from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIClient

from core.models import User, Post


class UserAuthenticationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = '/api/post/'

        cls.user_1 = User.objects.create_user(username="user_1")
        cls.user_2 = User.objects.create_user(username="user_2")

        Post.objects.create(title="TextTitle1", text="TestText1", author=cls.user_1)
        Post.objects.create(title="TextTitle11", text="TestText11", author=cls.user_1)
        Post.objects.create(title="TextTitle111", text="TestText111", author=cls.user_1)
        Post.objects.create(title="TextTitle2", text="TestText2", author=cls.user_2)

        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_view_all_posts(self):
        response = self.client.get(self.url)
        posts_amount = len(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(posts_amount, 4)

    def test_view_all_posts_sorted_by_date_desc(self):
        response = self.client.get(self.url)
        is_sorted = True
        dates = []
        for post in response.json():
            date = datetime.strptime(post['pub_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            dates.append(date)
        for i in range(len(dates) - 1):
            if dates[i] < dates[i + 1]:
                is_sorted = False
                break
        self.assertTrue(is_sorted)

    def test_view_posts_by_author(self):
        author_id = self.user_1.id
        response = self.client.get(self.url, {'author_id': f'{author_id}'})
        posts_amount = len(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(posts_amount, 3)

    def test_view_posts_by_author_sorted_by_date_desc(self):
        author_id = self.user_1.id
        response = self.client.get(self.url, {'author_id': f'{author_id}'})
        is_sorted = True
        dates = []
        for post in response.json():
            date = datetime.strptime(post['pub_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            dates.append(date)
        for i in range(len(dates) - 1):
            if dates[i] < dates[i + 1]:
                is_sorted = False
                break
        self.assertTrue(is_sorted)
