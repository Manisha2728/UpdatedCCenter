from django.contrib.auth.models import Group, User
from django.test import Client, TestCase

from authccenter.models.group import CCenterGroup
from authccenter.models.settings import SettingsModel
from authccenter.views import DisableCCenterLogin
from security.models import ADProviders


class CCenterViewsTests(TestCase):

    def ConfigureTestUserAccess(self):
        ADProviders.objects.all().delete()
        ADProviders.objects.create(domain_id=1, domain_name='dev2.local')
        ccneter_admins_group, _ = CCenterGroup.objects.get_or_create(name='ccenter_admins_group')
        ccneter_admins_group.adgroup_set.all().delete()
        ccneter_admins_group.adgroup_set.create(name='CCenterTestGroup')
        usernameDLN = 'DEV2\\CCenterTestUser'
        usernameUPN = 'CCenterTestUser@dev2.local'
        password = '1qaz@@wsx'

    def test_hide_switch_to_ad_only_link(self):
        User.objects.create_user('testing', '', 'testing')
        c = Client()
        c.login(username='testing', password='testing')
        response_of_user = c.get('/welcome/')
        c.logout()
        self.assertTrue('<li><a class="" href="/authccenter/">Switch to Login with AD only</a></li>' in
                        response_of_user.content)
        self.assertTrue('<li><a class="" href="/admin/auth/">Manage Users</a></li>' in
                        response_of_user.content)
        self.ConfigureTestUserAccess()
        c.login(username='DEV2\\CCenterTestUser', password='1qaz@@wsx')
        response_of_active_directory_user = c.get('/welcome/')
        c.logout()

        self.assertTrue('<li><a class="" href="/authccenter/">Switch to Login with AD only</a></li>' not in
                        response_of_active_directory_user.content)
        self.assertTrue('<li><a class="" href="/admin/auth/">Manage Users</a></li>' not in
                        response_of_active_directory_user.content)

    def test_remove_offline_users(self):
        User.objects.all().delete()
        User.objects.create_superuser('admin', '','123')
        User.objects.create_superuser('superuser1', '','superuser1')
        User.objects.create_superuser('superuser2', '','superuser2')
        User.objects.create_user('user1', '','user1')
        User.objects.create_user('user2', '','user2')

        Group.objects.create(name='group1')
        Group.objects.create(name='group2')
        Group.objects.create(name='group3')

        SettingsModel.objects.all().delete()

        settings = SettingsModel.objects.setting()

        self.assertFalse(settings.active_directory_mode)
        DisableCCenterLogin(None)
        self.assertFalse(User.objects.filter(is_active=True).exists())
        self.assertTrue(SettingsModel.objects.setting().active_directory_mode)

