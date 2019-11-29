from django.test import TestCase
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import time
from my_auth.models import ConfirmedUser
from my_auth.utils import get_temp_url_token, check_temp_url_token


class TestGetTempUrlToken(TestCase):
    
    def setUp(self):
        self.user = ConfirmedUser.objects.create(username='testuser', password='testpass', email='test@mail.ru')

    def test_check_temp_url_token_valid(self):
        seconds = 3
        token = get_temp_url_token(self.user)
        time.sleep(seconds/2)
        self.assertEqual(check_temp_url_token(token), self.user.username)
    
    def test_check_temp_url_token_expired(self):
        seconds = 3
        token = get_temp_url_token(self.user)
        time.sleep(seconds*2)
        self.assertFalse(check_temp_url_token(token, seconds=seconds))

    def test_bad_signature(self):
        seconds=3
        self.assertFalse(check_temp_url_token('', seconds=seconds))
        token = urlsafe_base64_encode(force_bytes('123abc'))
        self.assertFalse(check_temp_url_token(token, seconds=seconds))