from django.contrib import admin
from dbmconfigapp.admin import apps_reporting
from dbmconfigapp.models.cv_patient_display import CvPatientDisplayPage
from dbmconfigapp.models.apps_patient_display import PlPatientDisplayPage

from dbmconfigapp.models.cvtables import ClinicalDomainAllergies, ClinicalDomainProblems, ClinicalDomainImmunizations, ClinicalDomainVitals, ClinicalDomainDiagnoses, ClinicalDomainPathologies, ClinicalDomainMedications, ClinicalDomainEncounters, ClinicalDomainEncounterDetails, ClinicalDomainPlv, ClinicalDomainSummary, ClinicalDomainProcedures, ClinicalDomainLabResultsHistory, ClinicalDomainImaging, ClinicalDomainDocuments, ClinicalDomainLaboratory, ClinicalDomainLabResults, ClinicalDomainDemographics, ImagingPacs
from dbmconfigapp.models.collaborate_patient_search import CvPatientSearch
from dbmconfigapp.models.base import Service
from dbmconfigapp.models.base import Component
from dbmconfigapp.models.base import ModelDescriptor
from dbmconfigapp.models.direct_messaging_acdm import DirectMessagingAcdmPage
from dbmconfigapp.models.apps_reporting import CVReportingPage, PlReportingPage, PVReportingPage
from dbmconfigapp.models.clinical_viewer_general import ClinicalViewerGeneralPage,ExternalApplication
from dbmconfigapp.models.pl_general import PlGeneralPage
from dbmconfigapp.models.clinical_code_display import ClinicalCodeDisplayPage, PVClinicalCodeDisplayPage
from dbmconfigapp.models.operational_manager import OperationalManagerPage, DataAccessAuditingPage, CAGDataAccessAuditingPage
from dbmconfigapp.models.ehragent_measurements import EHRAgentSemanticGroup, PVMeasurementPage
from dbmconfigapp.models.agentpp_hosted_app import AgentppHostedAppPage,AgentSMARTonFHIRApp,AgentppHostedApp
from dbmconfigapp.models.capsule import CapsulePage
from dbmconfigapp.models.external_documents import MyHRConnectivityPage
from dbmconfigapp.models.patient_view import PatientViewPage, PVPatientSearchPage, PVClinicalDomainPage, PVPatientDisplayPage, CarequalityIntegrationSettingsPage, ParticipantListBasedPAAModel
from dbmconfigapp.models.agent_general_page import AgentHubGeneralPage


from dbmconfigapp.admin import clinical_domain, collaborate_patient_search
from dbmconfigapp.admin.apps_patient_display import CvPatientDisplayAdmin, PlPatientDisplayAdmin
from dbmconfigapp.admin.apps_reporting import CVReportingAdmin, PlReportingPageAdmin, PVReportingPageAdmin
from dbmconfigapp.admin.clinical_viewer_general import  ClinicalViewerGeneralAdmin, ExternalApplicationAdmin
from dbmconfigapp.admin.pl_general import  PlGeneralAdmin
from dbmconfigapp.admin.direct_messaging_acdm import DirectMessagingAcdmAdmin
from dbmconfigapp.admin.clinical_code_display import ClinicalCodeDisplayAdmin, PlClinicalCodeDisplayPage, PlClinicalCodeDisplayAdmin, PVClinicalCodeDisplayAdmin
from dbmconfigapp.admin.operational_manager import OperationalManagerAdmin, DataAccessAuditingAdmin, CAGDataAccessAuditingAdmin
from dbmconfigapp.admin.ehragent_measurements import EhrAgentSemanticGroupAdmin
from dbmconfigapp.admin.agentpp_hosted_app import AgentppHostedAppAdmin,AgentSMARTonFHIRAppAdmin,AgentHostedAppAdmin
from dbmconfigapp.admin.ccda_display import CVCCDADisplayAdmin, CVCCDADisplayPage, DataExportCCDADisplayPage, DataExportCCDADisplayAdmin 
from dbmconfigapp.admin.capsule import CapsuleAdmin
from dbmconfigapp.admin.external_documents import MyHRConnectivityAdmin
from dbmconfigapp.admin.patient_view import PatientViewPageAdmin, PVPatientSearchPageAdmin, PVClinicalDomainAdmin, PVPatientDisplayPageAdmin, CarequalityIntegrationSettingsPageAdmin, ParticipantListBasedPAAAdmin
from dbmconfigapp.admin.clinical_domain import PVMeasurementAdmin

from dbmconfigapp.models.tracking import ChangesHistory, LoginsHistory
from dbmconfigapp.admin.tracking import ChangesHistoryAdmin, LoginsHistoryAdmin
from dbmconfigapp.models.patient_view import PVCCDADisplayPage,PVCategoriesProperties
from dbmconfigapp.admin.patient_view import PVCCDADisplayAdmin, PVClinicalCategoriesAdmin

from dbmconfigapp.models.document_search_general import DocumentSearchGeneral,DocumentSearchGeneralProperties
from dbmconfigapp.admin.document_search_general import DocumentSearchGeneralInline, DocumentSearchGeneralAdmin
from dbmconfigapp.models.document_search_bootstrap import DocumentSearchBootstrap,DocumentSearchBootstrapProperties
from dbmconfigapp.admin.document_search_bootstrap import DocumentSearchBootstrapInline, DocumentSearchBootstrapAdmin
from dbmconfigapp.models.document_search_live_feeds import DocumentSearchLiveFeeds,DocumentSearchLiveFeedsProperties
from dbmconfigapp.admin.document_search_live_feeds import DocumentSearchLiveFeedsInline, DocumentSearchLiveFeedsAdmin


admin.autodiscover()
# admin.site.unregister(User)
# admin.site.unregister(Group)
# admin.site.unregister(Site)

admin.site.register(Service)
admin.site.register(Component)
admin.site.register(ModelDescriptor)

admin.site.register(ExternalApplication, ExternalApplicationAdmin)
admin.site.register(AgentSMARTonFHIRApp, AgentSMARTonFHIRAppAdmin)
admin.site.register(AgentppHostedApp, AgentHostedAppAdmin)
admin.site.register(PVCategoriesProperties, PVClinicalCategoriesAdmin)

admin.site.register(ImagingPacs, clinical_domain.ImagingPacsAdmin)

admin.site.register(ClinicalDomainAllergies, clinical_domain.ClinicalDomainAllergiesAdmin)
admin.site.register(ClinicalDomainProblems, clinical_domain.ClinicalDomainProblemsAdmin)
admin.site.register(ClinicalDomainImmunizations, clinical_domain.ClinicalDomainImmunizationsAdmin)
admin.site.register(ClinicalDomainVitals, clinical_domain.ClinicalDomainVitalsAdmin)
admin.site.register(ClinicalDomainDiagnoses, clinical_domain.ClinicalDomainDiagnosesAdmin)
admin.site.register(ClinicalDomainPathologies, clinical_domain.ClinicalDomainPathologiesAdmin)
admin.site.register(ClinicalDomainMedications, clinical_domain.ClinicalDomainMedicationsAdmin)
admin.site.register(ClinicalDomainEncounters, clinical_domain.ClinicalDomainEncountersAdmin)
admin.site.register(ClinicalDomainEncounterDetails, clinical_domain.ClinicalDomainEncounterDetailsAdmin)
admin.site.register(ClinicalDomainSummary, clinical_domain.ClinicalDomainSummaryAdmin)
admin.site.register(ClinicalDomainPlv, clinical_domain.ClinicalDomainPlvAdmin)
admin.site.register(ClinicalDomainProcedures, clinical_domain.ClinicalDomainProceduresAdmin)
admin.site.register(ClinicalDomainLabResultsHistory, clinical_domain.ClinicalDomainLabResultsHistoryAdmin)
admin.site.register(CvPatientSearch, collaborate_patient_search.CvPatientSearchAdmin)
admin.site.register(CvPatientDisplayPage, CvPatientDisplayAdmin)
admin.site.register(CAGDataAccessAuditingPage, CAGDataAccessAuditingAdmin)


admin.site.register(PlPatientDisplayPage, PlPatientDisplayAdmin)
admin.site.register(PlClinicalCodeDisplayPage, PlClinicalCodeDisplayAdmin)
admin.site.register(PVClinicalCodeDisplayPage, PVClinicalCodeDisplayAdmin)
admin.site.register(PlGeneralPage, PlGeneralAdmin)
admin.site.register(PlReportingPage, PlReportingPageAdmin)

admin.site.register(PVReportingPage, PVReportingPageAdmin)
admin.site.register(CVReportingPage, CVReportingAdmin)

admin.site.register(ClinicalDomainDemographics, clinical_domain.ClinicalDomainDemograhicsAdmin)
admin.site.register(ClinicalViewerGeneralPage, ClinicalViewerGeneralAdmin)
admin.site.register(ClinicalDomainImaging, clinical_domain.ClinicalDomainImagingAdmin)
admin.site.register(ClinicalDomainDocuments, clinical_domain.ClinicalDomainDocumentsAdmin)
admin.site.register(ClinicalDomainLaboratory, clinical_domain.ClinicalDomainLaboratoryAdmin)
admin.site.register(ClinicalDomainLabResults, clinical_domain.ClinicalDomainLabResultsAdmin)
admin.site.register(DirectMessagingAcdmPage, DirectMessagingAcdmAdmin)
admin.site.register(ClinicalCodeDisplayPage, ClinicalCodeDisplayAdmin)
admin.site.register(OperationalManagerPage, OperationalManagerAdmin)
admin.site.register(DataAccessAuditingPage, DataAccessAuditingAdmin)
admin.site.register(EHRAgentSemanticGroup, EhrAgentSemanticGroupAdmin)
admin.site.register(AgentppHostedAppPage, AgentppHostedAppAdmin)

admin.site.register(CVCCDADisplayPage, CVCCDADisplayAdmin)
admin.site.register(PVCCDADisplayPage, PVCCDADisplayAdmin)
admin.site.register(DataExportCCDADisplayPage, DataExportCCDADisplayAdmin)


admin.site.register(CapsulePage, CapsuleAdmin)
admin.site.register(CarequalityIntegrationSettingsPage, CarequalityIntegrationSettingsPageAdmin)
admin.site.register(ParticipantListBasedPAAModel, ParticipantListBasedPAAAdmin)
admin.site.register(MyHRConnectivityPage, MyHRConnectivityAdmin)
admin.site.register(PatientViewPage, PatientViewPageAdmin)
admin.site.register(PVPatientSearchPage, PVPatientSearchPageAdmin)
admin.site.register(PVPatientDisplayPage, PVPatientDisplayPageAdmin)
admin.site.register(PVClinicalDomainPage, PVClinicalDomainAdmin)

admin.site.register(PVMeasurementPage, PVMeasurementAdmin)

admin.site.register(ChangesHistory, ChangesHistoryAdmin)
admin.site.register(LoginsHistory, LoginsHistoryAdmin)
admin.site.register(DocumentSearchGeneral, DocumentSearchGeneralAdmin)
admin.site.register(DocumentSearchBootstrap, DocumentSearchBootstrapAdmin)
admin.site.register(DocumentSearchLiveFeeds, DocumentSearchLiveFeedsAdmin)

######### code samples ##################################

# https://docs.djangoproject.com/en/1.5/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_overrides 
    #formfield_overrides = {
    #    models.TextField: {'widget': RichTextEditorWidget},
    #}
    
    
    
