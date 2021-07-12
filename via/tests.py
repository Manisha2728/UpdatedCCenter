from django.test import TestCase
from django.test import Client
from authccenter.models.group import CCenterGroup
from security.models import ADProviders
from dbmconfigapp.models.tracking import LoginsHistory


# from django.models.admin import log

class CCenterLogInTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_offline_user(self):
        self.assertEqual(self.client.login(username='admin', password='123'), True)

    def test_login_offline_user_wrong_auth(self):
        self.assertEqual(self.client.login(username='admin', password='asdfksd'), False)

    # Eran M. 26.11.2019: removed the part from the tests checking login without domain when there only 1 Active directory provider.
    # Eran M. 15.01.2020: the AD group changed to CCenterTestGroup because the AD in dev2.local was removed.

    def ConfigureTestUserAccess(self):
        # ADProviders.objects.all().delete()
        # ADProviders.objects.create(domain_id=1, domain_name='dev2.local')

        """Mapping ccenter admin group to group of the test user"""
        ccneter_admins_group, _ = CCenterGroup.objects.get_or_create(name='ccenter_admins_group')
        ccneter_admins_group.adgroup_set.all().delete()
        ccneter_admins_group.adgroup_set.create(name='CCenterTestGroup')

    # Eran M. 26.11.2019: removed the part from the tests checking login without domain when there only 1 Active directory provider.
    # Eran M. 15.01.2020: AD user changed to RDQA5 because the AD in dev2.local was removed.
    def test_login_AD_user(self):
        self.ConfigureTestUserAccess()

        """Login without domain"""
        self.assertFalse(self.client.login(username='CCenterTestUser', password='1qaz@@wsx'))

        """Login using the DLN format"""
        self.assertFalse(self.client.login(username='DBMOTION\\RDQA5', password='wrongpass'))
        self.assertTrue(self.client.login(username='DBMOTION\\RDQA5', password='1qaz@@wsx'))

        """Login using the UPN format"""
        self.assertFalse(self.client.login(username='RDQA5@dbMotion.loc', password='wrongpass'))
        self.assertTrue(self.client.login(username='RDQA5@dbMotion.loc', password='1qaz@@wsx'))


    # Eran M. 26.11.2019: removed the part from the tests checking login without domain when there only 1 Active directory provider.
    # Eran M. 15.01.2020: AD user changed to RDQA5 because the AD in dev2.local was removed.
    def test_login_history_list(self):
        self.ConfigureTestUserAccess()

        """Initial count"""
        records_count = LoginsHistory.objects.count()

        """Login and logout with admin user"""
        self.assertTrue(self.client.login(username='admin', password='123'))
        self.assertEqual(LoginsHistory.objects.count() - records_count, 1)

        self.client.logout()
        self.assertEqual(LoginsHistory.objects.count() - records_count, 2)

        self.assertFalse(self.client.login(username='admin', password='asdfksd'))
        self.assertEqual(LoginsHistory.objects.count() - records_count, 3)

        """Login with DLN format"""
        self.assertTrue(self.client.login(username='DBMOTION\\RDQA5', password='1qaz@@wsx'))
        self.assertEqual(LoginsHistory.objects.count() - records_count, 4)

        self.client.logout()
        self.assertEqual(LoginsHistory.objects.count() - records_count, 5)

        # using of RDQA3 for failed login test to don't lock RDQA5
        self.assertFalse(self.client.login(username='DBMOTION\\RDQA3', password='wrongpass'))
        self.assertEqual(LoginsHistory.objects.count() - records_count, 6)

        """Login with UPN format"""
        self.assertTrue(self.client.login(username='RDQA5@dbMotion.loc', password='1qaz@@wsx'))
        self.assertEqual(LoginsHistory.objects.count() - records_count, 7)

        self.client.logout()
        self.assertEqual(LoginsHistory.objects.count() - records_count, 8)

        # using of RDQA3 for failed login test to don't lock RDQA5
        self.assertFalse(self.client.login(username='RDQA3@dbMotion.loc', password='wrongpass'))
        self.assertEqual(LoginsHistory.objects.count() - records_count, 9)

        """Login without domain"""
        self.assertFalse(self.client.login(username='RDQA5', password='1qaz@@wsx'))
        self.assertEqual(LoginsHistory.objects.count() - records_count, 10)

#   def test_tracking_list():
#       self.client.login(username='admin', password='123')
#       changesTableCount = log.objects.count()
#       self.client.post('/admin/dbmconfigapp/clinicaldomainallergies/1/', {'name':'save'}, follow=True)
#       self.assertNotEqual(log.objects.count(),changesTableCount)




