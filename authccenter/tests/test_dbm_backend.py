from django.test import TestCase

from authccenter.backends.dbmAuthenticationBackend import Backend
from authccenter.models.group import CCenterGroup
from security.models import ADProviders


class dbmAuthenticationBackendTests(TestCase):
    def ConfigureTestUserAccess(self):
        ADProviders.objects.all().delete()
        ADProviders.objects.create(domain_id=1, domain_name='dev2.local')
        ccneter_admins_group, _ = CCenterGroup.objects.get_or_create(name='ccenter_admins_group')
        ccneter_admins_group.adgroup_set.all().delete()
        ccneter_admins_group.adgroup_set.create(name='CCenterTestGroup')

    def setUp(self):
        self.backend = Backend()
        self.username = 'CCenterTestUser'
        self.usernameDLN = 'DEV2\\CCenterTestUser'
        self.usernameUPN = 'CCenterTestUser@dev2.local'
        self.password = '1qaz@@wsx'
        self.group_name = 'CCenterTestGroup'

    def test_active_directory_connection_establishment_ideal(self):
        self.ConfigureTestUserAccess()
        provider = ADProviders.objects.get(domain_name='dev2.local')

        conn, error = self.backend.active_directory_connection_establishment(provider, self.usernameDLN, self.password)
        if(conn):
            conn.unbind()

        self.assertIsNotNone(conn)
        self.assertIsNone(error)

        conn, error = self.backend.active_directory_connection_establishment(provider, self.usernameUPN, self.password)
        if(conn):
            conn.unbind()
        self.assertIsNotNone(conn)
        self.assertIsNone(error)

    def test_active_directory_connection_establishment_wrong_user_credentials(self):
        self.ConfigureTestUserAccess()
        provider = ADProviders.objects.get(domain_name='dev2.local')

        conn, error = self.backend.active_directory_connection_establishment(provider, self.usernameDLN + 'a1234', self.password)
        self.assertIsNone(conn)
        self.assertIsNotNone(error)

        conn, error = self.backend.active_directory_connection_establishment(provider, 'a1234' + self.usernameUPN, self.password)
        self.assertIsNone(conn)
        self.assertIsNotNone(error)

        conn, error = self.backend.active_directory_connection_establishment(provider, self.usernameUPN, self.password + 'a1234')
        self.assertIsNone(conn)
        self.assertIsNotNone(error)

        conn, error = self.backend.active_directory_connection_establishment(provider, self.usernameDLN, self.password + 'a1234')
        self.assertIsNone(conn)
        self.assertIsNotNone(error)

    def test_user_authentication_ideal(self):
        self.ConfigureTestUserAccess()

        user = self.backend.authenticate(self.usernameDLN, self.password)

        self.assertIsNotNone(user)

    def test_user_authentication_wrong_user_credentials(self):
        self.ConfigureTestUserAccess()

        user = self.backend.authenticate(self.usernameDLN + 'a1', self.password)
        self.assertIsNone(user)

        user = self.backend.authenticate(self.usernameDLN, self.password + 'a1')
        self.assertIsNone(user)

        user = self.backend.authenticate('a1' + self.usernameUPN, self.password)
        self.assertIsNone(user)

        user = self.backend.authenticate(self.usernameUPN, self.password + 'a1')
        self.assertIsNone(user)
