from django.test import TestCase, override_settings, RequestFactory, Client
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.shortcuts import reverse
from .models import CustomUrl
from .views import add_url
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


def create_custom_url(dest_url, short_url, owner=None):
<<<<<<< HEAD
<<<<<<< Updated upstream
    return CustomUrl.objects.create(owner=owner, destination_url=dest_url, short_url=short_url)
=======
    return CustomUrl.objects.create(owner=owner, source_url=dest_url, short_url=short_url, expiration_date=timezone.now() + datetime.timedelta(days=30))
>>>>>>> Stashed changes
=======
    return CustomUrl.objects.create(owner=owner, source_url=dest_url, short_url=short_url)
>>>>>>> master


class CustomUrlModelTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='testb@test.com', password='password')

    def test_right_custom_url_redirection(self):
        """
        basedomain/[short_url] should redirect to appropiate
        destination url
        """
        cu = create_custom_url("https://www.google.com", "google")
        response = self.client.get(
            reverse('redirection_url', args=("google",)))
        self.assertRedirects(response, cu.source_url,
                             fetch_redirect_response=False)

    def test_add_url(self):
        """
        post appropriate data to /urls/add must create custom url instance
        """
        request = self.factory.post(reverse('add_url'), {
                                    'source_url': 'https://www.google.com', 'short_url': 'google', 'time': ''})
        request.user = self.user
        request.session = SessionStore()
        request.session.create()
        response = add_url(request)
        response.client = Client()
        self.assertRedirects(response, reverse(
            'user_urls'), fetch_redirect_response=False)
        cu = CustomUrl.objects.get(owner__username='test')
        self.assertIsNot(cu, None)
        self.assertEqual(cu.source_url, 'https://www.google.com')
