from django.test import TestCase
from django.contrib import auth

User = auth.get_user_model()

from .. import models

class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='a@b.com')
        user.full_clean()  # should not raise

    def test_is_authenticated(self):
        user = User()
        self.assertTrue(user.is_authenticated)

    def test_email_is_primary_key(self):
        user = User()
        self.assertFalse(hasattr(user, 'id'))

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='edith@example.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)  # should not raise

class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token1 = models.Token.objects.create(email='a@b.com')
        token2 = models.Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)
