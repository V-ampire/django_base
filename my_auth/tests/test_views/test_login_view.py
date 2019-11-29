from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from my_auth.models import TemporaryBanIP


# class TestMyLoginView(TestCase):

#     def setUp(self):
#         self.test_client_ip = '127.0.0.1'
#         self.client = Client(REMOTE_ADDR=self.test_client_ip)
#         self.user = User.objects.create(username='test_user', password='testpass')
#         self.login_url = reverse('my_auth:login')
#         self.index_url = reverse('base:index')
#         self.invalid_params = {
#             'username': 'invalid_user',
#             'password': 'invalid_pass',
#         }

#     def test_get_login_template(self):
#         response = self.client.get(self.login_url)
#         self.assertTrue('csrf_token' in response.context.keys())
#         self.assertTrue('form' in response.context.keys())
#         self.assertTrue('my_auth/login.html' in [tmpl.name for tmpl in response.templates])

#     def test_redirect_authenticated_user(self):
#         self.client.force_login(self.user)
#         response = self.client.get(self.login_url)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL)

#     def test_15_min_block(self):
#         for attempt in range(settings.AUTH_ATTEMPTS['15_MINUTES_BLOCK']):
#             self.client.post(self.login_url, self.invalid_params)
#         post = self.client.post(self.login_url, self.invalid_params)
#         get = self.client.post(self.login_url)
#         self.assertTrue('my_auth/block_15_minutes.html' in [tmpl.name for tmpl in post.templates])
#         self.assertTrue('my_auth/block_15_minutes.html' in [tmpl.name for tmpl in get.templates])

#     def test_24_hours_block(self):
#         TemporaryBanIP.objects.create(
#             ip_address=self.test_client_ip,
#             attempts=settings.AUTH_ATTEMPTS['24_HOURS_BLOCK']-1,
#             time_unblock=timezone.now(),
#         )
#         # При следующем запросе будет бан
#         self.client.post(self.login_url, self.invalid_params)
#         # Тут уже страница бана
#         post = self.client.post(self.login_url, self.invalid_params)
#         get = self.client.post(self.login_url)
#         self.assertTrue('my_auth/block_24_hours.html' in [tmpl.name for tmpl in post.templates])
#         self.assertTrue('my_auth/block_24_hours.html' in [tmpl.name for tmpl in get.templates])
