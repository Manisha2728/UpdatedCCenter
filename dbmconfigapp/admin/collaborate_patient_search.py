from django.contrib import admin

from dbmconfigapp.models.collaborate_patient_search import *
from dbmconfigapp.admin.clinical_domain import DataElementFormSet
from dbmconfigapp.forms import ClinicalDomainDataElementsAdminForm, EmergencyDeclarationReasonsFormSet, PatientSearchTooltipFormSet, VpoInlineAdminForm
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline, get_grid_help_text, dbmBaseAdminTabularInline
from dbmconfigapp.models.vpo import Vpo, VpoPPOL
from dbmconfigapp.forms import PatientSearchDisplayOptionsInlineForm, PatientSearchDefaultSearchInlineForm


class CollaboratePatientSearchPropertiesInline(dbmBaseAdminStackedInline):
    model = CollaboratePatientSearchProperties
    fieldsets = (
                 ('Search by MRN', {
                 'fields': (
                     'MrnSystemSelectorMaxDropItems',
                     'MrnSystemSelectorMaxColumnCount',
                     'MrnSystemSelectorIsSortingEnabled',
                     'PatientSearch_IsDirectEnterPatientFile',
                     'PatientSearch_IsDirectEnterPatientFile_Demographics',
                     'PatientSearch_IsDirectEnterPatientFile_Demographics_MinScore',
                     'LeadingPatientRecordPolicy'                
                 ),'description' : 'This configuration defines how to display the MRN System Selector dropdown list used in the Patient Search feature. The user can search for the patient either by entering demographic data or by entering the MRN. If the MRN is entered, a dropdown list appears which enables the user to select and filter for the relevant MRN System. The display of the MRN System Selector dropdown list can be configured with these configuration points.<br><br>This configuration applies to:<ul><li>Collaborate Patient Search</li><li>Clinical Viewer Patient Search</li></ul>'
                 , 'classes': ['wide', 'extrapretty']
                 }),                 
                 ('Search by Demographics', {
                 'fields': (                     
                     'MinSQQ',
                     'ContinueSearchAfterSQQCheckFailure',
                 )
                 , 'classes': ['wide', 'extrapretty']
                 })
                 )

class CollaboratePatientSearchDataElementsInline(dbmBaseAdminTabularInline):
    form = ClinicalDomainDataElementsAdminForm  
    formset = DataElementFormSet
    list_display    = ('enable', 'name', 'page_width', 'default_width', 'order')
    fields          = ('enable', 'name', 'page_width', 'default_width', 'order')
    ordering        = ('order',)
    
    def get_readonly_fields(self, request, obj = None):
#        if not request.user.is_superuser:
        return ('name', 'default_width',) + self.readonly_fields
#         return self.readonly_fields

class PatientSearchResultsInline(CollaboratePatientSearchDataElementsInline):
    model = PatientSearchDataElement
    verbose_name_plural = "Patient Search Results Grid Display Options"

class PatientSearchResultsHistoryInline(CollaboratePatientSearchDataElementsInline):
    model = PatientSearchHistoryDataElement
    verbose_name_plural = "Patient Search Results - Patient File History Grid Display Options"

class PatientSearchDisplayOptionsInline(dbmBaseAdminStackedInline):
    model = PatientSearchDisplayOptions
    form = PatientSearchDisplayOptionsInlineForm
    #fields = ('display_warning',)
    #verbose_name_plural = "Display Options"
    fieldsets = (
                 ('Display Options', {
                  'fields': (
                        'display_warning',
                        'cluster_selection_behavior',
                             )
                    , 'classes': ['wide', 'extrapretty']
                    }
                  ),)
    radio_fields = {'cluster_selection_behavior': admin.VERTICAL}

class VpoPPOLPatientSearchInline(dbmBaseAdminStackedInline):
    model = VpoPPOL
    section_name = 'Search filters'
    fieldsets = (
                 (section_name, {
                 'fields': ('patient_privacy_remove_excluded_clusters', ), 'classes': ['wide', 'extrapretty']
                 }),
                 ) 
        
class VpoPatientSearchInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('facility_filter_enable', 'user_facility_root_oid'), 'classes': ['wide', 'extrapretty']
                 }),
                 ) 


class EmergencyDeclarationTextInline(dbmBaseAdminStackedInline):
    model = EmergencyDeclarationText
    section_name = 'Emergency Declaration Text'
    fieldsets = (
                 (section_name, {
                 'fields': ('text', ), 
                 'classes': ['wide', 'extrapretty']
                 }),
                 ) 

    
class EmergencyDeclarationReasonsInline(dbmBaseAdminTabularInline):
    model = EmergencyDeclarationReasons
    formset = EmergencyDeclarationReasonsFormSet
    fields = ('message', 'culture')
    extra = 1
    verbose_name_plural = "Emergency Declaration Reasons"
    #min_num = 1        # available from Django 1.7 (currently 1.5) - the minimum validation implemented in the FormSet
    
    
    class Meta:
        help_text = get_grid_help_text("Defines the options displayed in the Reasons for Override dropdown menu. These options can be edited or deleted and new messages can be added. These options can be different per culture. This configuration affects Clinical Viewer, Collaborate and Agent Hub.<br/>", 'list for culture en-US: "Emergency situation", "Patient gave his consent".')
    
class PatientSearchTooltipsInline(dbmBaseAdminTabularInline):
    model = PatientSearchTooltip
    formset = PatientSearchTooltipFormSet
    fields = ('message', 'culture')
    extra = 1
    verbose_name_plural = "Patient Search Tooltips"
    
    class Meta:
        help_text = get_grid_help_text("Patient Search service provides Search Tips to facilitate the search process. This configuration enables you to define Patient Search tooltip messages that would be shown to the user when performing a patient search.", 'for culture en-US, 3 tips: "First Name + Last Name + DOB", "SSN + Last Name + Zip Code", "Last Name + Phone + Zip Code".')
    
class PatientSearchDefaultSearchInline(dbmBaseAdminStackedInline):
    model = PatientSearchDefaultSearch
    form = PatientSearchDefaultSearchInlineForm
    
    fieldsets = (('Default Patient Search', {
                        'fields': ('default_search',),
                        'description' : 'This configuration allows to select the default type of the patient search method.'
                    }),
                )
    
    radio_fields = {'default_search': admin.VERTICAL}
 
class PatientSearchAdmin(dbmModelAdmin):
    inlines = (CollaboratePatientSearchPropertiesInline, PatientSearchResultsInline, PatientSearchResultsHistoryInline, PatientSearchDisplayOptionsInline, VpoPPOLPatientSearchInline, VpoPatientSearchInline, EmergencyDeclarationTextInline, EmergencyDeclarationReasonsInline, PatientSearchTooltipsInline, PatientSearchDefaultSearchInline)
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id', )

    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
        js = ['admin/js/dbmconfigapp/patient_search.js']         
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
   
class CvPatientSearchAdmin(PatientSearchAdmin):
    model = CvPatientSearch   
    