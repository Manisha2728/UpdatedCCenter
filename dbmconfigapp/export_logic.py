import sys
from django.contrib.admin.models import CHANGE
from dbmconfigapp.models.apps_patient_display import AppsPatientDisplay, AppsPatientDisplayVBP
from dbmconfigapp.models.apps_patient_display import AppsPatientDisplayWithAgent, AppsPatientDisplayCommon, AppsPatientDisplayAgeCalculation, AppsPatientDisplayMetricCodeBasedIndicator,PvPatientNameDisplay, AppsPatientDisplayValueBaseProgram, AppsAdvanceDirectiveNodes
from dbmconfigapp.models.apps_reporting import AppsReporting
from dbmconfigapp.models.collaborate_patient_search import CollaboratePatientSearchProperties, PatientSearchHistoryDataElement, PatientSearchDisplayOptions, \
    PatientSearchPage, PatientSearchDefaultSearch
from dbmconfigapp.models.cvtables import DataElement, GridDataElement, FindingDataElement, DocumentDataElement, \
    ImagingPacs, ImagingPacsParameter, DiagnosisDataElement, AllergiesDataElement, MedicationsDataElement, ProblemsDataElement, \
    LabsDataElement
from dbmconfigapp.models.cvtables import ClinicalDomainProperties
from dbmconfigapp.models.ppol_general import PpolGeneral
from dbmconfigapp.models.direct_messaging_acdm import DirectMessagingAcdm, DirectMessagingAcdmPage
from dbmconfigapp.models.clinical_domain_laboratory import LabChartDisplayOptions
from dbmconfigapp.models.db_files import DbFiles
from dbmconfigapp.models.clinical_code_display import PVClinicalCodeDisplayPage
from django.core import serializers
import json
import datetime
import logging

from dbmconfigapp.models.cvtables import ClinicalDomainDemographics
from dbmconfigapp.models.cvtables import ClinicalDomainPlv
from dbmconfigapp.models.cvtables import ClinicalDomainAllergies
from dbmconfigapp.models.cvtables import ClinicalDomainProblems
from dbmconfigapp.models.cvtables import ClinicalDomainImmunizations
from dbmconfigapp.models.cvtables import ClinicalDomainVitals
from dbmconfigapp.models.cvtables import ClinicalDomainMedications
from dbmconfigapp.models.cvtables import ClinicalDomainPathologies
from dbmconfigapp.models.cvtables import ClinicalDomainDiagnoses
from dbmconfigapp.models.cvtables import ClinicalDomainEncounters
from dbmconfigapp.models.cvtables import ClinicalDomainEncounterDetails
from dbmconfigapp.models.cvtables import ClinicalDomainSummary
from dbmconfigapp.models.cvtables import ClinicalDomainProcedures
from dbmconfigapp.models.cvtables import ClinicalDomainLabResultsHistory
from dbmconfigapp.models.cvtables import ClinicalDomainImaging
from dbmconfigapp.models.cvtables import ClinicalDomainLaboratory
from dbmconfigapp.models.cvtables import ClinicalDomainDocuments
from dbmconfigapp.models.cvtables import ClinicalDomainLabResults
from dbmconfigapp.models.clinical_viewer_general import ClinicalViewerGeneral, ClinicalViewerGeneralPage, DisclaimerText, WebCulture, ExternalApplication, ExternalApplicationParameter
from dbmconfigapp.models.patient_view import PatientViewGeneralDefinitions,PatientViewPage, PVClinicalDomainPage, PVPatientDisplayPage, PVCCDADisplayPage, DemographySearchFields, PatientViewDefaultLandingPage, ImagingPacsDisclaimer, CarequalityIntegrationSettingsPage, CarequalityIntegrationSettingsModel, ParticipantListBasedPAAModel, ParticipantListModel,ParticipantBaselineListModel,PrefetchSettingsModel, SpecializedViews, PatientsListViews
from dbmconfigapp.models import PVPatientSearchPage
from dbmconfigapp.models.pl_general import PlGeneralPage, EncounterDiagnosisRelationship
from dbmconfigapp.models.collaborate_patient_search import PatientSearchDataElement, EmergencyDeclarationReasons, PatientSearchTooltip, EmergencyDeclarationText, SearchResultGrid
from dbmconfigapp.models.apps_reporting import CVReportingPage, PlReportingPage, PVReportingPage
from dbmconfigapp.models.vpo import Vpo, VpoCommon, VpoPPOL, VpoCommunication, VpoEHRAgentDomains, VpoFacilityDisplay
from dbmconfigapp.models.collaborate_patient_search import CvPatientSearch
from dbmconfigapp.models.cv_patient_display import CvPatientDisplayPage
from dbmconfigapp.models.apps_patient_display import PlPatientDisplayPage, PatientDetailsSectionOrdering
from dbmconfigapp.models.clinical_code_display import ClinicalCodeDisplay, ClinicalCodeDisplayPage, PlClinicalCodeDisplayPage
from dbmconfigapp.models.ehragent_clinical_domains import EHRAgentClinicalDomainsProperties, EHRAgentCVCommonClinicalDomainsProperties, EHRAgentBlinks, VitalsInpatientMeasurement, EHRAgentSemanticDelta
from dbmconfigapp.models.ehragent import EhrAgentGeneral,EhrAgentBaseUrl,EhrAgentHelp
from dbmconfigapp.models.agentpp_hosted_app import AgentppHostedAppPage, AgentppHostedApp, AgentUserCentricApp, AgentSMARTonFHIRApp, LauncherGeneralProperties, AgentHostedAppsBehavior
from dbmconfigapp.models.ccda_display import CCDADisplay, CVCCDADisplayPage, DataExportCCDADisplayPage
from dbmconfigapp.models.capsule import CapsulePage, CapsuleService
from dbmconfigapp.models.external_documents import MyHRConnectivityEntity, MyHRConnectivityPage, MyHROrganizationsEntity
from via.models import Via, Initiate, InitiateVpo, InitiatePage, ViaVpo, ViaPage, InitiateMappingsPage, InitiateMappings, AuthoritySystemsPage, AuthoritySystems, dbMotionSystem, CCDAwithoutADTSystems, EmpiPpolGeneralPage
from externalapps.models import EHR, Instance, AppId, InstanceProperties, Participant, PatientContext, SourceSystem, UserContext, OrderingFacilities
from externalapps.models_installation_profiles import InstallationProfile
from dbmconfigapp.models.ehragent_measurements import EHRAgentSemanticGroup, EHRAgentMeasurementProperties
from dbmconfigapp.models.agent_general_page import AgentHubGeneralPage
from federation.models import *
from security.models import *

from django.core.serializers.python import Serializer as PythonSerializer
#from django.db.models.fields import FieldDoesNotExist

# from django.db.models import get_app, get_models
from django.apps import apps

# data loading
from dataloading.models import *
#

from django.contrib.contenttypes.models import ContentType
from dbmconfigapp.models.operational_manager import UsageReports, OperationalManagerPage, DataAccessAuditing, DataAccessAuditingPage, CAGDataAccessAuditingPage, CAGDataAccessAuditing

from os import path
from dbmconfigapp.admin.patient_view import PVVpoEhrAgentDomainsInline, PVCategoriesProperties
from dbmconfigapp.admin.patient_view import PVVpoEhrAgentDomainsProceduresInline

from dbmconfigapp.admin.clinical_domain import PVMeasurementPage

from dbmconfigapp.models.culture import Culture, CurrentCulture
from dbmconfigapp.models.document_search_general import DocumentSearchGeneral,DocumentSearchGeneralProperties
from dbmconfigapp.models.document_search_bootstrap import DocumentSearchBootstrap,DocumentSearchBootstrapProperties
from dbmconfigapp.models.document_search_live_feeds import DocumentSearchLiveFeeds,DocumentSearchLiveFeedsProperties

def export_all_ccenter():
    logger = logging.getLogger('django')
    err_additional_info = "Exporting all CCenter data"
    
    try:
        for app_name in ['dbmconfigapp', 'security', 'externalapps', 'via', 'dataloading', 'auth']:
            pages = []
            other_objects = []
            
            app = apps.get_app_config(app_name)
            for model in list(app.get_models()):
                if PageBaseModel in inspect.getmro(model):
                    pages += model.objects.all()
                else:
                    other_objects += model.objects.all()
            
            other_objects += get_files_to_export(other_objects, logger)
            
            all_objects = pages + other_objects
        
            data = {}
            data["meta"] = {
                "pages": 'All pages of app_name',
                "page_titles": '',
                "models": 'All models of app_name',
                "files:": '',
                "export_timestamp": datetime.datetime.today().strftime("%Y-%m-%dT%H%M")
            }
            
            err_additional_info = 'serializing data to JSON'
            data["objects"] = serializers.serialize('json', all_objects)
            
            json_data = json.dumps(data)
            with open(path.join(settings.PROJECT_DIR, 'resources/json/{0}.json'.format(app_name)), 'w') as f:
                f.write(json_data)
        
    
    except Exception as e:
        print('An error occurred while {0}'.format(err_additional_info))
        logger.error("Export failed. An error occurred while {1}\n{0}".format(e.message, err_additional_info))
        raise e

def export_all_objects(model):
    '''
    Simply export all the objects from the model, in the most basic way.
    '''
    return list(model.objects.all()) 

# export/import all application objects except Page models
def get_all_app_objects(app_name):
    objects = []
    
    app = apps.get_app_config(app_name)
    for model in list(app.get_models()):
        # if isinstance(model, PageBaseModel) != True:
        objects += model.objects.all()
    
    return objects

"""
For future use - encoding:
-------------------------
from: http://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password

from Crypto.Cipher import AES
key = "any_16_length_key"
cipher = AES.new(key)

enc_password = base64.encodestring(cipher.encrypt(password.rjust(32)))

to decode:
cipher.decrypt(base64.b64decode(enc_password)).strip()

"""
def get_managed_users_objects_for_export():
    objects = []
 
    for adprovider in ADProviders.objects.all():
        adprovider.untrusted_ad_user_name = ''
        adprovider.untrusted_ad_user_password = ''
    objects += ADProviders.objects.all()
    
    objects += SAMLIssuers.objects.all()
    
    return objects

def get_security_objects_for_export():
    objects = []
    
    app = apps.get_app_config("security")
    for model in list(app.get_models()):
        new_objects = model.objects.all()
        if model is ADProviders:
            for adprovider in new_objects:
                adprovider.untrusted_ad_user_name = ''
                adprovider.untrusted_ad_user_password = ''
        objects += new_objects
    
    return objects

def get_prefetch_settings_objects_for_export(model):
    objects = []
    new_objects = model.objects.all()
    if model is PrefetchSettingsModel:
        for prefetchset in new_objects:
            prefetchset.api_subscription_key = ''
    objects += new_objects
    return objects


# EHR, Instance, InstanceProperties, Participant, PatientContext, SourceSystem, UserContext
def get_all_externalapps_objects():
    objects = []
    objects += EHR.objects.all()
    objects += AppId.objects.all()
    objects += InstanceProperties.objects.all()
    objects += Instance.objects.all()
    objects += Participant.objects.all()
    objects += PatientContext.objects.all()
    objects += SourceSystem.objects.all()
    objects += UserContext.objects.all()
    objects += OrderingFacilities.objects.all()
    
    return objects

def export_pv_vpo_patient_groupby_objects(clinical_domain):
    cd_actual = clinical_domain.objects.all()[0]
    objects = []
    objects += Vpo.objects.filter(clinical_domain=cd_actual)
    return objects  


def export_vpo_patient_display_objects():
    objects = []
    objects += Vpo.objects.filter(cv_patient_display=1)
    objects += VpoPPOL.objects.filter(cv_patient_display=1)
    return objects

def delete_cv_general():
    objects = []
    objects += DisclaimerText.objects.all()
    objects += WebCulture.objects.all()
    objects += ExternalApplication.objects.all()
    objects += ExternalApplicationParameter.objects.all()
    return objects

def export_cv_general():
    objects = delete_cv_general()
    objects += ClinicalViewerGeneral.objects.all()
    objects += VpoFacilityDisplay.objects.filter(parent_cv_general=1)
    objects += VpoCommon.objects.filter(cv_general=1)
    objects += VpoCommunication.objects.filter(parent_cv_general=1)
    return objects

def delete_pl_general():
    objects = []
    return objects

def export_pl_general():
    objects = delete_pl_general()
    objects += VpoFacilityDisplay.objects.filter(pl_parent=1)
    objects += EncounterDiagnosisRelationship.objects.all()
    return objects

def delete_capsule():
    objects = []
    return objects

def export_capsule():
    objects = delete_capsule()
    objects += CapsuleService.objects.all()
    return objects

def export_apps_reporting():
    objects = []
    objects += AppsReporting.objects.all()
    objects += Vpo.objects.filter(reporting_cv=1)
    return objects

def export_pv_vpo_patient_display_objects():
    objects = []
    objects += Vpo.objects.filter(pv_parent=1)
    objects += Vpo.objects.filter(clinical_domain_id=13)
    return objects

def delete_patient_search(patient_search):
    
    objects = []
    objects += InitiateMappings.objects.all()
    objects += EmergencyDeclarationReasons.objects.all()
    objects += PatientSearchTooltip.objects.all()
    objects += DemographySearchFields.objects.all()
    objects += SearchResultGrid.objects.all()
    objects += VpoPPOL.objects.filter(clinical_domain=14)
    return objects

def export_patient_search(patient_search):
    objects = []
    objects += InitiateMappings.objects.all()
    objects += PatientSearchDisplayOptions.objects.all()
    objects += export_data_element(PatientSearchDataElement)
    objects += export_data_element(PatientSearchHistoryDataElement)
    objects += CollaboratePatientSearchProperties.objects.all()
    objects += Vpo.objects.filter(clinical_domain=14)
    objects += EmergencyDeclarationReasons.objects.all()
    objects += PatientSearchTooltip.objects.all()
    objects += VpoPPOL.objects.filter(clinical_domain=14)
    objects += PatientSearchDefaultSearch.objects.all()
    objects += EmergencyDeclarationText.objects.all()
    objects += DemographySearchFields.objects.all()
    objects += SearchResultGrid.objects.all()
    
    return objects

def export_data_element(model):
    '''
    Exports all the objects, and all the related objects from the data element.
    '''
    objects = []

    for obj in model.objects.all():
        # objects.append(obj)
        objects.append(obj.dataelement_ptr)

    return objects

# Specialized functions:

# For clinical domains:
def export_cd_elements_and_properties(clinical_domain):
    '''
    Exports a clinical domain's data elements and properties.

    @params
    clinical_domain: The clinical domain object (which inherits from PageBaseModel)
    Returns: a list of objects.
    '''
    objects = []

    # Get the ACTUAL clinical domain.
    cd_actual = clinical_domain.objects.all()[0]
    objects += DataElement.objects.filter(clinical_domain=cd_actual)
    objects += ClinicalDomainProperties.objects.filter(clinical_domain=cd_actual)
    objects += EHRAgentCVCommonClinicalDomainsProperties.objects.filter(cv_parent=cd_actual) 
    objects += Vpo.objects.filter(clinical_domain=cd_actual)
    objects += VpoCommon.objects.filter(clinical_domain=cd_actual)
    if (cd_actual.id != 11):
        # if not Procedures
        objects += VpoEHRAgentDomains.objects.filter(clinical_domain=cd_actual)

    return objects

# For clinical domain deletion:
def delete_cd_elements_before_import(clinical_domain):
    '''
    Exports a clinical domain's data elements and properties.

    @params
    clinical_domain: The clinical domain object (which inherits from PageBaseModel)
    Returns: a list of objects.
    '''
    objects = []

    # Get the ACTUAL clinical domain.
    cd_actual = clinical_domain.objects.all()[0]
    objects += Vpo.objects.filter(clinical_domain=cd_actual)
    objects += DataElement.objects.filter(clinical_domain=cd_actual)

    return objects

def export_MyHR(model):
    objects = MyHRConnectivityEntity.objects.all()
    for myhr in objects:
        myhr.pcehr_exist_url = ''
        myhr.gain_access_url = ''
        myhr.get_document_list_url = ''
        myhr.get_document_url= ''

    return objects

def get_all_federation_objects():
    objects = []
    objects += Node.objects.all()
    objects += Group.objects.all()
    
    return objects
# This is a dictionary that maps pages in the application (as the appear in the treeview) 
# to several pieces of info we need when exporting/importing.
#
# Format:
# {"pagename": {
#   page_model: "pagename" # This is the name of the model of the page (which inherits from PageBase).
#   functions_for_export_objs: [function_to_call_for_getting_export_objs, another_function],
#   functions_for_import_objs_to_del: [function_to_call_for_getting_import_objs, another],
# }
#
# You can use the generic functions above like export_all_objects(YourModel) and export_data_element(YourModel)
# to make your life easier.
get_objects_table = {
        'cv_allergies': {
            "page_model": ClinicalDomainAllergies,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainAllergies)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_documents': {
            "page_model": ClinicalDomainDocuments,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainDocuments)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_demographics': {
            "page_model": ClinicalDomainDemographics,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainDemographics)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_diagnoses': {
            "page_model": ClinicalDomainDiagnoses,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainDiagnoses)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_encounters': {
            "page_model": ClinicalDomainEncounters,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainEncounters)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_encounters_details': {
            "page_model": ClinicalDomainEncounterDetails,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainEncounterDetails)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_imaging': {
            "page_model": ClinicalDomainImaging,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainImaging),
                                          lambda: export_all_objects(ImagingPacs),                                          
                                          lambda: export_all_objects(ImagingPacsParameter)],
            "functions_for_import_objs_to_del": [lambda: delete_cd_elements_before_import(ClinicalDomainImaging),
                                                 lambda: export_all_objects(ImagingPacs),
                                                 lambda: export_all_objects(ImagingPacsParameter)],
        },
        'cv_immunizations': {
            "page_model": ClinicalDomainImmunizations,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainImmunizations)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_laboratory': {
            "page_model": ClinicalDomainLaboratory,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainLaboratory),
                                                        lambda: export_all_objects(LabChartDisplayOptions)],

            "functions_for_import_objs_to_del": [],
        },
        'cv_lab_results': {
            "page_model": ClinicalDomainLabResults,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainLabResults)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_lab_results_history': {
            "page_model": ClinicalDomainLabResultsHistory,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainLabResultsHistory)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_medications': {
            "page_model": ClinicalDomainMedications,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainMedications)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_pathologies': {
            "page_model": ClinicalDomainPathologies,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainPathologies)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_plv': {
            "page_model": ClinicalDomainPlv,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainPlv)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_problems': {
            "page_model": ClinicalDomainProblems,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainProblems)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_procedures': {
            "page_model": ClinicalDomainProcedures,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainProcedures)],
            "functions_for_import_objs_to_del": [],
        },
        'cv_summary': {
            "page_model": ClinicalDomainSummary,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainSummary),
                                          lambda: export_all_objects(AllergiesDataElement),
                                          lambda: export_all_objects(MedicationsDataElement),
                                          lambda: export_all_objects(ProblemsDataElement),
                                          lambda: export_all_objects(DiagnosisDataElement),
                                          lambda: export_all_objects(LabsDataElement)],
                                          
            "functions_for_import_objs_to_del": [lambda: delete_cd_elements_before_import(ClinicalDomainSummary)],
        },
        'cv_vitals': {
            "page_model": ClinicalDomainVitals,
            "functions_for_export_objs": [lambda: export_cd_elements_and_properties(ClinicalDomainVitals)],

            "functions_for_import_objs_to_del": [],
        },
        'cv_general': {
            "page_model": ClinicalViewerGeneralPage,
            "functions_for_export_objs": [lambda: export_cv_general()],
            "functions_for_import_objs_to_del": [lambda: delete_cv_general()],
        },
        'cv_patient_display': {
            "page_model": CvPatientDisplayPage,
            "functions_for_export_objs": [lambda: export_all_objects(AppsPatientDisplay),
                                          lambda: export_vpo_patient_display_objects(),
                                          lambda: export_all_objects(AppsPatientDisplayWithAgent),
                                          lambda: export_all_objects(AppsPatientDisplayCommon),
                                          lambda: export_all_objects(AppsAdvanceDirectiveNodes),
                                          lambda: export_all_objects(AppsPatientDisplayAgeCalculation),
                                          lambda: export_all_objects(AppsPatientDisplayValueBaseProgram),
                                          lambda: export_all_objects(AppsPatientDisplayVBP)],
            "functions_for_import_objs_to_del": [lambda: export_all_objects(AppsPatientDisplayAgeCalculation),
                                                 lambda: export_all_objects(AppsPatientDisplayVBP)],
        },
        'cv_patient_search': {
            "page_model": CvPatientSearch,
            "functions_for_export_objs": [lambda: export_patient_search(CvPatientSearch)],
            "functions_for_import_objs_to_del": [lambda: delete_patient_search(CvPatientSearch)],
        },
        'cv_reporting': {
            "page_model": CVReportingPage,
            "functions_for_export_objs": [lambda: export_apps_reporting()],
            "functions_for_import_objs_to_del": [],
        },
        'clinical_code_display': {
            "page_model": ClinicalCodeDisplayPage,
            "functions_for_export_objs": [lambda: export_all_objects(ClinicalCodeDisplay)],
            "functions_for_import_objs_to_del": [],
        },
        'directMessaging_acdm': {
            "page_model": DirectMessagingAcdmPage,
            "functions_for_export_objs": [lambda: export_all_objects(DirectMessagingAcdm)],
                "functions_for_import_objs_to_del": [],
        },
        'usage_reports': {
            "page_model": OperationalManagerPage,
            "functions_for_export_objs": [lambda: export_all_objects(UsageReports)],
                "functions_for_import_objs_to_del": [],
        },
        'data_access_auditing': {
            "page_model": DataAccessAuditingPage,
            "functions_for_export_objs": [lambda: export_all_objects(DataAccessAuditing)],
                "functions_for_import_objs_to_del": [],
        },
        'cag_data_access_auditing': {
            "page_model": CAGDataAccessAuditingPage,
            "functions_for_export_objs": [lambda: export_all_objects(CAGDataAccessAuditing)],
                 "functions_for_import_objs_to_del": [],
        },
        'via_general': {
            "page_model": ViaPage,
            "functions_for_export_objs": [lambda: export_all_objects(Via),
                                          lambda: export_all_objects(ViaVpo)],
                "functions_for_import_objs_to_del": [],
        },
        'via_initiate': {
            "page_model": InitiatePage,
            "functions_for_export_objs": [lambda: export_all_objects(Initiate),
                                          lambda: export_all_objects(InitiateVpo)],
                "functions_for_import_objs_to_del": [],
        },
                     'via_authoritysystems': {
            "page_model": AuthoritySystemsPage,
            "functions_for_export_objs": [lambda: export_all_objects(AuthoritySystems),
                                          lambda: export_all_objects(dbMotionSystem),
                                          lambda: export_all_objects(CCDAwithoutADTSystems)],
            "functions_for_import_objs_to_del": [lambda: export_all_objects(AuthoritySystems),
                                                 lambda: export_all_objects(dbMotionSystem), ],
        },
        'via_initiatemappings': {
            "page_model": InitiateMappingsPage,
            "functions_for_export_objs": [lambda: export_all_objects(InitiateMappings),
                                          lambda: export_all_objects(DemographySearchFields),
                                          lambda: export_all_objects(SearchResultGrid)],
                "functions_for_import_objs_to_del": [lambda: export_all_objects(InitiateMappings),
                                                      lambda: export_all_objects(DemographySearchFields),
                                                      lambda: export_all_objects(SearchResultGrid)],
        },
        'via_ppolgeneral': {
            "page_model": EmpiPpolGeneralPage,
            "functions_for_export_objs": [lambda: export_all_objects(PpolGeneral),],
                "functions_for_import_objs_to_del": [lambda: export_all_objects(PpolGeneral)],
        },
        # 'ehragent_apps' are always selected entirely
        'ehragent_apps_ehr': {
            "page_model": EHR,
            "functions_for_export_objs": [lambda: get_all_externalapps_objects()],
            "functions_for_import_objs_to_del": [lambda: get_all_externalapps_objects()],
        },
        'ehragent_apps_instance': {
            "page_model":  Instance,
            "functions_for_export_objs": [],
            "functions_for_import_objs_to_del": [],
        },
        'ehragent_apps_instance_properties': {
            "page_model": InstanceProperties,
            "functions_for_export_objs": [],
            "functions_for_import_objs_to_del": [],
        },
        'federation_app_node': {
            "page_model": Node,
            "functions_for_export_objs": [lambda: get_all_federation_objects(),],
            "functions_for_import_objs_to_del": [],
        },
        'ehragent_apps_install_profile': {
            "page_model": InstallationProfile,
            "functions_for_export_objs": [lambda: export_all_objects(InstallationProfile),],
            "functions_for_import_objs_to_del": [],
        },
        'agenthub_general': {
            "page_model": AgentHubGeneralPage,
            "functions_for_export_objs": [lambda: export_all_objects(EhrAgentBaseUrl),
                                          lambda:export_all_objects(CurrentCulture),
                                          lambda:export_all_objects(Culture),],
            "functions_for_import_objs_to_del": [],
        },
        'agent_plus_plus_hosted_aplications': {
            "page_model": AgentppHostedAppPage,
            "functions_for_export_objs": [lambda: export_all_objects(AgentppHostedApp),
                                          lambda: export_all_objects(LauncherGeneralProperties),
                                          lambda: export_all_objects(AgentHostedAppsBehavior),
                                          lambda: export_all_objects(AgentSMARTonFHIRApp),
                                          lambda: export_all_objects(EhrAgentHelp), ],
            "functions_for_import_objs_to_del": [lambda: export_all_objects(AgentppHostedApp),
                                                 # not adding LauncherGeneralProperties deletion so importing improper json will not corrupt the display
                                                 #lambda: export_all_objects(LauncherGeneralProperties),
                                                 lambda: export_all_objects(AgentSMARTonFHIRApp),
                                                 lambda: export_all_objects(EhrAgentHelp), ],
        },
        'security_managedusers': {
            "page_model": ADProviders,
            "functions_for_export_objs": [lambda: get_managed_users_objects_for_export(), ],
            "functions_for_import_objs_to_del": [lambda: export_all_objects(SAMLIssuers),
                                                 lambda: export_all_objects(ADProviders),],
        },
        'security_rolemapping': {
            "page_model": Applications,
            "functions_for_export_objs": [],
            "functions_for_import_objs_to_del": [],
        },
        'security_unmanagedusers': {
            "page_model": ApplicationDomains,
            "functions_for_export_objs": [lambda: export_all_objects(InternalRoles),
                                          lambda: export_all_objects(ApplicationDomains),
                                          lambda: export_all_objects(SAMLIssuersUnmanaged),
                                          lambda: export_all_objects(Applications),
                                          lambda: export_all_objects(RoleMapping),],
            "functions_for_import_objs_to_del": [lambda: export_all_objects(InternalRoles),
                                                  lambda: export_all_objects(ApplicationDomains),
                                                  lambda: export_all_objects(SAMLIssuersUnmanaged),
                                                  lambda: export_all_objects(Applications),
                                                  lambda: export_all_objects(RoleMapping),],
        },
        'security_general': {
            "page_model": SecurityGeneralPage,
            "functions_for_export_objs": [lambda: export_all_objects(SecurityGeneral),
                                          lambda: export_all_objects(PatientAuthorization),
                                          lambda: export_all_objects(PatientProviderRelationship),],
            "functions_for_import_objs_to_del": [],
        },



        'data_loading_app': {
            "page_model": PartitioningPage,
            "functions_for_export_objs": [lambda: export_all_objects(Partitioning)],
            "functions_for_import_objs_to_del": [],
        },
        'data_loading_batch': {
            "page_model": BatchLoadingPage,
            "functions_for_export_objs": [lambda: export_all_objects(BatchLoadingScheduler),
                                          lambda: export_all_objects(BatchLoadingSchedulerInPath), ],
            "functions_for_import_objs_to_del": [],
        },
        'patient_view_general': {
            "page_model": PatientViewPage,
            "functions_for_export_objs": [lambda: export_all_objects(PatientViewGeneralDefinitions),
                                          lambda: export_all_objects(VpoCommunication),
                                          lambda: export_all_objects(PatientViewDefaultLandingPage),
                                          lambda: export_all_objects(SpecializedViews),
                                          lambda: export_all_objects(PatientsListViews)],
            "functions_for_import_objs_to_del": [],
        },
		'pv_carequality_integration_settings': {
            "page_model": CarequalityIntegrationSettingsPage,
            "functions_for_export_objs": [lambda: export_all_objects(CarequalityIntegrationSettingsModel),
                                          lambda: export_all_objects(ParticipantListBasedPAAModel),
                                          lambda: export_all_objects(ParticipantListModel),
                                          lambda: export_all_objects(ParticipantBaselineListModel),
                                          lambda: get_prefetch_settings_objects_for_export(PrefetchSettingsModel),
                                          ],
            "functions_for_import_objs_to_del": [],
        },																					  
		 'pv_clinical_domains_page': {
            "page_model": PVClinicalDomainPage, 
            "functions_for_export_objs": [lambda: export_all_objects(VpoEHRAgentDomains),
                                          lambda: export_all_objects(EncounterDiagnosisRelationship),
                                          lambda: export_all_objects(PVCategoriesProperties),
                                          lambda:  export_pv_vpo_patient_groupby_objects(ClinicalDomainDocuments),
                                          lambda: export_all_objects(EHRAgentSemanticDelta),
                                          lambda: export_all_objects(EhrAgentGeneral),
                                          lambda: export_cd_elements_and_properties(ClinicalDomainDocuments),
                                          lambda: export_all_objects(EHRAgentClinicalDomainsProperties),
                                          lambda: export_all_objects(ImagingPacs),
                                          lambda: export_all_objects(ImagingPacsParameter),
                                          lambda: export_all_objects(ImagingPacsDisclaimer),
                                          ],
              "functions_for_import_objs_to_del": [lambda: export_all_objects(PVCategoriesProperties),
                                          lambda: export_all_objects(EHRAgentClinicalDomainsProperties),
                                          lambda: export_all_objects(ImagingPacs),
                                          lambda: export_all_objects(ImagingPacsParameter),
                                          ],
        },
        'pv_reporting': {
            "page_model": PVReportingPage,
            "functions_for_export_objs": [lambda: export_apps_reporting()],
                "functions_for_import_objs_to_del": [],
        },
        'pv_measurement': {
            "page_model": PVMeasurementPage,
            "functions_for_export_objs": [lambda: export_pv_vpo_patient_display_objects(),
                                          lambda: export_all_objects(VitalsInpatientMeasurement),
                                          lambda: export_all_objects(EHRAgentSemanticGroup),
                                          lambda: export_all_objects(EHRAgentMeasurementProperties)],
            "functions_for_import_objs_to_del": [lambda: export_pv_vpo_patient_display_objects(),
                                                  lambda: export_all_objects(VitalsInpatientMeasurement)],
        },
        'pv_clinical_code_display':{
            "page_model": PVClinicalCodeDisplayPage,
            "functions_for_export_objs": [lambda: export_all_objects(ClinicalCodeDisplay)],
                "functions_for_import_objs_to_del": [],
        },
        'pv_ccdadisplay':{
            "page_model": PVCCDADisplayPage,
            "functions_for_export_objs": [lambda: export_all_objects(CCDADisplay)],
                "functions_for_import_objs_to_del": [],
        },
        'pl_patient_display': {
            "page_model": PlPatientDisplayPage,
            "functions_for_export_objs": [lambda: export_all_objects(AppsPatientDisplay),
                                          lambda: export_vpo_patient_display_objects(),
                                          lambda: export_all_objects(AppsPatientDisplayWithAgent),
                                          lambda: export_all_objects(AppsPatientDisplayCommon),
                                          lambda: export_all_objects(AppsAdvanceDirectiveNodes),
                                          lambda: export_all_objects(AppsPatientDisplayAgeCalculation),
                                          lambda: export_all_objects(AppsPatientDisplayValueBaseProgram),
                                          lambda: export_all_objects(AppsPatientDisplayVBP),
                                          lambda: export_all_objects(PatientDetailsSectionOrdering)],
            "functions_for_import_objs_to_del": [lambda: export_all_objects(AppsPatientDisplayAgeCalculation),
                                                 lambda: export_all_objects(AppsPatientDisplayVBP)],
        },
        'pv_patient_display': {
            "page_model": PVPatientDisplayPage,
            "functions_for_export_objs": [lambda: export_all_objects(AppsPatientDisplay),
                                          lambda: export_vpo_patient_display_objects(),
                                          lambda: export_all_objects(AppsPatientDisplayWithAgent),
                                          lambda: export_all_objects(AppsPatientDisplayCommon),
                                          lambda: export_all_objects(AppsAdvanceDirectiveNodes),
                                          lambda: export_all_objects(AppsPatientDisplayAgeCalculation),
                                          lambda: export_all_objects(AppsPatientDisplayMetricCodeBasedIndicator),
                                          lambda: export_all_objects(PvPatientNameDisplay),
                                          lambda: export_all_objects(AppsPatientDisplayValueBaseProgram),
                                          lambda: export_all_objects(AppsPatientDisplayVBP),
                                          lambda: export_all_objects(PatientDetailsSectionOrdering)],
            "functions_for_import_objs_to_del": [lambda: export_all_objects(AppsPatientDisplayAgeCalculation),
                                                 lambda: export_all_objects(AppsPatientDisplayMetricCodeBasedIndicator),
                                                 lambda: export_all_objects(AppsPatientDisplayVBP),
                                                 lambda: export_all_objects(PvPatientNameDisplay)],
        },
        'pv_search_page': {
            "page_model": PVPatientSearchPage,                                          
            "functions_for_export_objs": [lambda: export_all_objects(InitiateMappings),
                                          lambda: export_all_objects(CollaboratePatientSearchProperties),
                                          lambda: export_all_objects(PatientSearchTooltip),
                                          lambda: export_all_objects(EmergencyDeclarationText),
                                          lambda: export_all_objects(EmergencyDeclarationReasons),
                                          lambda: export_all_objects(VpoPPOL),
                                          lambda: export_all_objects(PatientSearchDisplayOptions),                                          
                                          lambda: export_all_objects(DemographySearchFields),
                                          lambda: export_all_objects(SearchResultGrid)],
			"functions_for_import_objs_to_del": [lambda: delete_patient_search(PVPatientSearchPage)],
        },
        'pl_clinical_code_display': {
            "page_model": PlClinicalCodeDisplayPage,
            "functions_for_export_objs": [lambda: export_all_objects(ClinicalCodeDisplay)],
            "functions_for_import_objs_to_del": [],
        },
        'pl_general_definitions': {
            "page_model": PlGeneralPage,
            "functions_for_export_objs": [lambda: export_pl_general()],
            "functions_for_import_objs_to_del": [lambda: delete_pl_general()],
        },
        'pl_reporting': {
            "page_model": PlReportingPage,
            "functions_for_export_objs": [lambda: export_apps_reporting()],
                "functions_for_import_objs_to_del": [],
        },    
         'cv_ccdadisplay': {
            "page_model": CVCCDADisplayPage,
            "functions_for_export_objs": [lambda: export_all_objects(CCDADisplay)],
                "functions_for_import_objs_to_del": [],
        },                                                                              
         'dataexport_ccdadisplay': {
            "page_model": DataExportCCDADisplayPage,
            "functions_for_export_objs": [lambda: export_all_objects(CCDADisplay)],
                "functions_for_import_objs_to_del": [],
        },
         'capsule': {
            "page_model": CapsulePage,
            "functions_for_export_objs": [lambda: export_capsule()],
            "functions_for_import_objs_to_del": [lambda: delete_capsule()],
        },
         
        'external_documents_my_hr': {
            "page_model": MyHRConnectivityPage,
            "functions_for_export_objs": [lambda: export_MyHR(MyHRConnectivityEntity), 
                                          lambda: export_all_objects(MyHROrganizationsEntity)],
            "functions_for_import_objs_to_del": [lambda: export_all_objects(MyHRConnectivityEntity), 
                                                 lambda: export_all_objects(MyHROrganizationsEntity)],
        },
        'culture': {
            "page_model": Culture,
            "functions_for_export_objs": [lambda: export_all_objects(Culture)],
            "functions_for_import_objs_to_del": [],
        },
        'CurrentCulture': {
            "page_model": CurrentCulture,
            "functions_for_export_objs": [lambda: export_all_objects(CurrentCulture)],
            "functions_for_import_objs_to_del": [],
        },
        'document_search_general': {
            "page_model": DocumentSearchGeneral,
            "functions_for_export_objs": [lambda: export_all_objects(DocumentSearchGeneralProperties)],
                "functions_for_import_objs_to_del": [],
        },
		'document_search_bootstrap': {
            "page_model": DocumentSearchBootstrap,
            "functions_for_export_objs": [lambda: export_all_objects(DocumentSearchBootstrapProperties)],
                "functions_for_import_objs_to_del": [],
        },
		'document_search_live_feeds': {
            "page_model": DocumentSearchLiveFeeds,
            "functions_for_export_objs": [lambda: export_all_objects(DocumentSearchLiveFeedsProperties)],
                "functions_for_import_objs_to_del": [],
        },
}


def get_files_to_export(all_objects, logger):
    # Returns the list of records from DbFiles that are related to the given model
    dbfiles = []
    for model in all_objects:
        if hasattr(model, 'contains_file_fields'):
            if model.contains_file_fields():
                for img_fld in model.file_fields:
                    img = getattr(model, img_fld.name).name
                    if img:
                        try:
                            dbfiles.append(DbFiles.objects.get(filename=img))
                        except:
                            print('Error exporting: %s' % img)
                            logger.error("Couldn't find file: %s" % img)
        
    return set(dbfiles)
        

def get_export_db_data(pages_list, no_time_stamp=False):
    '''
    Export our models as a JSON file.

    Gets a list of names of pages, e.g. ["cv_demographics", "collaborate_ce_recipients", ...]
    '''
    err_additional_info = 'initializing'
    logger = logging.getLogger('django')
    all_objects = []  # all_objects will contain all of the exported objects.
    page_titles = []
    
    err_additional_info = 'collecting pages data'
    try:
        for page in pages_list:
            try:
                for func in get_objects_table[page]["functions_for_export_objs"]:
                    all_objects += func()
            except Exception as e:
                raise Exception("Page: {0} \nDetails: {1}".format(page, e.message))
            
            page_titles.append(get_objects_table[page]['page_model']._meta.verbose_name)
        
        
        # handle files
        err_additional_info = 'handling files'
        dbfiles = get_files_to_export(all_objects, logger)

        # add the files to all_objects
        if dbfiles:
            all_objects += dbfiles
        
        # get distinct list of model types
        model_types = set([type(obj) for obj in all_objects])
        if dbfiles: model_types.add(DbFiles) 
        
        # Serialize the data as JSON
        err_additional_info = 'writing JSON metadata'
        data = {}
        data["meta"] = {
            "pages": pages_list,
            "page_titles": page_titles,
            "models": [str(m) for m in model_types],
            "files:": [f.filename for f in dbfiles],
        }
        if not no_time_stamp:
            data["meta"]["export_timestamp"] = datetime.datetime.today().strftime("%Y-%m-%dT%H%M")
        
        err_additional_info = 'serializing data to JSON'
        data["objects"] = serializers.serialize('json', all_objects)
        ret = json.dumps(data)
    
        return ret
    
    except Exception as e:
        print('An error occurred while {0}'.format(err_additional_info))
        logger.error("Export failed. An error occurred while {1}\n{0}".format(e.message, err_additional_info))
        raise e

from django.db import transaction

def import_federation_nodes(nodes_list, group_list):
    
    # 1. Save federation nodes app server for all related models
    save_node_uid(AuthoritySystems, 'dbmotion_node_id')
    save_node_uid(dbMotionSystem, 'dbmotion_system_node_id')
     
    # 2. Delete all nodes and groups
    #Node.objects.exclude(pk__in=pk_list).delete()
    Node.objects.all().delete()
            
    Group.objects.all().delete()
    
    # 3. Create groups and nodes from imported list
    groups = [g.object for g in group_list]
    for g in groups:
        Group(id=g.id, name=g.name).save()
        
    nodes = [n.object for n in nodes_list]
    for n in nodes:
        Node(id=n.id, uid=n.uid, name=n.name, application_server=n.application_server, ppol_provider_node_id=n.id, request_from=n.request_from, response_to=n.response_to).save()
  
    # 4. save all list with all data
    [n.save() for n in nodes]
    
    # 5. Update related objects with new node ids
    update_node_id_foreign_key(AuthoritySystems, 'dbmotion_node_id')
    update_node_id_foreign_key(dbMotionSystem, 'dbmotion_system_node_id')

def save_node_uid(model, node_foreign_key_name):
    '''
    Save federation nodes uid for selected model.
    Note: Only for models that have foreign key to node and node_uid field
    '''
    for obj in model.objects.all():
        foreign_key_value = getattr(obj, node_foreign_key_name)
        if(foreign_key_value != None):
            obj.node_uid = foreign_key_value.uid
            setattr(obj, node_foreign_key_name, None)
            obj.save()

def update_node_id_foreign_key(model, node_foreign_key_name):
    '''
    Update related model foreign key with new node ids
    Note: Only for models that have foreign key to node and node_uid field
    '''
    for obj in model.objects.all():
        
        if(obj.node_uid != None):
            
            if(Node.objects.filter(uid = obj.node_uid).exists()):
                setattr(obj, node_foreign_key_name, Node.objects.get(uid = obj.node_uid))
                
            obj.node_uid = None
            obj.save()
               
# @transaction.atomic
def import_db_from_file(import_file, request):
    '''
    Imports the DB from a file.

    If there is a problem, raises a custom exception.   
    '''
    logger = logging.getLogger('django')
    err_additional_info = ''
    try:
        err_additional_info = 'json loading'
        dict_from_file = json.loads(import_file.read())
        
        adproviders_list = []

        err_additional_info = 'deleting objects'
        # Fist, delete all the objects from the pages we acutally want to export.
        for page in dict_from_file["meta"]["pages"]:
            for func in get_objects_table[page]["functions_for_import_objs_to_del"]:
                
                objects = func()
                for obj in objects:
                    if type(obj) == ADProviders:
                        allow_delete = obj.has_constraints()
                        if allow_delete == "can_delete":
                            obj.delete()
                        else:
                            adproviders_list.append(obj)
                    else:
                        obj.delete()

        objects_list = list(serializers.deserialize("json", dict_from_file["objects"]))
		
        agent_apps = [n for n in objects_list if type(n.object) == AgentppHostedApp]
        base_url = "https://{server}.{domain}/cva/server".format(server=get_param("application_server_statefull"),
                                                                      domain=get_param("default_domain_name"))
        state_url = base_url + "/api/patient/notifications"
        for agent_app in agent_apps:
            if agent_app.object.app_name == 'Clinical View Agent':
                agent_app.object.app_key = 'cva'
                agent_app.object.get_application_state_url = state_url
            if agent_app.object.app_name == 'pha':
                agent_app.object.app_key = 'pha'
            if agent_app.object.app_name == 'Document Search':
                agent_app.object.app_key = 'doc_search'
                agent_app.object.get_application_state_url=docsearch_state_url
                agent_app.object.launch_url=docsearch_launch_url
		
		
        new_adproviders = [n for n in objects_list if type(n.object) == ADProviders]
        
        storages = ""
        for adprovider in adproviders_list:
            flag = 0
            for new_provider in new_adproviders:
                if (adprovider.domain_id == new_provider.object.domain_id):
                    flag = 1
                    adprovider.delete()
            if flag == 0:
                storages = storages + "Domain Name: %s Domain ID: %d, " % (adprovider.domain_name, adprovider.domain_id)
        
        if storages != "":
            raise ValueError('The following Active Directory providers: %s  has users assigned, please delete all assigned users to these active directories in "dbMotion Security Management" in order to delete them' % (storages))  
        
        err_additional_info = 'saving ADProviders objects'
        for adprovider in new_adproviders:
            adprovider.save()
        
        # continue with all other objects
        objects_list = [n for n in objects_list if n not in new_adproviders]

        err_additional_info = 'saving federation nodes'
        
        # import for federation nodes
        fed_nodes = [n for n in objects_list if type(n.object) == Node]
        fed_groups = [g for g in objects_list if type(g.object) == Group]
        if fed_nodes:
            import_federation_nodes(fed_nodes, fed_groups)
            # continue with all other objects
            objects_list = [n for n in objects_list if n not in fed_nodes]
        
        err_additional_info = 'saving files'
        
        # import files following existing logic - save by path, not by id
        dbfiles = [n for n in objects_list if type(n.object) == DbFiles]
        for f in dbfiles:
            fl = f.object
            dbf = DbFiles.objects.filter(filename=fl.filename)
            if dbf:
                dbf.update(data=fl.data, size=fl.size)
            else:
                DbFiles.objects.create(filename=fl.filename, data=fl.data, size=fl.size)
        
        # continue with all other objects
        objects_list = [n for n in objects_list if n not in dbfiles]
        
        err_additional_info = 'saving remaining objects'
        
        print('object_list.len = ' + str(len(objects_list)))
        for deserialized_object in objects_list:
            deserialized_object.save()

        # Custom actions:
        err_additional_info = 'custom actions'
        # Duplicate data between VPO records
        if set(dict_from_file["meta"]["pages"]).intersection(['cv_reporting', 'collaborate_reporting', 'ehragent_reporting']):
            vpo = Vpo.objects.get(clinical_domain=19)
            vpo.lab_susceptibility_methods_code_type = Vpo.objects.get(reporting_cv=1).lab_susceptibility_methods_code_type
            vpo.save()
        else:
            if 'cv_lab_results' in dict_from_file["meta"]["pages"]:
                vpo = Vpo.objects.get(reporting_cv=1)
                vpo.lab_susceptibility_methods_code_type = Vpo.objects.get(clinical_domain=19).lab_susceptibility_methods_code_type
                vpo.save()
				
        # Create PV if not exists
        pv, created = AgentppHostedApp.objects.get_or_create(app_key='pv', defaults={
            'app_name': 'Patient View',
            'enabled': False,
            'launch_url': "(auto generated)",
            'get_application_state_url': state_url + "?pv",
            'is_window_resizable': True,
            'window_default_width_size': 322,
            'window_default_height_size': 640,
            'window_minimal_width_size': 322,
            'window_minimal_height_size': 640,
            'LogoFile': 'AgentHostedApps/Logo/PatientViewLogo.png'
            })
		
        if created:
            DbFiles.objects.get_or_create(filename = pv.LogoFile, defaults={
            'size' : '542',
            'data' : 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAdhJREFUSA1j5FGw/c9AZfAl1hduIhOcRSPGqAUEA3Y0iAgGEQtMBSsrC0NJVgyY++/ff4abdx4wHD19ieH1m/cMBemRDO8/fGZYuHILTDmYDvJxYpCTFmeYMHM5ijgyB24BOxsrQ1VBEsOzF68Z3r3/xKAoL8XAzcXJkFfVzaCrqcIQ5O3IsHX3YYY37z6C9bMB1U9oKWbYue84snkYbIxInjZ/DYOlVyKDilkA2LLMxFCG+cs3M7CwsDAE+TjDDfB2sWYQ5OdlmLt0A1wMGwPDApiiX7//AIPlE8O/v38Zjpy8wHDn/mOGiAA3mDRDVLAHw7Wb9xhOnL0CF8PGwLAgJzmU4fTuRQyPzm9h0NZQZpi5aB1Y36JVWxlMDbUYlBVkGMREhBhc7c0Z5i3fhM1MFDF4HMBEr1y/C3TxRYaPnz4zHD5xgeHm3YdgqSVrtjPUFacwhAN98fnLV4afv34zLF+3E6YNJ41hwYFj5xgmzsJMFaDUtG3vMYaIQDeGb9++M6zdso/h0+evOA2GSWAEEUwCG71wxRYGRTkpcNDNXboRmxIMMQwfYKhAEth98CTDk2cvGd4BI//sxetIMriZjKMVDu7AgciQFMmEDMMmP2oBtlBBEQMAMLGXj+2UgPwAAAAASUVORK5CYII='
            })
			
        # Create a history entry for all affected pages saying that an import occurred.
        err_additional_info = 'writing to admin log'

        from authccenter.utils import get_request_user_ids
        from dbmconfigapp.models.tracking import ChangesHistory

        user_id, ccenter_user_id = get_request_user_ids(request)
        for page in dict_from_file["meta"]["pages"]:
            page_model = get_objects_table[page]["page_model"]
            ChangesHistory.objects.log_action(user_id=user_id,
                    ccenter_user_id = ccenter_user_id,
                    content_type_id=ContentType.objects.get_for_model(page_model).pk,
                    object_id=page_model.objects.all()[0].pk if page_model.objects.all() else 1,
                    object_repr=str(page_model.objects.all()[0].pk) if page_model.objects.all() else '1',
                    action_flag=CHANGE,
                    change_message="*** DB File import has affected this page ***")

    except Exception as e:
        # import pdb; pdb.set_trace()
        logger.error("Import failed. \nDetails:{0}\nOccurred during: {1}".format(e.message, err_additional_info))
        raise Exception("Importing Export file failed. {0}".format(e))



