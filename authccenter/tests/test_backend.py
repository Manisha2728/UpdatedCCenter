from django.test import TestCase

from authccenter.backends.ADAuthenticationBackend import Backend, active_directory_connection_establishment, \
    retrieve_user_information, user_active_directory_authentication
from authccenter.models.group import CCenterGroup
from security.models import ADProviders


class ADAuthenticationBackendTests(TestCase):
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

        conn, error = active_directory_connection_establishment(provider, self.usernameDLN, self.password)
        conn.unbind()
        self.assertIsNotNone(conn)
        self.assertIsNone(error)

        conn, error = active_directory_connection_establishment(provider, self.usernameUPN, self.password)
        conn.unbind()
        self.assertIsNotNone(conn)
        self.assertIsNone(error)

    def test_active_directory_connection_establishment_wrong_user_credentials(self):
        self.ConfigureTestUserAccess()
        provider = ADProviders.objects.get(domain_name='dev2.local')

        conn, error = active_directory_connection_establishment(provider, self.usernameDLN + 'a1234', self.password)
        self.assertIsNone(conn)
        self.assertIsNotNone(error)

        conn, error = active_directory_connection_establishment(provider, 'a1234' + self.usernameUPN, self.password)
        self.assertIsNone(conn)
        self.assertIsNotNone(error)

        conn, error = active_directory_connection_establishment(provider, self.usernameUPN, self.password + 'a1234')
        self.assertIsNone(conn)
        self.assertIsNotNone(error)

        conn, error = active_directory_connection_establishment(provider, self.usernameDLN, self.password + 'a1234')
        self.assertIsNone(conn)
        self.assertIsNotNone(error)

    def test_retrieve_user_information_ideal(self):
        self.ConfigureTestUserAccess()
        provider = ADProviders.objects.get(domain_name='dev2.local')

        conn, error = active_directory_connection_establishment(provider, self.usernameDLN, self.password)
        user, groups, error = retrieve_user_information(provider, conn, self.username)
        conn.unbind()

        self.assertIsNone(error)
        self.assertIsNotNone(groups)
        self.assertIsNotNone(user)

    def test_retrieve_user_information_group_name_not_match(self):
        ccneter_admins_group, _ = CCenterGroup.objects.get_or_create(name='ccenter_admins_group')
        ccneter_admins_group.adgroup_set.all().delete()
        ccneter_admins_group.adgroup_set.create(name='CCenterTestGroup1')
        ADProviders.objects.all().delete()
        provider = ADProviders.objects.create(domain_id=1, domain_name='dev2.local')

        conn, error = active_directory_connection_establishment(provider, self.usernameDLN, self.password)
        user, groups, error = retrieve_user_information(provider, conn, self.username)
        conn.unbind()

        self.assertIsNotNone(error)
        self.assertIsNone(groups)
        self.assertIsNone(user)

    def test_user_active_directory_authentication_ideal(self):
        self.ConfigureTestUserAccess()
        provider = ADProviders.objects.get(domain_name='dev2.local')

        user, error = user_active_directory_authentication(provider, self.usernameDLN, self.password)

        self.assertIsNotNone(user)
        self.assertIsNone(error)

    def test_user_active_directory_authentication_wrong_user_credentials(self):
        self.ConfigureTestUserAccess()
        provider = ADProviders.objects.get(domain_name='dev2.local')

        user, error = user_active_directory_authentication(provider, self.usernameDLN + 'a1', self.password)

        self.assertIsNotNone(error)
        self.assertIsNone(user)

        user, error = user_active_directory_authentication(provider, self.usernameDLN, self.password + 'a1')

        self.assertIsNotNone(error)
        self.assertIsNone(user)

        user, error = user_active_directory_authentication(provider, 'a1' + self.usernameUPN, self.password)

        self.assertIsNotNone(error)
        self.assertIsNone(user)

        user, error = user_active_directory_authentication(provider, self.usernameUPN, self.password + 'a1')

        self.assertIsNotNone(error)
        self.assertIsNone(user)

    def test_single_active_directory_provider_login_DLN_format(self):
        self.ConfigureTestUserAccess()
        provider = ADProviders.objects.get(domain_name='dev2.local')

        user, error = self.backend.single_active_directory_provider_login(provider, self.usernameDLN, self.password)

        self.assertIsNotNone(user)
        self.assertIsNone(error)

    def test_single_active_directory_provider_login_UPN_format(self):
        self.ConfigureTestUserAccess()
        provider = ADProviders.objects.get(domain_name='dev2.local')

        user, error = self.backend.single_active_directory_provider_login(provider, self.usernameUPN, self.password)

        self.assertIsNotNone(user)
        self.assertIsNone(error)

    def test_single_active_directory_provider_login_auto_complete(self):
        self.ConfigureTestUserAccess()
        provider = ADProviders.objects.get(domain_name='dev2.local')

        user, error = self.backend.single_active_directory_provider_login(provider, self.username, self.password)

        self.assertIsNotNone(user)
        self.assertIsNone(error)

    def test_first_stage_authentication_DLN_format(self):
        self.ConfigureTestUserAccess()
        user, error = self.backend.first_stage_authentication(self.usernameDLN, self.password)

        self.assertIsNone(user)
        self.assertIsNotNone(error)

    def test_first_stage_authentication_DLN_format_netbios_domain_name_matched(self):
        self.ConfigureTestUserAccess()
        defaults = {'netbios_domain_name': 'DEV2'}
        ADProviders.objects.update_or_create(domain_id=1, defaults=defaults)
        user, error = self.backend.first_stage_authentication(self.usernameDLN, self.password)

        self.assertIsNotNone(user)
        self.assertIsNone(error)

    def test_first_stage_authentication_UPN_format(self):
        self.ConfigureTestUserAccess()

        user, error = self.backend.first_stage_authentication(self.usernameUPN, self.password)

        self.assertIsNotNone(user)
        self.assertIsNone(error)

    def test_first_stage_authentication_unknown_format(self):
        self.ConfigureTestUserAccess()

        user, error = self.backend.first_stage_authentication(self.username, self.password)

        self.assertIsNone(user)
        self.assertIsNotNone(error)

    def test_second_stage_authentication_ideal(self):
        self.ConfigureTestUserAccess()
        user, error = self.backend.second_stage_authentication(self.usernameDLN, self.password)

        self.assertIsNotNone(user)
        self.assertIsNone(error)

    def test_second_stage_authentication_netbios_exists(self):
        self.ConfigureTestUserAccess()
        defaults = {'netbios_domain_name': 'a1234'}
        ADProviders.objects.update_or_create(domain_id=1, defaults=defaults)
        user, error = self.backend.second_stage_authentication(self.usernameDLN, self.password)

        self.assertIsNone(user)
        self.assertIsNotNone(error)

    def test_third_stage_authentication_ideal(self):
        self.ConfigureTestUserAccess()
        user, error = self.backend.third_stage_authentication(self.usernameDLN, self.password)

        self.assertIsNone(user)
        self.assertIsNotNone(error)

    def test_third_stage_authentication_netbios_not_matched(self):
        self.ConfigureTestUserAccess()
        defaults = {'netbios_domain_name': 'a1234'}
        ADProviders.objects.update_or_create(domain_id=1, defaults=defaults)
        user, error = self.backend.third_stage_authentication(self.usernameDLN, self.password)

        self.assertIsNotNone(user)
        self.assertIsNone(error)
