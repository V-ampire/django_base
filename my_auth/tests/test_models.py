from django.core import mail
from django.template import loader
from django.test import TestCase
from my_auth.models import ConfirmedUser


def TestConfirmedUser(TestCase):

    def setUp(self):
        self.confirmed_user = ConfirmedUser.objects.create(
            username='testuser1', password='testpass', email='test1@mail.ru', confirm=True
        )
        self.not_confirmed_user = ConfirmedUser.objects.create(
            username='testuser2', password='testpass', email='test2@mail.ru'
        )

    def test_confirmed_manager(self):
        self.assertTrue(self.confirmed_user in ConfirmedUser.confirmed.all())
        self.assertTrue(self.not_confirmed_user not in ConfirmedUser.confirmed.all())

    def test_send_confirmation(self):
        mail.outbox = []
        domain = Site.objects.get_current().domain
        subject = loader.render_to_string(
            self.confirm_email_subject_template, {'domain': domain}
        )
        self.not_confirmed_user.send_confirmation()
        self.confirmed_user.send_confirmation()
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(len(mail.outbox), 1)
