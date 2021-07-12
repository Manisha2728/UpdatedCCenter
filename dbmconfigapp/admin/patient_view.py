from dbmconfigapp.models.patient_view import *
from dbmconfigapp.forms import PatientSearchTooltipFormSet, VpoInlineAdminForm
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminTabularInline,get_grid_help_text, dbmBaseAdminStackedInline, dbmBaseAdminStackedInline_Simple
from dbmconfigapp.forms import PatientViewPageForm
from dbmconfigapp.models.collaborate_patient_search import *
from dbmconfigapp.models.vpo import Vpo,VpoCommon,VpoCommunication,VpoPPOL
from dbmconfigapp.forms import VpoCommonInlineAdminForm
from dbmconfigapp.models.vpo import VpoCommon, VpoCommunication, VpoFacilityDisplay,VpoEHRAgentDomains
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdminSaveOnly, dbmBaseAdminStackedInline , get_grid_help_text, dbmBaseAdminTabularInline
from dbmconfigapp.admin.clinical_viewer_general import VpoFacilityDisplayInline
from dbmconfigapp.models.ehragent_clinical_domains import EHRAgentSemanticDelta
from dbmconfigapp.models.ehragent_clinical_domains import EHRAgentBlinks, EHRAgentClinicalDomainsProperties
from dbmconfigapp.forms import EmergencyDeclarationReasonsFormSet, SearchResultGridFormSet 
from django.contrib import admin
from dbmconfigapp.models.ehragent import EhrAgentGeneral
from dbmconfigapp.form.ehragent_forms import VpoEhrAgentDomainsInlineForm
from dbmconfigapp.form.ehragent_forms import EHRAgentBlinksInlineForm, VpoEhrAgentDomainsInlineForm, VitalsInpatientMeasurementForm, EHRAgentClinicalDomainInlineForm, EHRAgentCommonClinicalDomainInlineForm
from dbmconfigapp.models.pl_general import EncounterDiagnosisRelationship
from dbmconfigapp.admin.apps_patient_display import *
from dbmconfigapp.admin.ccda_display import CCDADisplayAdmin_Base
from dbmconfigapp.admin.clinical_domain import ImagingPacsInline

class PVPatientSearchPropertiesInline(dbmBaseAdminStackedInline):
    model = CollaboratePatientSearchProperties
    fieldsets = [(                               
                 'Search by Demographics', {
                 'fields': (                     
                     'MinSQQ',
                     'ContinueSearchAfterSQQCheckFailure',
                     'DemographicSearch_AutoEnter',
                 )
                 , 'classes': ['wide', 'extrapretty']
                 })
                 ] 
class PVVpoCommunicationInline(dbmBaseAdminStackedInline):
    model = VpoCommunication
    fieldsets = [
                 (model._meta.history_meta_label, {'fields': ['is_encounter_conf_inheritance'], 'classes': ['wide', 'extrapretty']}),
                 ]


class PatientViewLoginInline(dbmBaseAdminStackedInline):
    model = PatientViewGeneralDefinitions
    form = PatientViewPageForm
    fieldsets = [
				 ("Login Screen Settings", {'fields': ['default_domain','default_logofile','project_name','background_image'],'classes': ['wide', 'extrapretty']}),
				 #('Login Screen Settings', {'fields': ['default_logofile','project_name','background_image'], 'classes': ['wide', 'extrapretty']}),
				 ] 


# class SpecializedViewsInline(dbmBaseAdminTabularInline):
class SpecializedViewsInline(dbmBaseAdminTabularInline):
    model = SpecializedViews
    fieldsets = [
				 ("Specialized View", {'fields': ['view_name', 'domain_codes_file_name', 'roles']}),
				] 
    verbose_name_plural = "Specialized Views"
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

class PatientsListViewsInline(dbmBaseAdminTabularInline):
    model = PatientsListViews
    list_display = ('patients_list_type','patients_list_label', 'patients_list_order', 'patients_list_roles')
    fields = ('patients_list_type','patients_list_label', 'patients_list_order', 'patients_list_roles')
    readonly_fields = ('patients_list_type',)
    
    class Meta:
        help_text = get_grid_help_text("In standalone mode, My Patient List tabs are only displayed for users with the specified User Role. In addition, users must have a relationship with a patient for the patients to display in a list on a tab. Patient relationships are loaded in the Provider Registry (PPOL) database.")


class PatientViewDafaultLandingInline(dbmBaseAdminStackedInline):
    model = PatientViewDefaultLandingPage
    fieldsets = [
				 ("Patient Summary", {'fields': ['default_page'], 'classes': ['wide', 'extrapretty']}),
				 ] 
 
class PatientViewPageAdmin(dbmModelAdmin):
	model = PatientViewPage
	inlines = (PatientViewLoginInline,PVVpoCommunicationInline,VpoFacilityDisplayInline,PatientViewDafaultLandingInline,SpecializedViewsInline,PatientsListViewsInline)
	# exclude = ('page_help_text', 'page_name', 'services')

class CarequalityIntegrationSettingsInLine(dbmBaseAdminStackedInline):
    model = CarequalityIntegrationSettingsModel
    form = CarequalityIntegrationSettingsForm
    fieldsets = [
				 ("Carequality Integration", {'fields': ['enable_carequality_integration','home_community_id','certificate_thumptrint','patient_discovery_endpoint','find_documents_endpoint','retrieve_document_endpoint'],'classes': ['wide', 'extrapretty']}),
				 #('Login Screen Settings', {'fields': ['default_logofile','project_name','background_image'], 'classes': ['wide', 'extrapretty']}),
				 ] 
    class Media:        
        js = ['admin/js/dbmconfigapp/patientViewCategories.js']

class ParticipantListBasedPAAInLine(dbmBaseAdminTabularInline):
    model = ParticipantListBasedPAAModel
    fieldsets = [
				 ("Settings Per EHR", {'fields': ['healthcare_institude_name','patient_assigning_authority_name','identifier','home_community_id_three_level','participant_list_url'],'classes': ['wide', 'extrapretty']}),
				 #("Participant List Based on PPA", {'fields': ['healthcare_institude_name','patient_assigning_authority_name','identifier','participant_list_url'],'classes': ['wide', 'extrapretty']}),
				 ] 
    readonly_fields = ('participant_list_url',)
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

    class Meta:
        add_link = "/admin/dbmconfigapp/participantlistbasedpaamodel/add/"
        help_text = get_grid_help_text("Define settings per EHR. Administrators can define Carequality participants to query that depend on the EHR used.<br/><br/>Use the Patient Assigning Authority for Display to differentiate between EHRs as configured in CCenter, in Agent Hub -> EHR Integration -> Properties Packages -> Patient Contexts.</br>If Patient Assigning Authority for Display is empty, use Patient Assigning Authority for Resolve. When each EHR instance is registered as a Carequality participant, administrators can define a Home Community ID.</br>The ID identifies the EHR in the SAML assertion that is sent to the Carequality network within outbound queries.</br>If the ID field is left blank for an EHR, the dbMotion <b>Home Community ID</b> is used by default.</br></br>Carequality participants defined in the shared participant list are queried in addition to the Carequality participants defined in the Patient Assigning Authority participant list.")


class ParticipantListInLine(dbmBaseAdminTabularInline):
    model = ParticipantListModel
    fieldsets = [
				 ("Carequality Participant", {'fields': ['paticipant_name','paticipant_identifier'],'classes': ['wide', 'extrapretty']}),
				 #('Login Screen Settings', {'fields': ['default_logofile','project_name','background_image'], 'classes': ['wide', 'extrapretty']}),
				 ] 
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

class ParticipantBaselineListInLine(dbmBaseAdminTabularInline):
    model = ParticipantBaselineListModel
    fieldsets = [
				 ("Carequality Basline Participant", {'fields': ['paticipant_name','paticipant_identifier'],'classes': ['wide', 'extrapretty']}),
				 #('Login Screen Settings', {'fields': ['default_logofile','project_name','background_image'], 'classes': ['wide', 'extrapretty']}),
				 ] 
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

    class Meta:
        help_text = get_grid_help_text("Define a list of Carequality participants to query in an outbound flow.<br/>When users access a patient's Carequality documents in Patient View, all the Carequality participants listed are queried for documents,regardless of the user or patient in context, and regardless of the EHR used.")

class ParticipantListBasedPAAAdmin(dbmModelAdmin):
    model = ParticipantListBasedPAAModel    
    fieldsets = [              
        ('Settings Per EHR',
            {'fields': ['healthcare_institude_name', 'patient_assigning_authority_name', 'identifier','home_community_id_three_level']}),
        ]
    inlines=[ParticipantListInLine, ]
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True  
    
class PrefetchSettingsInLine(dbmBaseAdminStackedInline):
    model = PrefetchSettingsModel
    form = PrefetchSettingsForm
    fieldsets = [
				 ("Prefetch Settings", {'fields': ['enable_prefetch','api_url','api_subscription_key'],'classes': ['wide', 'extrapretty']}),
				] 

class CarequalityIntegrationSettingsPageAdmin(dbmModelAdmin):
	model = CarequalityIntegrationSettingsPage
	inlines = (CarequalityIntegrationSettingsInLine, ParticipantBaselineListInLine, ParticipantListBasedPAAInLine,PrefetchSettingsInLine,)

class PVPatientSearchInline(dbmBaseAdminStackedInline):
    model = CollaboratePatientSearchProperties
    fieldsets = [               
                 ("Search by MRN", 
                 {'fields': ['MRN_label','System_label','PatientSearch_IsDirectEnterPatientFile','PatientSearch_LeadingPatientRecordPolicy'],'classes': ['wide', 'extrapretty','container'],'description':'In Patient View, Patient Search uses the Medical Record Number (MRN) and Electronic Health Record (EHR) system to find a patient. Define the labels for the fields. <br/><br/><i>The default labels are "MRN" and "System". </i>'}),
                ]  

class PatientSearchTooltipsInline(dbmBaseAdminTabularInline):
    model = PatientSearchTooltip
    formset = PatientSearchTooltipFormSet
    fields = ('message', 'culture')
    extra = 1
    verbose_name_plural = "Patient Search Tips"
    
    class Meta:
        help_text = get_grid_help_text("Patient Search service provides Search Tips to facilitate the search process. This configuration enables you to define Patient Search tooltip messages that would be shown to the user when performing a patient search.", 'for culture en-US, 3 tips: "First Name + Last Name + DOB", "SSN + Last Name + Zip Code", "Last Name + Phone + Zip Code".')              
                



class PVEmergencyDeclarationTextInline(dbmBaseAdminStackedInline):
    model = EmergencyDeclarationText
    section_name = 'Emergency Declaration Text'
    fieldsets = (
                 (section_name, {
                 'fields': ('text', ), 
                 'classes': ['wide', 'extrapretty']
                 }),
                 ) 

    
class PVEmergencyDeclarationReasonsInline(dbmBaseAdminTabularInline):
    model = EmergencyDeclarationReasons
    formset = EmergencyDeclarationReasonsFormSet
    fields = ('message', 'culture')
    extra = 1
    verbose_name_plural = "Emergency Declaration Reasons"
    #min_num = 1        # available from Django 1.7 (currently 1.5) - the minimum validation implemented in the FormSet
    

    class Meta:
        help_text = get_grid_help_text("Defines the options displayed in the Reasons for Override dropdown menu. These options can be edited or deleted and new messages can be added. These options can be different per culture. This configuration affects Patient View and Agent Hub.", 'list for culture en-US: "Emergency situation", "Patient gave his consent", The last reason of the of this configuration enables user to enter custom text as reason in application, "Other" is configured by default to be the last in this list.')

class PVVpoPPOLPatientSearchInline(dbmBaseAdminStackedInline):
    model = VpoPPOL
    section_name = 'Search filters'
    fieldsets = (
                 (section_name, {
                 'fields': ('patient_privacy_remove_excluded_clusters', ), 'classes': ['wide', 'extrapretty']
                 }),
                 ) 

class PVPatientSearchDisplayOptionsInline(dbmBaseAdminStackedInline):
    model = PatientSearchDisplayOptions
    fieldsets = (
                  ('User Attestation', {
                  'fields': (
                        'display_user_attestation',
                        'attestation_text',
                             )
                    , 'classes': ['wide', 'extrapretty']
                    }
                  ),
                )

class PVPatientAuthorityInline(dbmBaseAdminStackedInline):
    model = PatientSearchDisplayOptions
    fieldsets = (
                  ('Retry fetching index', {
                  'fields': (                        
                        'authority_text',
                             )
                    , 'classes': ['wide', 'extrapretty']
                    }
                  ),
                )


class DemoSearchFieldsInline(dbmBaseAdminTabularInline):
    model = DemographySearchFields
    fields = ('demo_search_field_label', 'dbm_patient_attribute', 'max_chars')
    extra = 1
    verbose_name_plural = "Specify the Demographic Search Fields"
    
    class Meta:
        help_text = get_grid_help_text("In Patient View, Patient Search can include demographic search fields. Fields can be added, edited, or deleted.","First Name , Last name, Gender, DOB are displayed by default for demographic search.")

class PVSearchResultGridInline(dbmBaseAdminTabularInline):
    model = SearchResultGrid
    formset = SearchResultGridFormSet
    fields = ('label', 'dbMotion_patient_attribute_name','column_order')
    extra = 1
    verbose_name_plural = "Define the Search Results Grid"
   
    class Meta:
        help_text = get_grid_help_text("In Patient View, on the Patient Search page, specify the fields for the Search Results grid. Fields can be added, edited, or deleted.", 'System, Patient Name, DOB, Gender, SSN and Address. Patient Name, DOB, Address and System cannot be deleted, user can update label and order of these fields. User can configure display of Patient name, DOB and Address (Path: Agent Hub <b>-</b> Patient display).')

class PvSearchResultsInline(dbmBaseAdminStackedInline):
    model = PatientSearchDisplayOptions
    fieldsets = (
                  ('Configure Deceased indicator display', {
                  'fields': (                        
                        'enable_death_indicator',
                            )
                    , 'classes': ['wide', 'extrapretty']
                    }
                  ),
                )

class PVPatientSearchPageAdmin(dbmModelAdmin):
    model = PVPatientSearchPage
    inlines = (PVPatientSearchInline,DemoSearchFieldsInline,PVPatientSearchPropertiesInline,PatientSearchTooltipsInline,PVEmergencyDeclarationTextInline, PVEmergencyDeclarationReasonsInline,PVVpoPPOLPatientSearchInline,
    PVPatientSearchDisplayOptionsInline,PVPatientAuthorityInline,PVSearchResultGridInline, PvSearchResultsInline)
    
    class Meta:
        tree_id = 'pv_search_page'
    
    class Media:
        js = ['admin/js/dbmconfigapp/patient_search.js']    

class PvPatientDisplayInline(dbmBaseAdminStackedInline):
    model = AppsPatientDisplay
    fieldsets = [
        ("Patient Address Display",  {'fields': ['collaborate_address_format', 'cv_address_format'], 'classes': ['wide', 'extrapretty'],}),
    ]
    
    verbose_name=""
    verbose_name_plural = "Patient Name Display"     
    
class PVPatientDisplayPageAdmin(dbmModelAdmin):
    model = PVPatientDisplayPage
    inlines = (
               PvPatientNameDisplayInline,PvPatientDisplayInline, AppsPatientDisplayAgeCalculationInline,VpoPatientDisplayForPVInline, VpoPPOLPatientDisplayInline, PatientDisplayMetricCodeBasedIndicatorInline, PatientDisplayVBPInline,PatientDisplayADVDIR,
               PatientDetailsDemographic,
               DemographyInsuranceDisplayInline,
               InsuranceDataElementsInline,    
               PatientDetailsSectionOrderInline           
               )
    class Meta:
        tree_id = 'pv_display_page'
 

class PVClinicalDomainsSemanticDeltaInline(dbmBaseAdminTabularInline):
    model = EHRAgentSemanticDelta
    list_display    = ('display_name', 'enable_semantic_delta')
    fields          = ('display_name', 'enable_semantic_delta')
    readonly_fields = ('display_name', )
                
   
class PVClinicalDomainsGeneralDefinitions(dbmBaseAdminStackedInline):
    model = EhrAgentGeneral
    #form = EhrAgentGeneralInlineForm
    fieldsets = [
        ('Display Options',{'fields': ['my_ehr_data_default_view',]}),
        ]
    
    radio_fields = {'my_ehr_data_default_view': admin.VERTICAL}
    
class PVClinicalDomainsPropertiesInline(dbmBaseAdminTabularInline):
    model = EHRAgentClinicalDomainsProperties
    form = EHRAgentClinicalDomainInlineForm
    list_display    = ('display_name', 'attention_searching_time', 'attention_searching_option', 'default_attention_time')
    fields          = ('display_name', 'attention_searching_time','attention_searching_option', 'default_attention_time')
    readonly_fields = ('display_name','default_attention_time')
    
    class Meta:
        help_text = get_grid_help_text('This configuration enables the user to define the time period for calculating the displayed Badging in the Agent Hub and Patient View.<br/>Clinical data available within this defined time period (for example, the past 7 days) activates the applications Badging mechanism.<br/>To disable the Badging, set the Attention Time Unit to Off.<br/>The Badging displays clinical data updates. For more information, see the relevant chapter in the Agent Hub/Patient View Functional Specification.<br/>Note that Semantic Delta configuration applies not only to badging but also to the data displayed in the Clinical View Agent/Patient View application.<br/>For optimal performance, it is recommended to limit this configuration to a maximum period of 7 days. A value greater than 7 days might result in reduced performance.')

class PVVpoEhrAgentDomainsInline(dbmBaseAdminStackedInline):
    model = VpoEHRAgentDomains
    form = VpoEhrAgentDomainsInlineForm
    fields		= ['filter_codes']
    template	= 'admin/edit_inline/stacked.html'
    verbose_name_plural = 'Filtering Out Clinical Data'

    def queryset(self, request):
        qs = super(PVVpoEhrAgentDomainsInline, self).queryset(request)
        return qs.exclude(clinical_domain_id=11)

class PVVpoEhrAgentDomainsProceduresInline(dbmBaseAdminStackedInline_Simple):
    model = VpoEHRAgentDomains
    form = VpoEhrAgentDomainsInlineForm
    fields = ['filter_type', 'filter_codes',]
    verbose_name_plural = 'Filtering Procedures by type'
    
    def queryset(self, request):
        qs = super(PVVpoEhrAgentDomainsProceduresInline, self).queryset(request)
        return qs.filter(clinical_domain_id=11)

field_description = 'This configuration determines the values used for Primary and Admitting Diagnoses in the encounter-condition act-relationship (Field name: PriorityNumber).<br>The values are used as part of the logic that determines the display of the Encounter Diagnosis (or Encounter Reason) in the dbMotion clinical applications (for example, the data displayed in Discharge Diagnosis or the Admitted Reason fields).<br>The configuration is required since different values may be used depending on the customer location (for example, in the American market the values are Admitting=0 and Primary=1 while in the Israeli market the values are Primary=1, 6 and Other=0, while there is no value for Admitting) and on the specific field in the application.<br>This configuration affects EHR Agent, Patient List and Patient View. For a detailed description of the business logic, see the Functional Specification documentation.'

class PVEncounterDiagnosisRelationshipInline(dbmBaseAdminStackedInline):
    model = EncounterDiagnosisRelationship
    fieldsets = [
                 (model._meta.history_meta_label, {'fields': ['primary_diagnosis', 'admitted_diagnosis'], 'description' : field_description, 'classes': ['wide', 'extrapretty']}),
                 ]    
       
    
    verbose_name_plural = model._meta.history_meta_label
      
    class Meta:
        help_text = get_grid_help_text('Help goes here and can be formatted to whatever we want')

class PVClinicalDocumentsInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = PvVpoInlineAdminForm
    fieldsets = (
                 ('Grouping Priority Order', {
                 'fields': ('grouping_mode',)
                 }),
                 )
    radio_fields = {'grouping_mode': admin.VERTICAL}

    def get_queryset(self, request):
        query = super(PVClinicalDocumentsInline, self).get_queryset(request)
        return query.filter(clinical_domain_id=18)

class PVImagingInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = PvVpoInlineAdminForm
    fieldsets = (
                 ('', {
                 'fields': ('grouping_mode',)
                 }),
                 )
    radio_fields = {'grouping_mode': admin.VERTICAL}

    def get_queryset(self, request):
        query = super(PVImagingInline, self).get_queryset(request)
        return query.filter(clinical_domain_id=17)


class PVClinicalCategoriesInline(dbmBaseAdminTabularInline):
    model = PVCategoriesProperties
    fields = ('category_name_url', 'display_name','hide_fields','category_order', 'expand_by_default')

    readonly_fields = ('category_name_url',)
    ordering        = ('category_order',)
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    class Media:        
        js = ['admin/js/dbmconfigapp/patientViewCategories.js']
    class Meta:
        add_link = "/admin/dbmconfigapp/pvcategoriesproperties/add/"

class PVClinicalCategoriesAdmin(dbmModelAdmin):
    model = PVCategoriesProperties
    fields = ('category_name', 'display_name', 'category_order', 'nodes', 'information_text', 'roles', 'time_frame')

    readonly_fields = ('category_name',)
    ordering        = ('category_order',)
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

    class Media:        
        js = ['admin/js/dbmconfigapp/patientViewCategories.js']

class PVCCDADisplayAdmin(CCDADisplayAdmin_Base):
    model = PVCCDADisplayPage

class PVDocumentsPropertiesInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 ('External Documents', {
                 'fields': ('ClinicalDocument_ShowExternalDocumentsLabel','disclaimer')
                 }),
                 )
    form = PvDocumentsDomainPropertiesAdminForm

class PVOverrideDisclosureDirectiveInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 ('Override Disclosure Directive', {
                 'fields': ('ClinicalDocument_DD_ResetPasskey', 
                            'ClinicalDocument_DD_ProviderPolicy_URL', 
                            'ClinicalDocument_DD_PatientPolicy_URL',
                            'ClinicalDocument_DD_OverrdieWithoutConsentOrgPolicy_URL'
                            ),
                  'description': 'A Disclosure Directive is a patient privacy authorization directive, under the Canadian healthcare regulations (in British Columbia), which enables a patient to choose who can access information within the patient\'s electronic health record. If a patient applies a Disclosure Directive on the patient record, the patient\'s clinical data is hidden and cannot be viewed by the healthcare provider. However, under certain conditions, it is possible to override the Disclosure Directive.<br>This configuration defines the Help links available in the Disclosure Directive Override Page.<br><b>Note: The Disclosure Directive feature is relevant only for External Documents that might require the Disclosure Directive override process to view the patient record.</b>'                                                    
                 }),
                 )
    form = PVOverrideDisclosureDirectiveAdminForm

class PVFirstDayOfAdmissionInline(dbmBaseAdminStackedInline):
    model= EHRAgentBlinks
    form= EHRAgentBlinksInlineForm
    fieldsets=(
                 (model._meta.history_meta_label, {
                 'fields': ['admission_interval', 'admission_inpatient_domains'],
                 'classes': ['wide', 'extrapretty'] }),
                 )

class ImagingPacsDisclaimerInline(dbmBaseAdminStackedInline):
    model = ImagingPacsDisclaimer    
    fieldsets = (
                 ('Imaging', {
                 'fields': ('Pacs_Disclaimer_Text','Grouping_by_Modality') }),
                 )
    form = PvImagingPacsDisclaimerAdminForm

class PVBusinessRulesInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = PvVpoBusinessRulesInlineAdminForm
    fieldsets = (
                 ('BusinessRules', {
                 'fields': ('encounters_remove_duplicated',) }),
                 )

    def get_queryset(self, request):
        query = super(PVBusinessRulesInline, self).get_queryset(request)
        return query.filter(clinical_domain_id=8)

class PVClinicalDomainAdmin(dbmModelAdmin):
    model = PVClinicalDomainPage
    inlines = (PVClinicalDomainsPropertiesInline,PVFirstDayOfAdmissionInline,PVClinicalDomainsSemanticDeltaInline, PVClinicalDomainsGeneralDefinitions, PVVpoEhrAgentDomainsInline, PVVpoEhrAgentDomainsProceduresInline, PVEncounterDiagnosisRelationshipInline, PVBusinessRulesInline, PVClinicalDocumentsInline, PVImagingInline
               ,PVClinicalCategoriesInline,PVDocumentsPropertiesInline,PVOverrideDisclosureDirectiveInline, ImagingPacsInline, ImagingPacsDisclaimerInline)


