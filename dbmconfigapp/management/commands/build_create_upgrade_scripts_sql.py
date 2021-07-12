from django.core.management.base import BaseCommand, CommandError
import os.path
from configcenter import settings
from dbmconfigapp.models.base import *
from dbmconfigapp.models.cvtables import DataElement

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):        
        try:
            folder_path = os.path.join(settings.PROJECT_DIR, 'dbmconfigapp','sql', 'upgrade_scripts')
            template_file_path = os.path.join(folder_path, 'create_upgrade_scripts_template.sql')
            result_file_path = os.path.join(folder_path, 'create_ccenter_upgrade_scripts.sql')

            with open(template_file_path, "r") as template_file:
                template = template_file.read()

            with open(result_file_path, "w") as result_file:
                result_file.write(template.replace('$INSERT_TABLE_FIELDS_METADATA$', self.get_models_metadata()))
                self.stdout.write('Successfully saved file "{0}"'.format(result_file_path))
        except Exception as e:
            raise CommandError('Build "{0}" failed with error: {1}'.format(result_file_path, e))

    def get_models_metadata(self):
        selects = []
        models_to_update = self.get_merge_models()

        for model in self.get_relevent_models():
            table_name = model._meta.db_table

            for field in model._meta.fields:
                field_name = field.get_attname_column()[0]
                # we don't need fields from parent model (inherits from django LogEntry)
                #if(table_name == 'dbmconfigapp_changeshistory' and field_name not in ('logentry_ptr_id', 'ccenter_user_id')):
                #    continue
                if(table_name == 'dbmconfigapp_agentpphostedapp' and field_name=='id'):
                    continue

                default = field.get_default()
                if default == None:
                    default = 'NULL'
                else: 
                    default = "'{}'".format(default)

                if(table_name == 'federation_node' and field_name == 'uid'):
                    default = "'''+ cast([id] as varchar(1000))+'''"
                if(table_name == 'dbmconfigapp_appspatientdisplayvbp' and field_name == 'vbp_display_name_long'):
                    default = "'''+ cast([vbp_display_name] as varchar(1000))+'''"

                readonly_fields=[]
                is_key = "NULL"
                if(table_name in models_to_update.keys()):
                    key_fields = models_to_update[table_name][0]
                    readonly_fields = models_to_update[table_name][1]
                    if (field_name in key_fields):
                        is_key = 1

                if (field_name not in readonly_fields):
                    insert_string = "INSERT INTO #TableFieldsMetadata\nSELECT '{}', '{}', {}, {}".format(table_name, field_name, default, is_key)    
                    selects.append(insert_string)

        return '\n'.join(sorted(selects))

    def get_pages(self):
        from django.db.models import get_app, get_models
        models = get_models(include_auto_created=True)
        table_names = [model._meta.db_table + '                    ' + model.__name__ + ',' for model in models  
                    if PageBaseModel in inspect.getmro(model)]
        print ('\n'.join(sorted(table_names)))
        return

    def get_merge_models(self):
        models_to_merge = {
        #'dbmconfigapp_agentpphostedapp': 
        #    [['app_name',], ['get_application_state_url', 'launch_url', 'app_key']], #update and insert?
        'dbmconfigapp_appsadvancedirectivenodes': 
            [['id',], ['cv_parent_id', 'ehragent_parent_id', 
                       'pl_parent_id', 'pv_parent_patient_display_id',]],
        'dbmconfigapp_clinicalcodedisplay': 
            [['business_aspect', 'business_table', 'code_name'], []],  #if display_as contains 'Preferred' and 'Baseline' and 'Local'and 'Text' 
        'dbmconfigapp_ccdadisplay': 
            [['id',], ['cv_parent_id', 'dataexport_parent_id', 'ehragent_parent_id', 'pv_parent_id', 
                       'CCDA_export_continuity_of_care_document', 'CCDA_export_discharge_summary',
                       'CCDA_export_referral_notes', 'CCDA_export_unstructured_document']],
        'dbmconfigapp_clinicaldomainproperties':
            [['clinical_domain_id',], ['help_1', 'help_2', 'help_3', 'pl_parent_id', 'pv_parent_patient_display_id', 
                                       'pv_ClinicalDocument_ShowExternalDocumentsLabel_id']],
        'dbmconfigapp_dataelement': 
            [['id',], ['clinical_domain_id', 'default_width', 'default_report_width', 
                       'clinical_view_name', 'report_field_name', 'grid_name', 'report_name', 
                       'pl_parent_id', 'pv_parent_patient_display_id',]],
        'dbmconfigapp_ehragentcvcommonclinicaldomainsproperties': 
            [['id',], ['ehragent_parent_id', 'cv_parent_id', 'name', 'display_name', 'default_time_range']],
        'dbmconfigapp_patientsearchdisplayoptions': [['id',], ['patient_search_page_id', 'pv_patient_search_page_id']],
        'dbmconfigapp_vitalsinpatientmeasurement': 
            [['id',], ['ehragent_parent_id', 'cv_vital_parent_id', 'pv_parent_id',]],
        'dbmconfigapp_vpo': [['id',], []],
        'dbmconfigapp_vpofacilitydisplay': 
            [['id',], ['display_name', 'clinical_domain_id', 'parent_cv_general_id', 
                       'parent_ehragent_general_id', 'pl_parent_id', 'patient_view_id',]],
        'dbmconfigapp_vpoppol': 
            [['id',], ['cv_patient_display_id', 'clinical_domain_id', 'ehragent_patient_display_id', 
                       'pl_patient_display_id', 'pv_patient_display_id', 'pv_parent_patient_display_id']],
        }
        return models_to_merge

    def get_relevent_models(self):
        from django.db.models import get_app, get_models

        not_relevent_models = [		
		'auth_permission',
        'auth_user_user_permissions',
		'authccenter_ccentergroup',
		'authccenter_ccentergroup_permissions',
		'authccenter_ccenteruser',
		'authccenter_ccenteruser_groups',
		'authccenter_settingsmodel',
		'ccenter_migration_manager',
		'dbmconfigapp_culture',
        'dbmconfigapp_ehragentbaseurl',
		'dbmconfigapp_migrationmanager',
		'dbmconfigapp_modeldescriptor',
		'dbmconfigapp_systemparameters',
		'dbmconfigapp_versionmanager',
        # not in use or not editable
        'dbmconfigapp_agentusercentricapp',
        'dbmconfigapp_ehragenttooltips',
        'dbmconfigapp_ehragentcategoriesproperties',
        'dbmconfigapp_ehragentcategoriestopic',
        'dbmconfigapp_ehragentlabratory',
        'dbmconfigapp_ehragentmedication',
        'dbmconfigapp_ehragentpastmedicalhistory',
        'dbmconfigapp_vpoehragent',
        'dbmconfigapp_changeshistory',
        # special cases
        'dbmconfigapp_dbfiles', # don't delete table, add not existing rows
        ]

        models = get_models(include_auto_created=True)
        models = [model for model in models  
                  if not PageBaseModel in inspect.getmro(model) 
                      and (model is DataElement or (DataElement not in inspect.getmro(model)))
                      and model._meta.db_table not in not_relevent_models 
                      #and (model._meta.db_table=='django_admin_log' or ('django_' not in model._meta.db_table))
                      and 'django_' not in model._meta.db_table
                      and '_component' not in model._meta.db_table
                      and '_service' not in model._meta.db_table]
    
        return models

