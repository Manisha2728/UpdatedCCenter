from django.contrib import admin
from dbmconfigapp.models.apps_patient_display import *
from dbmconfigapp.models.cv_patient_display import CvPatientDisplayPage
from dbmconfigapp.models.apps_patient_display import *
from dbmconfigapp.models.vpo import Vpo, VpoPPOL
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, get_grid_help_text, dbmBaseAdminStackedInline, dbmBaseAdminTabularInline, dbmBaseModelAdmin,dbmBaseAdminStackedInline_Simple, dbmBaseInline,dbmBaseAdminTabularSimple
from dbmconfigapp.forms import VpoPatientDisplayInlineAdminForm, VpoPPOLInlineAdminForm, AppsPatientDisplayVBPForm, AppsPatientDisplayMetricCodeBasedIndicatorForm, MinimumOneFormSet
from dbmconfigapp.models.cvtables import DemographicsDetailsDEGrid, InsuranceDataElement
from dbmconfigapp.admin.clinical_domain import ClinicalDomainDataElementsInline,ClinicalDomainDataElementsSimpleInline, ClinicalDomainProperties, ClinicalDomainDataElementsInline_WithReport
from dbmconfigapp.forms import * 
class PatientDisplayADVDIR(dbmBaseAdminStackedInline):
    model = AppsAdvanceDirectiveNodes
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ['adv_dir','nodes']
                    , 'classes': ['wide', 'extrapretty'],'description':'Advance Directive is a document by which a person makes provision for health care decisions in the event that, in the future, he/she becomes incapable of making these decisions. When this document exists (the document type code is located in the Advance Directive vocabulary subdomain), a textual indication is displayed in the Agent Hub header.'
                 }),
                 ) 
        

class PatientDisplayCommonInline(dbmBaseAdminStackedInline):
    model = AppsPatientDisplayCommon
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ['is_display_patient_mrn','is_display_patient_mrn_report']
                    , 'classes': ['wide', 'extrapretty']
                 }),
                 ) 

class PatientDisplayInline(dbmBaseAdminStackedInline):
    model = AppsPatientDisplay
    fieldsets = [
        ("Patient Name Display - Patient Search",               {'fields': ['patient_search_name_format'], 'classes': ['wide', 'extrapretty'],}),
        ("Patient Address Display",            {'fields': ['collaborate_address_format', 'cv_address_format'], 'classes': ['wide', 'extrapretty'],}),
        #("Patient Phone Number Format",        {'fields': ['phone_format'], 'classes': ['wide', 'extrapretty'],}),
    ]
    
    verbose_name=""
    verbose_name_plural = "Patient Name Display"
    

class PatientDisplayWithAgentInline(dbmBaseAdminStackedInline):
    model = AppsPatientDisplayWithAgent
    fieldsets = [
        ("Patient Name Display - Patient Header",               {'fields': ['patient_name_format'], 'classes': ['wide', 'extrapretty'],}),
        ]
    

class VpoPatientDisplayInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoPatientDisplayInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('patient_id_type_display_priority', 
                            'patient_privacy_indicate_minority', 'patient_privacy_minor_min',
                            'patient_privacy_minor_max'), 'classes': ['wide', 'extrapretty']
                 }),
                 )

class VpoPatientDisplayForPVInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoPatientDisplayInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('pv_patient_id_type_display_priority', 
                            'patient_privacy_indicate_minority', 'patient_privacy_minor_min',
                            'patient_privacy_minor_max'), 'classes': ['wide', 'extrapretty']
                 }),
                 )                 
    
class VpoPPOLPatientDisplayInline(dbmBaseAdminStackedInline):
    model = VpoPPOL
    form = VpoPPOLInlineAdminForm
    section_name = 'Display SSN'
    fieldsets = (
                 (section_name, {
                 'fields': ( 'patient_privacy_mask_ssn',), 'classes': ['wide', 'extrapretty']
                 }),
                 )
    

class AppsPatientDisplayAgeCalculationInline(dbmBaseAdminTabularInline):
    model= AppsPatientDisplayAgeCalculation
    verbose_name_plural = 'Patient Age Display'
 
    #readonly_fields = ('display_text',)   
    list_display    = ('age_calc_time_span', 'date_format', 'priority_order')
    fields    = ('age_calc_time_span', 'date_format', 'priority_order')
    ordering        = ('priority_order',)
    formset = MinimumOneFormSet
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

    class Meta:
        help_text = get_grid_help_text("This configuration defines the calculation used to display different age groups in the clinical applications. Each age group is defined by an Age Range calculated by defining the upper value of the range.<br/>Patient Age Range Upper Value: Defines the Upper Value used to define an age group, for example, 6 years.<br/>The Lower Value of this group is automatically calculated as equal to the Upper Value configured for the age group below this group, for example 30 months.<br/>In this example, the Age Range for this group is 30 months to 6 years.")

class PatientDisplayValueBaseProgramInline(dbmBaseAdminStackedInline):
    model = AppsPatientDisplayValueBaseProgram
    fieldsets = (
                 ('Displayed Risk Scores', {
                 'fields': [('vbp_low_risk_score','vbp_medium_risk_score','vbp_high_risk_score','vbp_very_high_risk_score'), 'vbp_risk_score_code']
                    , 'classes': ['wide', 'extrapretty'], 'description':'Determines the Risk Score level(s) which will be displayed to the user in the EHR Agent and Clinical Viewer header.<b> The Risk Score level is determined based on the assigned sub-domain of the risk score interpretation code.</b><br/>One or more of the following 4 levels can be displayed: Low, Medium, High, and Very High.<br/>Only the latest metric from the selected Risk Score will be displayed.'
                 }),
                ) 

            
class PatientDisplayVBPInline(dbmBaseAdminTabularInline):
    model= AppsPatientDisplayVBP
    form= AppsPatientDisplayVBPForm
    verbose_name_plural = model._meta.history_meta_label
 
    #readonly_fields = ('display_text',)   
    list_display = ('vbp_oid_system', 'vbp_display_name_long', 'vbp_description')
    fields = ('vbp_oid_system', 'vbp_display_name_long', 'vbp_description')
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

    class Meta:
        help_text = get_grid_help_text("A Value Based Program (VBP) is a program provided by an organization of health care providers (for example, an ACO) that agrees to be accountable for the quality, cost, and overall care of patients who are assigned to it.<br/>dbMotion Clinical Viewer and Patient View (but not Collaborate) applications display an indication for patients that are registered in a VBP in the application header. This configuration is used to define all the VBPs in an organization. A patient can belong to multiple VBPs but only one program is displayed for a  patient in the application. The order of the configured VBPs configured here determines the priority order for display of the VBP in the application. If a patient belongs to multiple VBPs, the patient's VBP with the highest priority will be displayed in the application header.<br/><br/><br/>The System OID field can also be structured as MetricCodeSystem|MetricCode|InterpretationDomain to be displayed as a metric-based indicator. For example: 2.16.840.1.113883.3.57.1.2.17.89|0006|Interpretation_VeryHigh<br><br>The display of metric-based indicators takes precedence over indicators without metric codes. If there are multiple metric-based indicators, then the most recent one will be displayed, regardless of the configured order in CCenter. If the most recent metric-based indicator is not configured for display, then no metric-based indicator will be displayed. This configuration applies to Clinical Viewer only.")   


class PatientDisplayMetricCodeBasedIndicatorInline(dbmBaseAdminTabularInline):
    model= AppsPatientDisplayMetricCodeBasedIndicator
    form= AppsPatientDisplayMetricCodeBasedIndicatorForm
    verbose_name_plural = model._meta.history_meta_label
 
    #readonly_fields = ('display_text',)   
    list_display = ('mci_oid_system', 'mci_interpretation', 'mci_label', 'mci_priority', 'mci_tooltip')
    fields = ('mci_oid_system', 'mci_interpretation', 'mci_label', 'mci_priority', 'mci_tooltip')
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

    class Meta:
        help_text = get_grid_help_text("This configuration determines the Indicators to display on the banner based on the metric code and its interpretation combination that is configured here. One Metric code can be configured to display different indicators based on the interpretation code. An Indicator's metric code and interpretation code should be unique. Multiple metric codes can be configured to display as indicators on the banner. No metric code is configured out of the box. This configuration applies to: Agent Hub, Patient View and CVA.")   

class PvPatientNameDisplayInline(dbmBaseAdminTabularInline):
    model = PvPatientNameDisplay
    form = PvPatientNameDisplayForm
    verbose_name_plural = model._meta.history_meta_label

    list_display = ('pv_patient_name_display')
    fields = ('pv_patient_name_display',)


    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    class Meta:
        help_text = get_grid_help_text("This configuration defines the display name of the patient in patient view application. The attributes configured under initiate mappings should be used to define the display name and the order of the display name parts.")


class PatientDetailsDemographic(ClinicalDomainDataElementsInline):
    verbose_name_plural = "Patient Details"
    model = DemographicsDetailsDEGrid
    list_display = ('enable', 'name',)
    fields = ('enable', 'name',)
    formset = BaseInlineFormSet
    class Meta:
        help_text = get_grid_help_text("Demography Details Grid Display Options") + "This configuration is supported by Agent hub."  
       
    class Media:
        js = ['admin/js/dbmconfigapp/patient_display.js'] 


class DemographyInsuranceDisplayInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fields = ('demography_display_insurances_grid',)

class InsuranceDataElementsInline(ClinicalDomainDataElementsSimpleInline):
    model = InsuranceDataElement
    list_display = ('enable', 'name', )
    fields = ('enable', 'name',)
    verbose_name_plural = 'Insurance Grid Display Options'
    formset = BaseInlineFormSet
    class Meta:
        help_text = get_grid_help_text("Insurance Grid Display Options")
      
class PatientDetailsSectionOrderInline(dbmBaseAdminTabularSimple):
    model = PatientDetailsSectionOrdering
    list_display = ('display_name','priority_order')
    fields = ('display_name','priority_order')
    formset = BaseInlineFormSet
    readonly_fields = ('display_name',)
    
    class Meta:
        help_text = get_grid_help_text("Section Display Order<br/>You can configure the way that the Patient details section are displayed in Agent hub.") 

class PatientDisplayAdmin(dbmModelAdmin):
    inlines = (
               PatientDisplayCommonInline, PatientDisplayWithAgentInline, PatientDisplayInline, AppsPatientDisplayAgeCalculationInline, VpoPatientDisplayInline, VpoPPOLPatientDisplayInline, PatientDisplayValueBaseProgramInline, PatientDisplayVBPInline,PatientDisplayADVDIR
               )

class CvPatientDisplayAdmin(PatientDisplayAdmin):
    model = CvPatientDisplayPage
    
class PlPatientDisplayAdmin(dbmModelAdmin):
    model = PlPatientDisplayPage
    inlines = (
               PatientDisplayWithAgentInline, PatientDisplayInline, AppsPatientDisplayAgeCalculationInline, VpoPatientDisplayInline, VpoPPOLPatientDisplayInline, PatientDisplayValueBaseProgramInline, PatientDisplayVBPInline,PatientDisplayADVDIR,
               PatientDetailsDemographic,
               DemographyInsuranceDisplayInline,
               InsuranceDataElementsInline,    
               PatientDetailsSectionOrderInline           
               )


    
