from django.core import mail
from django.template import loader
from django.test import TestCase
from my_auth.models import ConfirmedUser, CustomConfirmedUser


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


class TestCustomConfirmedUser(TestCase):
    
    def test_create_user_success(self):
        username = 'test'
        email = 'test@test.ru'
        password = 'testpassword123'
        user = CustomConfirmedUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.confirm)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_success(self):
        username = 'test'
        email = 'test@test.ru'
        password = 'testpassword123'
        user = CustomConfirmedUser.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.confirm)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_confirmed_manager(self):
        confirmed_user = user = CustomConfirmedUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            confim=True,
        )
        not_confirmed_user = user = CustomConfirmedUser.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        assertTrue(confirmed_user in ConfirmedUser.confirmed.all())
        assertTrue(not_confirmed_user not in ConfirmedUser.confirmed.all())