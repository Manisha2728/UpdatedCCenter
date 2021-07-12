import datetime

from django.utils import timezone
from django.test import TestCase

from authccenter.models.user import CCenterUser


class CCenterUserModelTests(TestCase):

    def test_user_username(self):
        username = 'active test user'
        active_user = CCenterUser(username=username)
        self.assertEqual(active_user.username, username)
        self.assertEqual(active_user.get_username(), username)

    def test_user_active(self):
        active_user = CCenterUser(username='active test user')
        self.assertEqual(active_user.is_active, True)

    def test_user_not_active_past(self):
        inactive_user = CCenterUser(username='inactive test user past',
                                    last_login=timezone.now() - datetime.timedelta(days=1))
        self.assertFalse(inactive_user.is_active)

    def test_user_not_active_future(self):
        inactive_user_fature = CCenterUser(username='inactive test user future',
                                           date_joined=timezone.now() + datetime.timedelta(days=1))
        self.assertEqual(inactive_user_fature.is_active, False)

    def test_user_authenticated(self):
        active_user = CCenterUser(username='authenticated test user')
        self.assertEqual(active_user.is_authenticated(), True)

    def test_user_not_authenticated_past(self):
        inactive_user = CCenterUser(username='not authenticated test user past',
                                    last_login=timezone.now() - datetime.timedelta(days=1))
        self.assertEqual(inactive_user.is_authenticated(), False)

    def test_user_not_authenticated_future(self):
        inactive_user_fature = CCenterUser(username='not authenticated test user future',
                                           date_joined=timezone.now() + datetime.timedelta(days=1))
        self.assertEqual(inactive_user_fature.is_authenticated(), False)
