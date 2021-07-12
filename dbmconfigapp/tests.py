from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
import json
import os

from dbmconfigapp.export_logic import get_export_db_data, get_objects_table
from dbmconfigapp.models.base import *
from dbmconfigapp.models.cvtables import DataElement
from dbmconfigapp.utils import search

from django.contrib.admin.sites import AdminSite
from dbmconfigapp.models.tracking import *
from dbmconfigapp.admin.tracking import *

class CCenterTests(TestCase):
    
    def setUp(self):
        # log in to CCenter before running tests
        self.client.login(username='admin', password='123')
    
    # get all models except system ones      
    def get_custom_models(self):
        return ContentType.objects.exclude(app_label__in=['auth', 'contenttypes', 'sessions', 'sites', 'admin', 'south'])
    
    # test that export objects list contains all relevant models
    def test_export_data(self):
        
        # models that should not be exported/imported
        not_for_export = ['Component', 'ModelDescriptor', 'Service', 'SystemParameters', 'MigrationManager', 'VersionManager',
                          'EHRAgentCategoriesTopic', 'InitiateConnection', 'VpoEHRAgent',
                          'ADGroup', 'CCenterGroup', 'SettingsModel', 'CCenterUser', 'ChangesHistory', 'LoginsHistory',
                          'EHRAgentPastMedicalHistory', 'EhrAgentBaseUrl', 'EhrAgentHelp', 'EHRAgentCategoriesProperties', 
                          'EHRAgentTooltips', 
                          'EHRAgentBlinks','EHRAgentLabratory','EHRAgentMedication','AgentUserCentricApp',
						  ]
        
        empty_models = []
        missing_models = []
        # load json export data with export_logic methods
        json_data = json.loads(get_export_db_data(get_objects_table.keys(), True))
        
        for model in self.get_custom_models().exclude(model__in=not_for_export):
            model_class = model.model_class()
            # exclude models inherited from PageBaseModel and DataElement
            if model_class == None or PageBaseModel in inspect.getmro(model_class) or DataElement in inspect.getmro(model_class):
                continue
            # check if the model appears in json and if not check that model contains data
            # (if model table is empty we can't now either it was in export list or not)            
            model_name = str(model_class)
            if model_name not in json_data['meta']['models']:
                if model_class.objects.count() == 0:
                    empty_models.append(model_name)
                else:
                    missing_models.append(model_name)
        
        if(len(empty_models) > 0):
            print ('\nWarning! Export of following models can\'t be tested because they don\'t contain any data\n')          
            print ('\n'.join(sorted(empty_models)))
        
        self.assertEqual(len(missing_models), 0, '\nMissing models:\n' + '\n'.join(sorted(missing_models)))
        
        print ('\nTest export data success')
    
    # tests that search dictionary contains all relevant models    
    def test_search_missing_pages(self):

        not_for_search = ['ClinicalDomain', 'PatientSearchPage',]
        urls = []
        missing_pages = []
        
        for finfo in search.PAGES_INFO.values():
            for pinfo in finfo:
                urls.append(pinfo[1])

        for model in self.get_custom_models().exclude(model__in=not_for_search):
            
            model_class = model.model_class()
            # exclude models inherited from PageBaseModel
            if PageBaseModel in inspect.getmro(model_class):
                model_name = model_class.__name__
                is_missing = True
                
                for url in urls:
                    if '/' + model_name.lower() + '/' in url:
                        is_missing = False
                        continue
                    
                if is_missing:   
                    missing_pages.append(model_name)
         
        self.assertEqual(len(missing_pages), 0, '\nMissing pages:\n' + '\n'.join(sorted(missing_pages)))
        
        print ('\nTest search - missing pages success')
    
    # tests that search dictionary contains all html file names 
    # and that all files listed in search dictionary exist                
    def test_search_missing_files(self):
        from configcenter.settings import PROJECT_DIR
        ignored_files = []

        base_path = os.path.normpath(os.path.join(PROJECT_DIR, 'resources/html'))
        
        missing_files = [file_name for file_name in search.PAGES_INFO if not os.path.isfile(os.path.join(base_path, file_name))]     
        self.assertEqual(len(missing_files), 0, '\nMissing files in ' + base_path + ':\n' + '\n'.join(sorted(missing_files)))

        # I changed the filter to multiple stages so it easier to maintain it and it more readable.
        htm_files = filter(lambda file_name: file_name.endswith('.htm'), os.listdir(base_path)) # Retriving all the htm files.
        htm_files = filter(lambda file_name: file_name not in ignored_files, htm_files) # Ignoring marked htm files.
        missing_files_names = filter(lambda file_name: file_name not in search.PAGES_INFO, htm_files) # Filtering the files that not in the PAGES_INFO.

        #missing_files_names = [file_name for file_name in os.listdir(base_path) if file_name.endswith('.htm') and not file_name in search.PAGES_INFO]

        self.assertEqual(len(missing_files_names), 0, '\nMissing file names in PAGES_INFO dictionary:\n' + '\n'.join(sorted(missing_files_names)))
   
        print ('\nTest search - missing files success')
        
    # simple search test    
    def test_search_text(self):
  
        # search with expected result - found
        text_to_search = 'Clinical Documents'
        search_results, errors = search.go(text_to_search)
        
        self.assertEqual(len(errors), 0, 'There are errors when searching:\n' + '\n'.join(errors))
        self.assertNotEqual(len(search_results), 0, 'The string \"' + text_to_search + '\" was not found')
        
        # search with expected result - not found
        text_to_search = 'Search missing string'
        search_results, errors = search.go(text_to_search)
        self.assertEqual(len(search_results), 0, 'The string \"' + text_to_search + '\" was found when it should not be')
        
        print ('\nTest search simple page success')        
        
    # test that all requested pages return response status 200 - success     
    def test_pages_navigation(self):
        
        failed_urls = []
        
        for finfo in search.PAGES_INFO.values():
            for pinfo in finfo:
                response = self.client.get(pinfo[1])
                if response.status_code != 200:
                    failed_urls.append('\n' + pinfo[1] + ' - status code ' + str(response.status_code))
                    
        self.assertEqual(len(failed_urls), 0, '\nResponse status code of the following pages is wrong (not equal to 200):\n' + '\n'.join(sorted(failed_urls)))
        
        print ('\nTest pages navigation success')
        
    # tests that all relevant models have model descriptor defined    
    def test_model_descriptor(self):
        
        not_for_test = ['Component', 'dbFiles', 'Node', 'MigrationManager', 'VersionManager', 'ModelDescriptor', 'Partitioning', 'Service', 'SystemParameters', 'UsageReports',
                         'ADGroup', 'CCenterGroup', 'SettingsModel', 'CCenterUser', 'ChangesHistory', 'LoginsHistory', 'DataAccessAuditing', 'CAGDataAccessAuditing']
        missing_models = []
        
        descriptor_table_names = [row.model_name.lower() for row in ModelDescriptor.objects.all()]

        for model in self.get_custom_models().exclude(model__in=not_for_test):
            
            model_class = model.model_class()
            
            if PageBaseModel not in inspect.getmro(model_class) and DataElement not in inspect.getmro(model_class):
                
                if model_class._meta.db_table not in descriptor_table_names:
                    missing_models.append(model_class.__name__)
                    
        self.assertEqual(len(missing_models), 0, '\nFollowing models don\'t have model descriptor:\n' + '\n'.join(sorted(missing_models)))

        print ('\nTest model descriptor success')           
    
    # tests that __unicode__ or __str__ method of all models with more than one record does not return empty string
    # these methods used for history log
    def test_model_unicode(self): 
        
        not_for_test = ['SystemParameters', 'ClinicalDomainProperties', 'Vpo', 'VpoCommon', 'VpoEHRAgentDomains', 'VpoPPOL', 
                        'MyHROrganizationsEntity', 'PatientDetailsSectionOrdering','ParticipantListBasedPAAModel', 'OrderingFacilities']
        empty_unicode_models = []
        
        for model in self.get_custom_models().exclude(model__in=not_for_test):
            model_class = model.model_class()

            if model_class != None and ConfigurationEntityBaseModel in inspect.getmro(model_class): 

                if model_class.objects.count() > 1 and model_class.objects.all()[0].__unicode__() == '' and model_class.objects.all()[0].__str__() == '':
                    empty_unicode_models.append(model_class.__name__)

        self.assertEqual(len(empty_unicode_models), 0, '\nModels with empty __unicode__:\n' + '\n'.join(sorted(empty_unicode_models)))

        print ('\nTest model __unicode__ or __str__ method success')
        
class MockRequest:
    pass

class TrackingHistoryTests(TestCase):
    
    def setUp(self):
        self.map_test_ad_group()

    def test_changes_history_logging(self):
        from django.contrib.admin.options import get_content_type_for_model
        from dbmconfigapp.models.direct_messaging_acdm import DirectMessagingAcdm
        from dbmconfigapp.admin.direct_messaging_acdm import DirectMessagingAcdmAdmin
        from django.contrib.admin.models import CHANGE

        admin = DirectMessagingAcdmAdmin(DirectMessagingAcdm, AdminSite())
        mock_request = MockRequest()
        mock_request.user = User.objects.create(username='bill')
        obj = DirectMessagingAcdm(clientOid='clientOid_test', acdmCommunityName = 'acdmCommunityName_test')

        content_type = get_content_type_for_model(obj)

        admin.log_change(mock_request, obj, 'change_message_test')

        fetched = ChangesHistory.objects.filter(action_flag=CHANGE).latest('id')
        self.assertEqual(fetched.action_flag, CHANGE)
        self.assertEqual(fetched.content_type, content_type)
        self.assertEqual(fetched.object_id, str(obj.pk))
        self.assertEqual(fetched.user, mock_request.user)
        self.assertEqual(fetched.change_message, 'change_message_test')

        print ('\nTest changes history logging success')        

    def test_changes_history_user_fields(self):

        user = User.objects.create_superuser(username='super', email='', password='pass', first_name = 'first_name', last_name='last_name')
        user_pk = user.pk
        admin = ChangesHistoryAdmin(ChangesHistory, AdminSite())
        obj = ChangesHistory(None, None, user_id = user_pk)
        
        self.assertEqual(admin.user_to_dispay(obj).username, 'super')
        self.assertEqual(admin.user_name(obj), 'first_name last_name')

        print ('\nTest changes history user fields success')     
        
    def test_logins_history_logging(self):

        logins_before_test = LoginsHistory.objects.filter(action='Login').count()
        logouts_before_test = LoginsHistory.objects.filter(action='Logout').count()
        failures_before_test = LoginsHistory.objects.filter(action='Login failed').count()

        self.client.login(username='admin', password='123')
        self.client.logout()
        try:
            self.client.login(username='wrong_user', password='123')
        except:
            pass
        # self.client.login(username='CCenterTestUser@dev2.local', password='1qaz@@wsx')

        self.assertEqual(LoginsHistory.objects.filter(action='Login').count() - logins_before_test, 1)
        self.assertEqual(LoginsHistory.objects.filter(action='Logout').count() - logouts_before_test, 1)
        self.assertEqual(LoginsHistory.objects.filter(action='Login failed').count() - failures_before_test, 1)

        print ('\nTest logins history logging success')        

    def test_logins_history_export_csv(self):

        self.client.login(username='admin', password='123')
        self.client.logout()
        try:
            self.client.login(username='wrong_user', password='123')
        except:
            pass

        admin = LoginsHistoryAdmin(LoginsHistory, AdminSite())
        response = admin.export_csv(None, LoginsHistory.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Date/Time,Domain\\UserID,User Name,Action')
        self.assertContains(response, 'admin,,Login')
        self.assertContains(response, 'admin,,Logout')
        self.assertContains(response, 'wrong_user,,Login failed')

        print ('\nTest logins history export csv success')

    def map_test_ad_group(self):
        from security.models import ADProviders
        from authccenter.models.group import CCenterGroup

        ADProviders.objects.all().delete()
        ADProviders.objects.create(domain_id=1, domain_name='dev2.local')
        ccneter_admins_group, _ = CCenterGroup.objects.get_or_create(name='ccenter_admins_group')
        ccneter_admins_group.adgroup_set.all().delete()
        ccneter_admins_group.adgroup_set.create(name='CCenterTestGroup')

