from django.test import TestCase, Client
from django.contrib.auth import get_user_model

user = get_user_model()


# Create your tests here.

class UsersTestCase(TestCase):

    def setUp(self):
        user.objects.create_user("test", "test", "test")
        self.user = user.objects.get(username="test")
        self.client = Client()

    def test_user_creation(self):
        user = self.user
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.groups.count(), 0)
        self.assertEqual(user.user_permissions.count(), 0)

    def test_user_login(self):
        response = self.client.post('/users/login/', {'username': 'test', 'password': 'test'}, follow=True)
        self.assertEqual(response.content, b"Hello test. You're at the users index.")

