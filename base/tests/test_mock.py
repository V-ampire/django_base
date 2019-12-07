from django.test import TestCase
from unittest.mock import Mock, patch

from base.bot import Bot


class TestMock(TestCase):
    def setUp(self):
        self.bot = Bot()

    def test_check_users_correct(self):
        with patch.object(self.bot, 'session') as s:
            s.get.return_value = [{'name': 'test'}]*10
            self.assertTrue(self.bot.check_users())

    def test_check_users_incorrect(self):
        with patch.object(self.bot, 'session') as s:
            s.get.return_value = [{'name': 'test'}]*8
            self.assertFalse(self.bot.check_users())
