from django.contrib import admin
from dbmconfigapp.models.cvtables import *
from dbmconfigapp.models.ehragent_clinical_domains import EHRAgentCVCommonClinicalDomainsProperties
from dbmconfigapp.forms import * 
from decimal import Decimal
from .dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline, get_grid_help_text, dbmBaseAdminTabularInline,dbmBaseAdminStackedInline_Simple, dbmBaseAdminTabularSimple
from dbmconfigapp.models.vpo import VpoEHRAgentDomains
from dbmconfigapp.form.ehragent_forms import VpoEhrAgentDomainsInlineForm
from dbmconfigapp.admin.ehragent_clinical_domains import VitalsInpatientMeasurementInline
from dbmconfigapp.models.ehragent_measurements import PVMeasurementPage, EHRAgentSemanticGroup

class DataElementFormSet_WithReport(BaseInlineFormSet):
    '''
    Validate formset data here
    '''
    
    def clean(self):
        super(DataElementFormSet_WithReport, self).clean()
        
        
        error_less_than_one = u"Ensure this value is greater than or equal to 1."
        error_more_than_2_digits_before_point = u"Ensure that there are no more than 2 digits before the decimal point."
        error_more_than_2_digits_after_point = u"Ensure that there are no more than 2 decimal places."
        
        hide_uom = []
        concat_values = []
                
        width = float(0.0)
        is_valid = True
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            is_valid = is_valid and form.is_valid()
            data = form.cleaned_data
            enabled = data.get('enable')
            if enabled and form.is_valid():
                page_width = data.get('page_width', float(0.0))
                width += page_width
                if page_width < 1.0:
                    form._errors['page_width'] = ErrorList([error_less_than_one])
                elif page_width >= 100.0:
                    form._errors['page_width'] = ErrorList([error_more_than_2_digits_before_point])
                elif float(format(page_width, '.2f')) != page_width:
                    form._errors['page_width'] = ErrorList([error_more_than_2_digits_after_point])
            if type(self.instance) == ClinicalDomainVitals:
                if data.get('hide_uom'):
                    hide_uom.append(data.get('name'))
                if data.get('concatenate_values'):
                    concat_values.append(data.get('name'))
        
        if type(self.instance) == ClinicalDomainVitals:
            cv = ClinicalDomain.objects.get(clinical_view_name=self.instance)
            vpo_vitals = Vpo.objects.get(clinical_domain=cv)    # vitals id = 13
            vpo_vitals.domains_to_hide_uom = ','.join(hide_uom)
            vpo_vitals.domains_to_concatenate_values = ','.join(concat_values)
            vpo_vitals.save()

        if width < 100.0 and is_valid:
            raise ValidationError('Total page width must be 100 or higher. Current page width is ' + str(width))

        width = float(0.0)
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            enabled = data.get('enable')
            if enabled:
                report_width = data.get('report_width', float(0.0))
                width += report_width
                if (report_width < 1.0):
                    if not (("_info" in data.keys()) and ("ignore-report-width-0" in data.get('_info'))):
                        form._errors['report_width'] = ErrorList([error_less_than_one])
                elif report_width >= 100.0:
                    form._errors['report_width'] = ErrorList([error_more_than_2_digits_before_point])
                elif float(format(report_width, '.2f')) != report_width:
                    form._errors['report_width'] = ErrorList([error_more_than_2_digits_after_point])
        if width != 100.0:
            raise ValidationError('Total report width must be equal to 100. Current report width is ' + str(width))
        


class DataElementFormSet(BaseInlineFormSet):
    '''
    Validate formset data here
    '''

    def clean(self):
        super(DataElementFormSet, self).clean()

        width = float(0.0)
        is_valid = True
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            enabled = data.get('enable')
            if enabled and form.is_valid():
                page_width = data.get('page_width', float(0.0))
                width += page_width
                if page_width < 1.0:
                    form._errors['page_width'] = ErrorList([u"Ensure this value is greater than or equal to 1."])
                elif page_width >= 100.0:
                    form._errors['page_width'] = ErrorList([u"Ensure that there are no more than 2 digits before the decimal point."])
                elif float(format(page_width, '.2f')) != page_width:
                    form._errors['page_width'] = ErrorList([u"Ensure that there are no more than 2 decimal places."])
        if width < 100.0 and is_valid:
            raise ValidationError('Total page width must be 100 or higher. Current page width is ' + str(width))

########################################################

class ClinicalDomainDataElementsInline(dbmBaseAdminTabularInline):
    verbose_name = "Grid Display Option"
    verbose_name_plural = "Grid Display Options"
    model = DataElement
    form = ClinicalDomainDataElementsAdminForm  
    formset = DataElementFormSet
    list_display    = ('enable', 'name', 'page_width', 'default_width', 'order')
    fields          = ('enable', 'name', 'page_width', 'default_width', 'order')
    ordering        = ('order',)
    
    def get_readonly_fields(self, request, obj = None):
#        if not request.user.is_superuser:
        return ('name', 'default_width',) + self.readonly_fields
#         return self.readonly_fields
    
    
class ClinicalDomainDataElementsSimpleInline(dbmBaseAdminTabularSimple):
    verbose_name = "Grid Display Option"
    verbose_name_plural = "Grid Display Options"
    model = DataElement
    form = ClinicalDomainDataElementsAdminForm  
    formset = DataElementFormSet
    list_display    = ('enable', 'name', 'page_width', 'default_width', 'order')
    fields          = ('enable', 'name', 'page_width', 'default_width', 'order')
    ordering        = ('order',)
    
    def get_readonly_fields(self, request, obj = None):
#        if not request.user.is_superuser:
        return ('name', 'default_width',) + self.readonly_fields
#         return self.readonly_fields

    
class ClinicalDomainPropertiesInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    

class ClinicalDomainPropertiesInline_TimeFilter(dbmBaseAdminStackedInline):
    model = EHRAgentCVCommonClinicalDomainsProperties
    fieldsets = (
                 ('Time Range Filter', {
                 'fields': (('default_searching_time', 'default_searching_option'),)
                 }),
                 )

class ClinicalDomainPropertiesInline_DisplayOptions(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 ('Display Options', {
                 'fields': (('show_cancelled_display', 'show_cancelled_selected'), 
                            ('grouped_by_display', 'grouped_by_selected'))
                 }),
                 ) 


class AllergiesPropertiesInline(ClinicalDomainPropertiesInline_DisplayOptions):
    form = AllergiesDomainPropertiesAdminForm

class AllergiesTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = AllergiesDomainTimeFilterAdminForm

class ClinicalDomainAdmin(dbmModelAdmin):
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id')

    class Media:
        js = ['admin/js/dbmconfigapp/clinical_domains.js'] 



######### base classes ##################################
#from django.contrib.admin.options import InlineModelAdmin



################## VPO ######################################

class VpoEhrAgentDomainsFilteringInline(dbmBaseAdminStackedInline_Simple):
    model = VpoEHRAgentDomains
    form = VpoEhrAgentDomainsInlineForm
    fields = ['filter_codes',]


class VpoProblemsInline(dbmBaseAdminStackedInline):
    model = Vpo
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('filter_status_code', 'filter_cancelled_items')
                 }),
                 ) 
    form = VpoProblemsInlineAdminForm
    formfield_overrides = {
         models.TextField: {'widget': forms.Textarea(attrs={'rows':4, 'cols':100})},
         }
    
class VpoDiagnosisInline(dbmBaseAdminStackedInline):
    model = Vpo
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('filter_status_code', 'filter_cancelled_items')
                 }),
                 ) 
    form = VpoDiagnosisInlineAdminForm

    
class VpoClinicalDocumentsInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('medical_staff_types_priority', )
                 }),
                 ('Grouping', {
                 'fields': ('grouping_mode',)
                 }),
                 )
    radio_fields = {'grouping_mode': admin.VERTICAL}
    
class VpoImagingInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoImagingInlineAdminForm    
    fieldsets = (
                 ('Grouping', {
                 'fields': ('grouping_mode',)
                 }),
                 )
    radio_fields = {'grouping_mode': admin.VERTICAL}
    

class VpoSummaryInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoSummaryInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('encounter_types_to_display', 'summary_med_filter_undefined_status', 'filter_status_code')
                            , 'classes': ['wide', 'extrapretty']},),
                  (None, {
                 'fields': (
                            'summary_top_encounters', 'summary_top_allergy_intolerance',
                            'summary_top_conditions', 'summary_top_laboratory_events',
                            'summary_top_substance_administration'), 'classes': ['wide', 'extrapretty']
                 }),
                  (None, {
                 'fields': (
                            ('summary_time_filter_amount_labs', 'summary_time_filter_unit_labs'),
                            ('summary_time_filter_amount_encounter', 'summary_time_filter_unit_encounter'),
                            ('summary_time_filter_amount_meds', 'summary_time_filter_unit_meds'),
                            ), 'classes': ['wide', 'extrapretty']
                 }),
                 )
    formfield_overrides = {
         models.TextField: {'widget': forms.Textarea(attrs={'rows':4, 'cols':100})},
         }

class VpoEncountersInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('encounters_enable_episode_filter',
                            'encounters_emergency_threshold')
                 }),
                 )

class VpoEncounterDetailsInline(dbmBaseAdminStackedInline):
    model = Vpo
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('encounters_remove_duplicated', )
                 }),
                 )

class VpoImmunizationsInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoImmunizationsInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('filter_mood_codes', 'filter_status_code')
                 }),
                 )
    formfield_overrides = {
         models.TextField: {'widget': forms.Textarea(attrs={'rows':4, 'cols':100})},
         }
    
    
class VpoLabResultsInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('lab_susceptibility_methods_code_type',)
                 }),
                 ) 
    
    radio_fields = {'lab_susceptibility_methods_code_type': admin.VERTICAL}
    
class VpoDemographyInline(dbmBaseAdminStackedInline):
    model = Vpo
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('patient_name_type_priority',)
                 }),
                 )

class VpoVitalsInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoVitalsInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('unit_priority_list_body_weight', 'unit_priority_list_body_height')
                 }),
                 )
    formfield_overrides = {
         models.TextField: {'widget': forms.Textarea(attrs={'rows':4, 'cols':100})},
         }

class VpoCommonInline(dbmBaseAdminStackedInline):
    model = VpoCommon
    form = VpoCommonInlineAdminForm
    section_name = 'Code System Display'
    fieldsets = (
                 (section_name, {
                 'fields': ('code_system_name_display',)
                 }),
                 )
    
    radio_fields = {'code_system_name_display': admin.VERTICAL}

    
    
########################################################

class ClinicalDomainAllergiesAdmin(ClinicalDomainAdmin):
    inlines = (ClinicalDomainDataElementsInline, AllergiesTimeFilterInline, AllergiesPropertiesInline)



############################################################################

class PageAdmin(dbmModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

############################################################################


class ClinicalDomainDataElementsInline_WithReport(dbmBaseAdminTabularInline):
    verbose_name = "Grid Display Option"
    verbose_name_plural = "Grid Display Options"
    model = DataElement
    formset = DataElementFormSet_WithReport
    list_display    = ('enable', 'name', 'page_width', 'default_width', 'order')
    fields          = ('enable', 'name', 'page_width', 'default_width', 'report_width', 'default_report_width', 'order')
    ordering        = ('order',)
    readonly_fields = ('name', 'default_width', 'default_report_width')

    

class ImmunizationsPropertiesInline(ClinicalDomainPropertiesInline):
    fieldsets = (
                 ('Display Options', {
                 'fields': ('show_cancelled_display', 'show_cancelled_selected')
                 }),
                 )
    radio_fields = {'code_system_name_display': admin.VERTICAL}
    form = ImmunizationsDomainPropertiesAdminForm

class ImmunizationsTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = ImmunizationsDomainTimeFilterAdminForm

class ClinicalDomainImmunizationsAdmin(dbmModelAdmin):
    inlines = (ClinicalDomainDataElementsInline_WithReport, ImmunizationsTimeFilterInline, ImmunizationsPropertiesInline, VpoImmunizationsInline)
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

############################################################################################

class ClinicalDomainDemographicsDetailsDEInline(ClinicalDomainDataElementsInline):
    verbose_name_plural = "Demography Details Grid Display Options"
    model = DemographicsDetailsDEGrid

    list_display = ('enable', 'name',)
    fields = ('enable', 'name',)

    # We're not using the normal DataElement formset, because we DON'T want the validation of the columns.
    # That's cause we don't HAVE columns in this case.
    formset = BaseInlineFormSet


class InsuranceDataElementsInline(ClinicalDomainDataElementsInline_WithReport):
    model = InsuranceDataElement
    verbose_name_plural = "Insurance Grid Display Options"

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
class DemographyDisplayOptionsInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ('demography_details_type', 'demography_display_insurances_grid')
                 }),
                 )
    radio_fields = {'demography_details_type': admin.VERTICAL}
    form = DemographyDisplayOptionsInlineForm

class ClinicalDomainDemograhicsAdmin(ClinicalDomainAdmin):
    inlines = (ClinicalDomainDemographicsDetailsDEInline, DemographyDisplayOptionsInline, InsuranceDataElementsInline, VpoDemographyInline)
    
############################################################################################
class VitalsDataElementsInline(dbmBaseAdminTabularInline):
    verbose_name = "Grid Display Option"
    verbose_name_plural = "Elements Grid Display Options"
    model = DataElement
    formset = DataElementFormSet_WithReport
    list_display    = ('enable', 'name', 'page_width', 'default_width', 'hide_uom', 'concatenate_values', 'order')
    fields          = ('enable', 'name', 'page_width', 'default_width', 'report_width', 'default_report_width', 'hide_uom', 'concatenate_values', 'order')
    ordering        = ('order',)
    readonly_fields = ('default_width', 'default_report_width')
        
    # this changes the model_descriptor referenced in the "services to restart" list
    def get_db_model_descriptor(self):
        return 'dbmconfigapp_dataelement_with_vpo'


class VitalsPropertiesInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 ('Display Options', {
                 'fields': ('show_cancelled_display', 'show_cancelled_selected')
                 }),
                 )
    radio_fields = {'code_system_name_display': admin.VERTICAL}
    form = VitalsDomainPropertiesAdminForm

class VitalsTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = VitalsDomainTimeFilterAdminForm

class MeasurementSemanticGroupInline(dbmBaseAdminTabularInline):
    model = EHRAgentSemanticGroup
    fields = ('name_url', 'order', 'measurements' )
    readonly_fields = ('name_url', 'measurements')
    ordering = ('order','display_name')
    extra=0
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    class Meta:
        add_link = "/admin/dbmconfigapp/ehragentsemanticgroup/add/"
        help_text = "For Patient View, configure the measurement vocabulary domains and define the semantic grouping. <br><b>Group Display Name:</b> Define a new semantic group name under Measurements.<br><b>Group Order:</b> Specify the order to display the groups under Measurements."


class PVMeasurementAdmin(dbmModelAdmin):
    inlines = (VpoVitalsInline, VitalsInpatientMeasurementInline, MeasurementSemanticGroupInline)
    model = PVMeasurementPage
    exclude = ('page_help_text', 'page_name', 'tree_id')

class ClinicalDomainVitalsAdmin(dbmModelAdmin):
    inlines = (VitalsDataElementsInline, VitalsTimeFilterInline, VitalsPropertiesInline, VpoVitalsInline, VitalsInpatientMeasurementInline)
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProblemsPropertiesInline(ClinicalDomainPropertiesInline):
    fieldsets = (
                 ('Display Options', {
                 'fields': ('show_cancelled_display', 'show_cancelled_selected',
                            'grouped_by_display', 'grouped_by_selected')
                 }),
                 )
    form = ProblemsDomainPropertiesAdminForm

class ProblemsTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = ProblemsDomainTimeFilterAdminForm

class ClinicalDomainProblemsAdmin(ClinicalDomainAdmin):
    inlines = (ClinicalDomainDataElementsInline, ProblemsTimeFilterInline, ProblemsPropertiesInline, VpoProblemsInline, VpoCommonInline)

class DiagnosesPropertiesInline(ClinicalDomainPropertiesInline):
    fieldsets = (
                 ('Display Options', {
                 'fields': ('grouped_by_display', 'grouped_by_selected')
                 }),
                 )
    form = DiagnosesDomainPropertiesAdminForm

class DiagnosesTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = DiagnosesDomainTimeFilterAdminForm

class ClinicalDomainDiagnosesAdmin(ClinicalDomainAdmin):
    inlines = (ClinicalDomainDataElementsInline_WithReport, DiagnosesTimeFilterInline, DiagnosesPropertiesInline, VpoDiagnosisInline, VpoCommonInline, VpoEhrAgentDomainsFilteringInline)
    


class PathologiesTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = PathologiesDomainTimeFilterAdminForm


class GridDataElementsInline(ClinicalDomainDataElementsInline):
    model = GridDataElement
    verbose_name_plural = "Pathology Grid Display Options"


class FindingDataElementsInline(ClinicalDomainDataElementsInline):
    model = FindingDataElement
    verbose_name_plural = "Related Findings Grid Display Options"


class DocumentDataElementsInline(ClinicalDomainDataElementsInline):
    model = DocumentDataElement
    verbose_name_plural = "Related Documents Grid Display Options"


class ClinicalDomainPathologiesAdmin(dbmModelAdmin):
    inlines = (GridDataElementsInline, FindingDataElementsInline, DocumentDataElementsInline, PathologiesTimeFilterInline)
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id')

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class MedicationsPropertiesInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 ('Display Options', {
                 'fields': ('show_cancelled_display', 'show_cancelled_selected',
                            'display_not_inactive',
                            'grouped_by_display', 'grouped_by_selected')
                 }),
                 )
    form = MedicationsDomainPropertiesAdminForm

class MedicationsTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = MedicationsDomainTimeFilterAdminForm

class ClinicalDomainMedicationsAdmin(ClinicalDomainAdmin):
    inlines = (ClinicalDomainDataElementsInline_WithReport, MedicationsTimeFilterInline, MedicationsPropertiesInline, VpoEhrAgentDomainsFilteringInline)

########################################Encounters Details#####################################################################################
class EncounterDetailsPropertiesInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    
    fieldsets = [
             ('Display Options', {
             'fields': ('display_grid','code_system_name_display',)
             }),
             ]
    radio_fields = {'code_system_name_display': admin.VERTICAL}
    form = EncounterDetailsDomainPropertiesAdminForm


class LocationHistoryDataElementsInline(ClinicalDomainDataElementsInline):
    model = LocationHistoryDataElement
    verbose_name_plural = "Location History Grid Display Options"

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class ProviderRelationshipDataElementsInline(ClinicalDomainDataElementsInline):
    model = ProviderRelationshipDataElement
    verbose_name_plural = "Provider Relationship Grid Display Options"

class DiagnosesDataElementsInline(ClinicalDomainDataElementsInline):
    model = DiagnosesDataElement
    verbose_name_plural = "Diagnoses Grid Display Options"


class ClinicalDomainEncounterDetailsAdmin(dbmModelAdmin):
    inlines = (EncounterDetailsPropertiesInline, LocationHistoryDataElementsInline, DiagnosesDataElementsInline, ProviderRelationshipDataElementsInline, VpoEncounterDetailsInline)
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id')

    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

######################################## PLV #####################################################################################
class PlvTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = PlvDomainTimeFilterAdminForm
     
         
class ClinicalDomainPlvAdmin(dbmModelAdmin):
    inlines = (PlvTimeFilterInline, )
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id', )

    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

######################################## Encounters #####################################################################################
class EncountersTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = EncountersDomainTimeFilterAdminForm

class ClinicalDomainEncountersAdmin(dbmModelAdmin):
    inlines = (ClinicalDomainDataElementsInline, EncountersTimeFilterInline, VpoEncountersInline)
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id')

    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

######################################## Summary #####################################################################################
class SummaryPropertiesInline(ClinicalDomainPropertiesInline):
    fieldsets = [
             ('Display Options', {
             'fields': ('show_record_count', 'ConditionTypeToDisplay',), 'classes': ['wide', 'extrapretty']
             }),
             ]
    radio_fields = {'ConditionTypeToDisplay': admin.VERTICAL}
    form = SummaryDomainPropertiesAdminForm


class AllergiesDataElementsInline(ClinicalDomainDataElementsInline_WithReport):
    model = AllergiesDataElement
    verbose_name_plural = "Allergies Grid Display Options"

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class MedicationsDataElementsInline(ClinicalDomainDataElementsInline_WithReport):
    model = MedicationsDataElement
    verbose_name_plural = "Medications Grid Display Options"

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
class ProblemsElementsInline(ClinicalDomainDataElementsInline_WithReport):
    model = ProblemsDataElement
    verbose_name_plural = "Problems Grid Display Options"

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class DiagnosisElementsInline(ClinicalDomainDataElementsInline_WithReport):
    model = DiagnosisDataElement
    verbose_name_plural = "Diagnosis Grid Display Options"

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class LabsElementsInline(ClinicalDomainDataElementsInline_WithReport):
    model = LabsDataElement
    verbose_name_plural = "Labs Grid Display Options"


class ClinicalDomainSummaryAdmin(dbmModelAdmin):
    inlines = (AllergiesDataElementsInline, MedicationsDataElementsInline, ProblemsElementsInline, DiagnosisElementsInline, LabsElementsInline, SummaryPropertiesInline, VpoSummaryInline)
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id')

    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
    
    ######################################## Procedures #####################################################################################

class ProceduresPropertiesInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 ('Display Filters', {
                 'fields': ('grouped_by_display', 'grouped_by_selected')
                 }),
                 )
    form = ProceduresDomainPropertiesAdminForm

class ProceduresTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = ProceduresDomainTimeFilterAdminForm

class ClinicalDomainProceduresAdmin(ClinicalDomainAdmin):
    inlines = (ClinicalDomainDataElementsInline, ProceduresTimeFilterInline, ProceduresPropertiesInline, VpoCommonInline)
    

######################################## LabResultsHistory #####################################################################################
class LabResultsHistoryPropertiesInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 ('Display Filters', {
                 'fields': ('LabEvents_DefaultGrouping',)
                 }),
                 ('Lab Search Display', {
                 'fields': ('LabResultHistory_DisplaySearch',)
                 }),
                 )
    form = LabResultsHistoryDomainPropertiesAdminForm

class LabResultsHistoryTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = LabResultsHistoryDomainTimeFilterAdminForm     
    
class ClinicalDomainLabResultsHistoryAdmin(dbmModelAdmin):
    inlines = (LabResultsHistoryTimeFilterInline, LabResultsHistoryPropertiesInline )
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id', )

    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

######################################## Imaging #####################################################################################
class ImagingPropertiesInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 ('Display Filters', {
                 'fields': ('Imaging_DisplayImagingMetaData', 'Imaging_ShowEmptyFolders')
                 }),
                 )
    form = ImagingDomainPropertiesAdminForm

class ImagingTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = ImagingDomainTimeFilterAdminForm

class ImagingPacsInline(dbmBaseAdminTabularInline):
    model = ImagingPacs
    fields = ('name_url', 'device_id', 'use_code', 'schema_code', 'facility', 'method', 'parameters')
    readonly_fields = ('name_url', 'device_id', 'use_code', 'schema_code', 'facility', 'method', 'parameters')
    extra=0
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    class Meta:
        add_link = "/admin/dbmconfigapp/imagingpacs/add/"
        help_text = get_grid_help_text('This configuration is used to access the PACS (Picture Archiving and Communication Systems) to display the selected Imaging records of the specific patient. The deviceId, useCode, schemeCode represents the system identity. The link to the system can be composed of both static and dynamic parts. These parts can be a function of the metadata (for example, use code) of the imaging record. Patient View only supports https:// URL for viewing PACS images.')
        
class ClinicalDomainImagingAdmin(dbmModelAdmin):
    inlines = (ImagingTimeFilterInline, ImagingPropertiesInline, ImagingPacsInline, VpoImagingInline)
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'help_text_1', 'help_text_2', 'help_text_3', 'services', 'tree_id', )

    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
    


############################### Laboratory ###############################

class LabEventsTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = LaboratoryDomainTimeFilterAdminForm   
        
class LabChartDisplayOptionsInline(dbmBaseAdminStackedInline):
    model = LabChartDisplayOptions
    fieldsets = (
                 ('Lab Report Display Options', {
                    'fields': ('report_max_rows_in_regular_col', 'report_max_chars_in_remark_col', 'report_max_rows_in_long_row_cell'),
                    'description': 'The Lab Report column configuration is used to define how the Remarks column and the Results column of the Lab Report are displayed. Three basic display options are available, depending on the size of the text to be displayed. The display option is selected based on a series of verifications performed by the system based on the configured values of the parameters below.<br>The following options are available:<ul><li>Regular Column Display: In this scenario, the text is not too large and can easily fit in the grid column area. To verify that the text can be displayed in the regular grid column, the system checks the text size according to the values configured in the following parameters: Result column configurations and Remarks column configurations.</li><li>Long Row Display: If the text size is too large and cannot be displayed in the regular grid column, the system provides an additional option, where the text is displayed in a long row provided either for the Result or the Remarks text (added immediately below the grid column) if either one of them is too large for the regular display. To verify that the text can be displayed in the long row, the system checks the text size according to the values configured in the following parameters.</li><li>End of Report Display: If the text size is too large for the Long Row (either in the Result or the Remarks column, or for both), the system provides an additional option, where the text is displayed at the end of the report regardless of the text size or the number of rows. Additional pages are provided to include the entire text.</li></ul>'
                    }),
                 ('Lab Charts Display Options (Affect Labs and Diabetes clinical domains)', {
                    'fields': ('chart_format', 'range_values', 'abnormal_values', 'date_format',
                               'display_range_values', 'display_abnormal_in_color')
                    })
                 )
    radio_fields = {'chart_format': admin.VERTICAL, 
                    'range_values': admin.VERTICAL, 
                    'abnormal_values': admin.VERTICAL, 
                    'date_format': admin.VERTICAL}
    form = LabChartDisplayOptionsForm


class ClinicalDomainLaboratoryAdmin(ClinicalDomainAdmin):
    inlines = (ClinicalDomainDataElementsInline, LabEventsTimeFilterInline, LabChartDisplayOptionsInline)


######################################## Clinical Documents #####################################################################################
class DocumentsPropertiesInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    fieldsets = (
                 ('Display Options', {
                 'fields': (('show_cancelled_display', 'show_cancelled_selected'),
                            'ClinicalDocument_ShowExternalDocumentsLabel', 'ClinicalDocument_BringExtDocsOnShowAll', 'ClinicalDocument_ShowExternalDocumentsLabelForAgent',
                            ('Documents_CompletionStatusAdded', 'ClinicalDocument_ShowEmptyFolders'),
                            'ClinicalDocument_DocPreviewFontFamily', 'ClinicalDocument_SortTypeByDesignation',
                            ('ClinicalDocument_DocsTreePaneWidth','ClinicalDocument_ExtDocsTreePaneHeight'),
                            'ExteranlDocument_Default_Grouping'
                            ),
                 }),
                 )
    form = DocumentsDomainPropertiesAdminForm

class DocumentsTimeFilterInline(ClinicalDomainPropertiesInline_TimeFilter):
    form = DocumentsDomainTimeFilterAdminForm

class ClinicalDomainDocumentsAdmin(ClinicalDomainAdmin):
    inlines = (DocumentsTimeFilterInline, DocumentsPropertiesInline, VpoEhrAgentDomainsFilteringInline, VpoClinicalDocumentsInline)


############################### Lab Results ###############################

class LabResultsDataElements(ClinicalDomainDataElementsInline_WithReport):
    fields          = ('enable', 'name', 'page_width', 'default_width', 'report_width', 'default_report_width', 'order', '_info')


class LabResultsInline(dbmBaseAdminStackedInline):
    model = ClinicalDomainProperties
    form = LabResultsDomainPropertiesAdminForm
    verbose_name_plural = "Display Options"
#     fields = ('LabResults_FormatText', 'Laboratory_UseWrappedText')
    fieldsets = (
                 ('Display Options', {
                 'fields': ('LabResults_FormatText', 'Laboratory_UseWrappedText',
                            ),
                 }),
                 ('Microbiology', {
                 'fields': ('Laboratory_OpenMicroReportForMicroEvent',
                            ),
                 }),
                 )

    
class ClinicalDomainLabResultsAdmin(ClinicalDomainAdmin):
    inlines = (LabResultsDataElements, LabResultsInline, VpoLabResultsInline)


############################### Imaging PACS ###############################


class ImagingPacsParametersInline(dbmBaseAdminTabularInline):
    model = ImagingPacsParameter
    fields = ('name', 'is_static', 'parameter_value')
    extra = 1
    
    
class ImagingPacsAdmin(dbmModelAdmin):
    model = ImagingPacs
    form = ImagingPacsForm
    inlines = (ImagingPacsParametersInline, )
    fieldsets = [              
        (model._meta.verbose_name, 
            {'fields': ['uri','device_id', 'use_code', 'schema_code', 'facility', 'method'], 'classes': ['wide', 'extrapretty'] }),
        ]
    radio_fields = {'method': admin.HORIZONTAL }
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
#    class Media:
#        js = ['admin/js/external-applications.js'] 




