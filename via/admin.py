from django.contrib import admin
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdminSaveOnly, dbmBaseAdminStackedInline, dbmBaseAdminTabularInline, get_grid_help_text, dbmBaseAdminStackedInline_Simple,dbmModelAdmin
from via.models import *
from via.forms import *
from django.forms import TextInput, ModelForm, Textarea
from django.forms.widgets import HiddenInput
from configcenter.settings import get_param
from dbmconfigapp.models.ppol_general import PpolGeneral


      
        
    
class ViaVpoInline(dbmBaseAdminStackedInline):
    model = ViaVpo
    fieldsets = [              
        ('EMPI VPO Settings',   {'fields': ['vpo_personindex_dynamic_field_list_for_response'], 'classes': ['wide', 'extrapretty']})]
class ViaInline(dbmBaseAdminStackedInline):
    model = Via
    form = ViaAdminForm
    help_test_field = Via._meta.get_field("empi_type")
    def_val = help_test_field.help_text.split("Default:",1)[1]
    if get_param('default_language') == 'he-IL' :
        help_test_field.help_text = get_help_text('Defines the EMPI connection type <br> *Federated CDR Relevant only in Israel.<br><b>Important</b> need to update "Patient Search" -> "Search Filter" -> "Filter patient cluster when patient is partially confidential" based on project needs',def_val)
        fieldsets = [              
        ('EMPI Type',   {'fields':['empi_type','hmo_id'], 'classes': ['wide', 'extrapretty']}),
        ('HiddenSection', {'fields': ['hmo_name']})]
    else:
        fieldsets = [              
        ('EMPI Type',   {'fields':['empi_type'], 'classes': ['wide', 'extrapretty']})]
    
        
class ViaAdmin(dbmModelAdmin):
    model = ViaPage
    inlines = (ViaInline,ViaVpoInline, )
    change_form_template = 'admin/dbmconfigapp/change_form.html'
    
    class Meta:
        tree_id = 'via_general'
        
    class Media:
        js = ['admin/js/via/general_definitions.js']
    
class InitiateVpoInline(dbmBaseAdminStackedInline_Simple):
    model = InitiateVpo
    
class InitiateConnectionInline(dbmBaseAdminStackedInline):
    model = InitiateConnection
    fieldsets = ('Initiate Connection Settings', {'fields': ['initiate_version', 'initiate_url', 'patient_credential_username', 'patient_credential_password'],'description':'<br/><b>Note!</b> These configurations will not be transferred in the export/import process.' ,'classes': ['wide', 'extrapretty']}),
    form = InitiateConnectionForm
        
class InitiateInline(dbmBaseAdminStackedInline):
    model = Initiate
    form = InitiateAdminForm
    fieldsets = [              
        ('Initiate General Settings',   {'fields': ['patient_member_type', 'patient_entity_type', 'set_isrealleading', 'filter_mode', 'patient_results_sort_order'], 'classes': ['wide', 'extrapretty']}),
        ('Initiate Filter Settings', {'fields': ['filter_active', 'filter_overlay', 'filter_merged', 'filter_deleted','filter_MinimumScoreThreshold'], 'classes': ['wide', 'extrapretty'], 'description':'For each patient index status in Initiate choose one of the following filters:<br/><b>- Exclude:</b> This patient index status will be excluded from the request of VIA to Initiate.<br/><b>- VIA Input:</b> This patient index status will be included in the request of VIA to Initiate but will not be forwarded to VIA consumers (for example, Clinical Viewer).<br/><b>- VIA Input and Output:</b> This patient index status will be included in the request of VIA to Initiate and will also be forwarded to VIA consumers.' }),
        ('HiddenSection', {'fields': ['empi_url_address_for_patient_identity_feed_v3'], 'classes': ['wide', 'extrapretty']}),
        ]

class CCDAWOADTInline(dbmBaseAdminStackedInline_Simple):
    model = CCDAwithoutADTSystems
    
    class Meta:
        help_text = "Defining Real Source System for CCDA without ADT<br/>To support CCDA without ADT a single Real Source System must be defined (per federated node)."


class dbMotionSystemInline(dbmBaseAdminTabularInline):
    model = dbMotionSystem
    formset  = DbmotionSystemsForm
    fields          = ('dbmotion_system', 'dbmotion_system_node_id')

    extra = 1
       
    class Meta:
        help_text = get_grid_help_text("Defines the single Real Source System in VIA that supports CCDA without ADT.<br/>Only one Real Source System can be defined for each node in a federated system.")


class AuthoritySystemsInline(dbmBaseAdminTabularInline):
    template = 'admin/edit_inline/authority_systems_tabular.html'
    model = AuthoritySystems
    formset = AuthoritySystemsForm
    fields = ('source_system_dbMotion_oid', 'source_system_name', 'source_system_display_name', 'display_for_search', 'is_default','is_system_mandatory', 'dbmotion_node_id','cluster_filter_indication','system_type','segment_name','attribute_code','application_name','facility_name','organization_code')
    ordering = ('source_system_display_name',)
    extra = 1
    
    class Meta:
            help_text = get_grid_help_text("""The Authority Systems configurations are used to define the attributes of all source systems that send patient data to dbMotion. Defining and mapping these attributes is required in order to successfully search for and retrieve patient demographic data from the EMPI and also to correctly retrieve the same patient's clinical data from the CDR.
                <div id='system_type_help'>
                <br/>Source System Type 
                <input type='button' value='Show' id='btn_show_hide_help_extension' onclick='show_hide_help_extension(this);' style='cursor: pointer;'/>
                <div id='help_extension' style='display:none;'>
                This configuration is used to define the type of Source System that VIA returns in the response to the Patient Search query. This can only be returned by defining the location of the source system in the index(es) received from Initiate. All Source Systems in Initiate are Real Source Systems. However, if required, the customer can also add to each Real Source System  one or more (secondary) Virtual Source Systems. In this way,  each Source System in VIA can be both Real and also Virtual.<br/>
                When Initiate returns an index to VIA in response to Patient Search, the response will contain the identifiers of the Real index (root/extension). However, if required, it can also return the identifiers of a Virtual index (root/extension) in a specific location (segment) within the index. Each Source System Type (Real, Virtual, Virtual Replace Real, etc.) is defined within that segment in this Source System Type attribute.<br/>
                These identifiers can then be mapped by this configuration to one of the configured dbMotion Source Systems (dbMotion root).<br/><br/>
                Definition of Source System Types  in VIA
                <ul>
                <li><b>Real</b> represents a real Source System in Initiate. Initiate can only contain Real Source Systems and returns indexes of these Real systems to VIA in the Initiate response.</li>
                <li><b>Virtual</b> represents an additional Source System. Virtual Source Systems only exist in VIA. However, the patient identifiers (root/extension) of the Virtual Source System are located in a specific location (segment) in the index returned by Initiate to VIA. VIA retrieves this data from the relevant segment in the index and uses it to match it to the dbMotion Source System.<br/> 
                The Demographic value of the Real index and the Virtual index are identical.<br/> 
                The Real index is NOT removed from the VIA response.
                </li>
                <li><b>Virtual Replace Real</b> - This is the same as the Virtual Source System Type. However, in this case the Real index is removed and only the Virtual index is returned from VIA to the consumer (for example, in Patient Search).</li>
                <li><b>Search Only</b> - This Source System is used only for a search and does not return a response. For example, if the Patient Search used the Insurance Number source system but this source system is not required in the response.</li>
                <li><b>Virtual MPIID</b> - This is the same as the Virtual Source System Type except that the extension of this index is the MPI ID. Each cluster can contain only one index with MPI ID (duplicate indexes will be removed).</li>
                <li><b>Search Only MPIID</b> - This Source System is used only for a search (by MPI ID) and does not return a response.</li>
                </ul>
                </div>
                </div>""")
            


class InitiateAdmin(dbmModelAdmin):
    model = InitiatePage
    inlines = (InitiateConnectionInline, InitiateInline, InitiateVpoInline, )
    change_form_template = 'admin/dbmconfigapp/change_form.html'
    
    class Meta:
        tree_id = 'via_initiate'
    class Media:
        js = ['admin/js/via/initiate.js']

class AuthoritySystemsAdmin(dbmModelAdmin):
    model = AuthoritySystemsPage
    inlines = (AuthoritySystemsInline, CCDAWOADTInline, dbMotionSystemInline, ViaInline,)
    change_form_template = 'admin/dbmconfigapp/change_form.html'
    
    class Meta:
        tree_id = 'via_authoritysystems'
    class Media:
        js = ['admin/js/via/authority_systems.js']

class InitiateMappingsInline(dbmBaseAdminTabularInline):
    model = InitiateMappings
    formset = MappingsForm
    
    list_display    = ('dbmotion_attribute_name', 'dbmotion_attribute_description', 'initiate_hub_segment_name', 
                       'initiate_hub_attribute_code', 'initiate_hub_field_name', 'initiate_hub_id_issuer',
                        'mapping_values', 'dbmotion_attribute_input', 'dbmotion_attribute_output', 'dbmotion_attribute_weight')
    fields          = ('parent', 'dbmotion_attribute_name', 'dbmotion_attribute_description', 'initiate_hub_segment_name', 
                       'initiate_hub_attribute_code', 'initiate_hub_field_name', 'initiate_hub_id_issuer',
                        'mapping_values', 'dbmotion_attribute_input', 'dbmotion_attribute_output', 'dbmotion_attribute_weight')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    }

    extra = 1
       
    class Meta:
        help_text = get_grid_help_text('These configurations are used to map the patient demographic attributes between dbMotion and Initiate.<br/>These mappings are used when sending a Patient Search query to retrieve the data from Initiate/or to update Initiate with patient data through VIA.')

class InitiateMappingsAdmin(dbmModelAdmin):
    model = InitiateMappingsPage
    inlines = (InitiateMappingsInline, )
    change_form_template = 'admin/dbmconfigapp/change_form.html'
    
    class Meta:
        tree_id = 'via_initiatemappings'
    class Media:
        js = ['admin/js/via/initiate_mappings.js']

class EmpiPpolGeneralInline(dbmBaseAdminStackedInline):
    model = PpolGeneral
    fieldsets = [              
        ('Provider Registry General Settings',{'fields': ['PatientDefaultCacheTolerance', 'PcpRelationStrategy']}),
        ('CDR Discovery Sync Options', {'fields': ['CdrDiscovery', 'MaximumAttemptsNumber', 'PatientResetWorker', 'RelationSourceResetWorker', 'RelationTargetResetWorker', 'GeneralResetWorker'], 'description' : "In projects with no CAG, PH or Patient View it is recommended to stop these services. This action is recommended in order to improve system performance.<br/><div style=\"color:red\">Important! Check this with the Product team before disabling the service</div>",'classes': ['wide', 'extrapretty']}),
        ('Medical Staff Sync Options', {'fields': ['MedicalStaffSync', 'MedicalStaffSyncTracing'], 'description' : "In projects with no CAG, PH or Patient View it is recommended to stop these services. This action is recommended in order to improve system performance.<br/><div style=\"color:red\">Important! Check this with the Product team before disabling the service</div>",'classes': ['wide', 'extrapretty']})]

class EmpiPpolGeneralAdmin(dbmModelAdmin):
    model = EmpiPpolGeneralPage
    inlines = (EmpiPpolGeneralInline, )
    exclude = ('page_help_text', 'page_name', 'services')
    change_form_template = 'admin/dbmconfigapp/change_form.html'    
    class Meta:
        tree_id = 'via_ppolgeneral'
    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
        js = ['admin/js/via/ppolgeneral.js']
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ViaPage, ViaAdmin)
admin.site.register(InitiatePage, InitiateAdmin)
admin.site.register(AuthoritySystemsPage, AuthoritySystemsAdmin)
admin.site.register(InitiateMappingsPage, InitiateMappingsAdmin)
admin.site.register(EmpiPpolGeneralPage, EmpiPpolGeneralAdmin)
