from django.contrib import admin

from dbmconfigapp.models.ehragent_clinical_domains import EHRAgentBlinks, EHRAgentClinicalDomainsProperties,\
    EHRAgentCVCommonClinicalDomainsProperties, VitalsInpatientMeasurement, EHRAgentSemanticDelta
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminTabularInline, get_grid_help_text, dbmBaseAdminStackedInline, dbmBaseAdminStackedInline_Simple
from dbmconfigapp.form.ehragent_forms import EHRAgentBlinksInlineForm, VpoEhrAgentDomainsInlineForm, VitalsInpatientMeasurementForm, EHRAgentClinicalDomainInlineForm, EHRAgentCommonClinicalDomainInlineForm
from dbmconfigapp.models.vpo import VpoEHRAgentDomains
from dbmconfigapp.models.cvtables import ImagingPacs

########################################################

class EHRAgentClinicalDomainInline(dbmBaseAdminTabularInline):
    model = EHRAgentClinicalDomainsProperties
    form = EHRAgentClinicalDomainInlineForm
    list_display    = ('display_name', 'attention_searching_time', 'attention_searching_option', 'default_attention_time')
    fields          = ('parent', 'display_name', 'attention_searching_time','attention_searching_option', 'default_attention_time')
    readonly_fields = ('display_name','default_attention_time', 'parent')
    
    class Meta:
        help_text = get_grid_help_text('This configuration enables the user to define the time period for calculating the displayed Badging in the Agent Hub and Patient View.<br/>Clinical data available within this defined time period (for example, the past 7 days) activates the applications Badging mechanism.<br/>To disable the Badging, set the Attention Time Unit to Off.<br/>The Badging displays clinical data updates. For more information, see the relevant chapter in the Agent Hub/Patient View Functional Specification.<br/>Note that Semantic Delta configuration applies not only to badging but also to the data displayed in the Clinical View Agent/Patient View application.<br/>For optimal performance, it is recommended to limit this configuration to a maximum period of 7 days. A value greater than 7 days might result in reduced performance.')
       
class EHRAgentCVCommonClinicalDomainInline(dbmBaseAdminTabularInline):
    model = EHRAgentCVCommonClinicalDomainsProperties
    form = EHRAgentCommonClinicalDomainInlineForm
    list_display    = ('display_name', 'default_searching_time', 'default_searching_option','default_time_range')
    fields          = ('ehragent_parent', 'display_name', 'default_searching_time', 'default_searching_option','default_time_range')
    readonly_fields = ('display_name', 'default_time_range', 'ehragent_parent')
    
    class Meta:
        help_text = get_grid_help_text('This configuration defines the time range used to filter the clinical data displayed for each domain in the clinical applications. Use the Time Range field and the Time Unit dropdown menu to define the time range for each domain.<br>For example, for Diagnoses, if the Time Range is 10 and the Time Unit is Month, the patient\'s Diagnoses over the past 10 months are displayed.<br>This configuration is used for the Clinical Viewer and EHR Agent.')
    def queryset(self, request):
        qs = super(EHRAgentCVCommonClinicalDomainInline, self).queryset(request)
        return qs.exclude(name='PLV'
                ).exclude(name='LabResultsHistory'
                ).exclude(name='AllergyIntolerance'
                ).exclude(name='Medication'
                ).exclude(name='Problem')

 
class EHRAgentBlinksInline(dbmBaseAdminStackedInline):
    model= EHRAgentBlinks
    form= EHRAgentBlinksInlineForm

    fieldsets=(
                 (model._meta.history_meta_label, {
                 'fields': ['admission_interval', 'admission_inpatient_domains'],
                 'classes': ['wide', 'extrapretty'] }),
                 )

class VpoEhrAgentDomainsInline(dbmBaseAdminStackedInline):
    model = VpoEHRAgentDomains
    form = VpoEhrAgentDomainsInlineForm
    fields = ['filter_codes',]
    template = 'admin/edit_inline/stacked.html'
    verbose_name_plural = 'Filtering Out Clinical Data'
    
    def queryset(self, request):
        qs = super(VpoEhrAgentDomainsInline, self).queryset(request)
        return qs.exclude(clinical_domain_id=11)
    
class VpoEhrAgentDomainsProceduresInline(dbmBaseAdminStackedInline_Simple):
    model = VpoEHRAgentDomains
    form = VpoEhrAgentDomainsInlineForm
    fields = ['filter_type', 'filter_codes',]
    verbose_name_plural = 'Filtering Clinical Data'
    
    def queryset(self, request):
        qs = super(VpoEhrAgentDomainsProceduresInline, self).queryset(request)
        return qs.filter(clinical_domain_id=11)
    
    def get_services_to_restart(self):
        qs = super(VpoEhrAgentDomainsProceduresInline, self).get_services_to_restart()
        return qs.exclude(code_name='VPO')

class ImagingPacsInline(dbmBaseAdminTabularInline):
    model = ImagingPacs
    fields = ('name_url', 'device_id', 'use_code', 'schema_code', 'method', 'parameters')
    readonly_fields = ('name_url', 'device_id', 'use_code', 'schema_code', 'method', 'parameters')
    extra=0
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    class Meta:
        add_link = "/admin/dbmconfigapp/imagingpacs/add/"
        help_text = get_grid_help_text('This configuration is used to access the PACS (Picture Archiving and Communication Systems) to display the selected Imaging records of the specific patient. The deviceId, useCode, schemeCode represents the system identity. The link to the system can be composed of both static and dynamic parts. These parts can be a function of the metadata (for example, use code) of the imaging record.')
    
class VitalsInpatientMeasurementInline(dbmBaseAdminStackedInline_Simple):
    model = VitalsInpatientMeasurement
    form = VitalsInpatientMeasurementForm
    
    fields = ['include_inpatient_measurements', 'include_emergency_measurements']  
    verbose_name_plural = 'Inpatient Measurements'

class EHRAgentSemanticDeltaInline(dbmBaseAdminTabularInline):
    model = EHRAgentSemanticDelta
    list_display    = ('display_name', 'enable_semantic_delta')
    fields          = ('display_name', 'enable_semantic_delta')
    readonly_fields = ('display_name', )
        
       
 
    

