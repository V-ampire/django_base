from django.conf import settings
from django.core import mail
from my_auth.models import ConfirmedUser
from django.test import TestCase
from django.test import Client
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from my_auth.utils import get_temp_url_token
import time


class TestRegisterView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('my_auth:register')
        self.user_data = {
            'username': 'test_user',
            'email': 'test@mail.ru',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        self.user_invalid_data = {
            'username': 'test_user',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

    def test_valid_register_view(self):
        mail.outbox = []
        response = self.client.post(self.register_url, self.user_data)
        self.assertTrue(ConfirmedUser.objects.get(username=self.user_data['username']))
        self.assertFalse(ConfirmedUser.confirmed.filter(username=self.user_data['username']).exists())
        self.assertEqual(len(mail.outbox), 1)

    def test_invalid_register_view(self):
        mail.outbox = []
        response = self.client.post(self.register_url, self.user_invalid_data)
        self.assertFalse(ConfirmedUser.objects.filter(username=self.user_invalid_data['username']).exists())
        self.assertEqual(len(mail.outbox), 0)


class RegisterConfirmView(TestCase):

    def setUp(self):
        self.client = Client()
        self.confirmed_user = ConfirmedUser.objects.create(
            username='testuser1', password='testpass', email='test1@mail.ru', confirm=True
        )
        self.not_confirmed_user = ConfirmedUser.objects.create(
            username='testuser2', password='testpass', email='test2@mail.ru'
        )

    def test_success_user_confirm(self):
        token = get_temp_url_token(self.not_confirmed_user)
        res = self.client.get(reverse('my_auth:register_confirm', args=[token]))
        self.not_confirmed_user.refresh_from_db()
        self.assertTrue(self.not_confirmed_user.confirm)
        self.assertEqual(res.url, reverse('my_auth:register_confirm_done'))
    
    def test_expired_token(self):
        token = get_temp_url_token(self.not_confirmed_user)
        time.sleep(settings.REGISTER_TIMEOUT*2)
        res = self.client.get(reverse('my_auth:register_confirm', args=[token]))
        self.not_confirmed_user.refresh_from_db()
        self.assertFalse(self.not_confirmed_user.confirm)
        self.assertEqual(res.url, reverse('my_auth:register_confirm_fail'))

    def test_invalid_token(self):
        token = urlsafe_base64_encode(force_bytes('123abc'))
        res = self.client.get(reverse('my_auth:register_confirm', args=[token]))
        self.assertEqual(res.url, reverse('my_auth:register_confirm_fail'))