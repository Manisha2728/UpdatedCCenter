from django.contrib import admin, messages
from dbmconfigapp.admin.dbm_ModelAdmin import dbmBaseModelAdmin, ServicesToRestart, dbmBaseAdminTabularInline, get_grid_help_text, dbmModelAdmin
from .models import *
from .forms import *
from dbmconfigapp.forms import MinimumOneFormSet
from configcenter import *
from configcenter.settings import get_param
import copy
from django.utils.encoding import force_text
import logging
from .models_installation_profiles import *
 
default_language = get_param('default_language')
#print(default_language) 
IsOfek = (default_language == 'he-IL')

class BaseAdmin(dbmBaseModelAdmin, ServicesToRestart):
    def __init__(self, *args, **kwargs):
        super(BaseAdmin, self).__init__(*args, **kwargs)
        if not self.fieldsets:
            self.fieldsets = [(self.model._meta.history_meta_label, 
                 {'fields': [f.name for f in self.model._meta.fields][1:], 'classes': ['wide', ]}),]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] =  ('_popup' in request.GET)
        extra_context['show_delete_link'] = False
        extra_context['show_save_as_new'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(BaseAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = ('_popup' in request.GET)
        extra_context['show_delete_link'] = False
        extra_context['show_save_as_new'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(BaseAdmin, self).add_view(request, form_url, extra_context=extra_context)

    
class EhrAdmin(BaseAdmin):
    model = EHR
    list_display = ('name', 'deploy_type_display', 'instances')
    list_display_links = ('name', 'deploy_type_display')
    form = EhrAdminForm
    change_form_template = 'admin/externalapps/ehr_preview_extension.html'
    fieldsets = (
        ('EHR', {
            'fields': ('name',)}),
        ('Detection', {
            'fields': ('deployment_type', 'detection_exe', 'detection_launch_title', 'detection_window_class', 'detection_url', 'detection_title', 'detection_follow_focused_window', 'prevent_detected_window_topmost','detection_version')}),
        ('Position', {
            'fields': (('position_app_corner', 'position_agent_corner', 'position_offset_x', 'position_offset_y'),), 'description': 'This configuration enables you to define the EHR Agent window position relative to the EHR application window. This configuration defines the default position each time the EHR Agent opens. After it opens in the defined position, however, it can be moved to any other position that the user prefers.<br/>App corner: Defines the corner of the EHR application window that is used as a starting point to calculate the EHR Agent window position.<br/>Agent corner: Defines the corner of the EHR Agent window that is positioned in relation to the defined EHR application window corner.<br/>Offset: Defines the horizontal and vertical offset positions, in pixels, of the EHR Agent window corner from the EHR application window corner.'}), 
    )
    
    class Meta:
        tree_id = 'ehragent_apps_ehr'
    
    class Media:
        css = { "all" : ("admin/css/externalapps/externalapps.css",) }
        js = ['admin/js/externalapps/ehr.js']

class ParticpantInline(dbmBaseAdminTabularInline):
    type = None
    model = Participant
    extra = 1
    
    formfield_overrides = {
         models.TextField: {'widget': forms.Textarea(attrs={'rows':2, 'cols':140})},
         }
    
    def queryset(self, request):
        qs = super(ParticpantInline, self).queryset(request)
        return qs.filter(type=self.type)
    
    class Meta:
        help_text = 'This configuration is used to configure the participant name and passcode that the EHR needs in order to join the context of the Context Manager.<br/>These values are provided by the customer or by dbMotion and must be agreed upon by both.<br/>If the customer does not provide a passcode, use the Generate button to generate a passcode.<br/><b>Note:</b> Is Shared functionality works only for non Web EHRs.' # The passcode is displayed decrypted, while it is saved encrypted.'
    
    
class ParticpantInline1(ParticpantInline):
    # display a single row. no add. no is_shared field
    type = 'CcowParticipant'
    fields = ('name', 'ccow_passcode')
    max_num=1
    
    
class ParticpantInline2(ParticpantInline):
    # allow adding. display is_shared
    type='CcowReceiver'
    fields = ('name', 'ccow_passcode', 'is_shared')

if IsOfek:  
    fields   = ['facility_root','facility_extension','ofek_url']
else:
    fields = ['facility_root','facility_extension']
    
    user_mapping_fields = ['user_mapping_file_path','user_mapping_is_use_as_role','user_mapping_is_default_to_loggedInUser']

class InstanceAdmin(BaseAdmin):
    model = Instance
    form = InstanceAdminForm
    list_display = ('name', 'ehr', 'instance_properties', 'is_enabled')
    list_filter = ('ehr', 'instance_properties', )
    readonly_fields = ('is_enabled',)
    fieldsets = [(model._meta.history_meta_label, 
                 {'fields': ['name', 'ehr', 'is_enabled','instance_properties', ('env_variable_name', 'env_variable_value')]
                    , 'classes': ['wide', ]}),
                 ('Context Properties',
                 {'fields': ['context_type', 'nonCcowPluginType', 'interceptor_type', 'uiAutomation_config_file_path', 'is_user_mapping_enabled', ],
                   'description': """Context properties define the way that User and Patient data are retrieved from an EHR"""
                    , 'classes': ['wide', ]}),
                 ('User Mapping Properties',
                 {'fields': ['user_mapping_file_path','user_mapping_is_use_as_role','user_mapping_is_default_to_loggedInUser'],
                   'description': """Configuration for user mapping"""
                    , 'classes': ['wide', ]}),
                 ('User Facility Identification', 
                 {'fields': fields,
                  'description': """User  Facility  Identification detects the facility mapped to  the EHR instance intercepted by the EHR Agent.<br/>
                                      For more information about the functionality associated with this capability, see the EHR Agent Functional Specification document.
                                      """
                    , 'classes': ['wide', ]}),
        ('More options', {
            'classes': ('collapse', 'wide'),
            'fields': ('exclude_dash_from_mrn', 'blink_only_first_doa', 'supported_profiles', 
                       'direct_address', 'direct_address_suffix', 'mu_reporting_endpoint', 'mu_reporting_source_system_name', 'mu_reporting_type', 
                       'thumbprint', 'mu_reporting_login', 'mu_reporting_password', 'mu_reporting_app_name', 'mu_reporting_community_oid',
                        'ccow_item_name', )
        }),]
    inlines = [ParticpantInline1, ParticpantInline2]
    radio_fields = {'context_type': admin.VERTICAL}
    formfield_overrides = {
         models.TextField: {'widget': forms.Textarea(attrs={'rows':2, 'cols':150})},
         }


    def save_formset(self, request, form, formset, change):
        participants = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for participant in participants:
            participant.type = participant.instance.context_type
            participant.save()
        formset.save_m2m()
    
    def save_related(self, request, form, formsets, change):
        super(InstanceAdmin, self).save_related(request, form, formsets, change)
        form.instance.participant_set.exclude(type=form.instance.context_type).delete()

    
    def get_readonly_fields(self, request, obj=None):
        # on add or edit
        return ()
    
    def get_inline_instances(self, request, obj=None):
        inline_instances = super(InstanceAdmin, self).get_inline_instances(request, obj)
#         if request.method == 'POST':
#             for inline in inline_instances:
#                 if not inline.type == request.POST['context_type']:
#                     inline_instances.remove(inline)
                    
                    
#         for inline_class in self.inlines:
#             inline = inline_class(self.model, self.admin_site)
#             if request:
#                 if not (inline.has_add_permission(request) or
#                         inline.has_change_permission(request, obj) or
#                         inline.has_delete_permission(request, obj)):
#                     continue
#                 if not inline.has_add_permission(request):
#                     inline.max_num = 0
#             inline_instances.append(inline)

        return inline_instances
    
    class Meta:
        tree_id = 'ehragent_apps_instance'
        
    class Media:
        css = { "all" : ("admin/css/externalapps/externalapps.css",) }
        js = ['admin/js/externalapps/instance.js']
        
        
class SourceSystemInline(dbmBaseAdminTabularInline):
    model = SourceSystem
    formset = MinimumOneFormSet
    extra = 1
    fields = ('name', 'act_types')
    
    class Meta:
        help_text = """
            <b>Configuring the Delta View</b><br/>
            The EHR Agent Delta View displays all patient clinical data that is NOT displayed in the hosting EHR. In order to enable the Delta View, it is necessary to define all act types that are received by the EHR from each external source system. These configured act types will not be displayed in the EHR Agent Delta View.<br/> 
            For each external Source System define the following:<br/>
            <ul><li>Name - Source System name as configured in the OIDs XML file
            <li>Act types - All the act types sent by this source system to the EHR
            </ul>
            Possible values are 'All' or one or more of the following, in a comma-separated list:<br/>""" + ', '.join(ACT_TYPES_LIST)


class OrderingFacilitiesInline(dbmBaseAdminTabularInline):
    model = OrderingFacilities
    extra = 1
    fields = ('act_type', 'facility_root', 'facility_extension')
    
    class Meta:
        help_text = """
            <b>Configuring the Delta View By Ordering Facility</b><br/>
            Configure the required Ordering Facilities to be filtered out of the Delta View<br/>
            <br/>The following Facilities can be configured:<br/>
            <ul>
            <li>Referral organization for Lab Request/Pathlogy Request/Imaging Request or Participate Organization for Clinical Document
            <li>Sending organization (will be used only if there is no referral organization)
            </ul>
 
            For each Ordering Facility define the following:<br/>
            <ul> 
            <li>Act type - Possible values are: Lab Event, Pathology Event, Clinical Image Study, Clinical Document 
            <li>Ordering Facility ID Root - OID of the Ordering Facility (e.g: 2.16.840.1.113883.3.57.1.3.5.1.111.1.6.1)
            <li>Ordering Facility ID Extension - Extension of the Ordering Facility (e.g: facilityName)
            </ul>
            <br/><b>Note that Delta By Ordering Facility will override Delta by Source System for any domain that is configured in this section. For these domains the system will filter out data based on the configured Ordering Facility and not based on the configured Source System.</b>
            """
             

class UserContextInline(dbmBaseAdminTabularInline):
    model = UserContext
    form = UserContextInlineForm
    extra = 1
    
    class Meta:
        help_text = """
            <b>Note:</b> for Non CCOW context type, Managed and Unmanaged credentials can be used only when there is a unique AppId for the EHR Instance.<br/>
			    If the AppId is configured for more than one EHR Instance, these fields are irrelevant<br/>
            <br/>
            <b>User context type</b> options:<br/>
            <ul>
            <li>Managed - Authenticates users who are defined in the Active Directory.In a project that requires configuring more than one Active Directory Domain, enter each AD Domain value separated by the "|" character. For example: AD1|AD2<br/>
            <li>Unmanaged credentials - Authenticates users who are not defined in the Active Directory.<br/>
            <li>Unmanaged SAML - Authenticates users using SAML token.<br/>
            <li>User for "Send to my EHR" - User to be used in the CCD of "Send to my EHR".
            </ul>
            """
    
class PatientContextInline(dbmBaseAdminTabularInline):
    model = PatientContext
    extra = 1
    
    class Meta:
        help_text ="""
            <b>Patient Assigning Authority for display:</b><br/>
            Enables the customer to determine from which source system the patient MRN is taken to be displayed in the EHR Agent Patient Details header.<br/>
            If not configured, the EHR Agent will continue to display the patient MRN according to the previous logic, which is to display the MRN of the patient context and the Demographics from the leading record. <br/>
            The updated MRN display logic is as follows:<br/>
            <ul>
            <li>The EHR Agent will display a MRN from a system that can be configured.
            <li>The following logic for MRN display will be implemented: 
            <li>If the configured system exists in the patient cluster returned from PHRED, use it for MRN display. 
            <li>Else if the patient ID that was passed in CCOW exists in the patient cluster returned from PHRED, use it for MRN display. 
            <li>Else take the first patient index (this is the last updated record OOB) from the patient cluster returned from PHRED, use it for MRN display. 
            <li>dbMotion supports EHRs that use more than one patient assigning authority for resolving the patient. 
            <li>MRN (according to this logic) will also be displayed in the EHR Agent report. 
            <li>The selected patient MRN system will be added to the CV launch. 
            <li>The selected patient MRN system and MRN will be used for Send to my EHR.
            </ul>
            <b>Note:</b> This configuration is used to make sure that when a patient search by MRN is made, the priority order is to first return the MRN of the configured system. If this configuration is not added, the EHR Agent continues to operate according to the old logic.
            <Br/><Br/>
            <b>Suffixes:</b><br/>
            This field is irrelevant in case of Non CCOW context type.<br/>
            Defines the postfix of the CCOW property for the patient MRN \ MPI ID, used to retrieve the patient MRN \ MPI ID.<br/>
            For example, if MRNSystemPostfix is <b>pro</b>, the CCOW Context Receiver gets the CCOW item name <b>patient.id.mrn.AllscriptsEHR</b>.<br/>
            <br/>
            Some EHRs can only support a single CCOW suffix, even when there are multiple Assigning Authorities.<br/>
            In a project that requires configuring more than one patient Assigning Authority for a single CCOW suffix,<br/>
            enter each Assigning Authority value separated by the  "|" character. <br/>
            For example: 1.2.3.4.1.8.1|1.2.3.4.1.8.2|1.2.3.4.1.8.3|1.2.3.4.1.8.4<br/>
            <br/>
            In case of Non CCOW context type, only single context should be defined.
        """
    
class InstancePropertiesAdmin(BaseAdmin):
    model = InstanceProperties
    form = InstancePropertiesAdminForm
    list_display = ('name', 'app_id', 'instances', 'ehr_user_assign_auth', 'user_contexts', 'patient_contexts')
    inlines = (UserContextInline, PatientContextInline)
    fieldsets = [
                 (model._meta.history_meta_label, {'fields': ['name', 'app_id', 'app_id_description'], 'classes': ['wide', ]}),
                 ('User Context Authority', {'fields': ['ehr_user_assign_auth'], 'classes': ['wide', ]}),
                 ('Leading index prioritization for Launch API', {'fields': ['patient_assigning_Authority_for_Display'], 'classes': ['wide', ]}),
                ]
    readonly_fields = ('app_id_description', )
        
#     formfield_overrides = {
#          models.ManyToManyField: {'widget': CheckboxSelectMultipleEx()},
#          }
    
    class Meta:
        tree_id = 'ehragent_apps_instance_properties'
    
    class Media:
        js = ['admin/js/externalapps/instance_properties.js']


class AppIdAdmin(BaseAdmin):
    model = AppId
    fieldsets = [(model._meta.history_meta_label, 
                 {'fields': ('app_id', 'categories_available_for_send', ('send_to_my_EHR_success_message', 'send_to_my_EHR_failure_message', 'send_to_my_EHR_ccda_only')), 'classes': ['wide', ]}),]
    inlines = (SourceSystemInline, OrderingFacilitiesInline)
    
#  Installation Packages:

def log_copy(request, to_object, from_object, object_repr):
    
    from authccenter.utils import get_request_user_ids

    user_id, ccenter_user_id = get_request_user_ids(request)

    message = 'Copied "%s"' % force_text(to_object)
    try:
        message = 'Copied [%s] from "%s" to "%s"' % (to_object._meta.verbose_name, force_text(from_object), force_text(to_object))
    except:
        pass

    from django.contrib.admin.models import ADDITION
    from dbmconfigapp.models.tracking import ChangesHistory
    from django.contrib.contenttypes.models import ContentType

    ChangesHistory.objects.log_action(user_id = user_id,
    ccenter_user_id = ccenter_user_id,
    content_type_id = ContentType.objects.get_for_model(to_object).pk,
    object_id       = to_object.pk,
    object_repr     = object_repr,
    action_flag     = ADDITION,
    change_message = message)

def copy_Selected(modeladmin, request, queryset):    
    for sd in queryset:
        sd_copy = copy.copy(sd) # (2) django copy object
        sd_copy.id = None   # (3) set 'id' to None to create new object
        sd_copy.name = "Test"
        # don't copy installation url
        sd_copy.install_url_expiration_date = None
        sd_copy.install_url = None
        n=1
        while(n<256):
            try:                
                sd_copy.name = sd.name +'_Copy('+str(n)+')'
                sd_copy.save()               
                n=256
            except:
                n=n+1
                        
        #log history
        log_copy(request, sd_copy, sd, sd_copy.name)

copy_Selected.short_description = "Duplicate existing installation profiler(s)"


class InstallationProfileAdmin(BaseAdmin):
    
    list_display = ('name',)
    list_display_links = ('name',)
    model = InstallationProfile
    form = InstallationProfileForm    
    ordering = ('id',)
    actions = [copy_Selected,'delete_profile']    
    fieldsets =(
        ('Installation Profile Details', {
            'fields': ('name', 'product_server_url', 'is_auto_run', 'is_install_ccow_context_receiver', 'is_install_dbm_context_receiver', 'is_launch_api', 'profile_name', 'is_show_system_tray_icon', 'web_server_stateful', 'user_absolute_domain', 'is_multitenant', 'is_uninstall_previous_version', 'is_update_configuration_enabled', 'is_update_new_version_enabled', 'is_activate_ccow_receiver', 'is_display_alert_message', 'is_ccow_isolated_session', 'display_lang'), 'classes': ['wide', 'extrapretty']}),
        ('Installation URL Creation', {
            'fields': ('install_url_expiration_date', 'install_url',), 'classes': ['wide', 'extrapretty']})   
        
    ) 
    
    def get_actions(self, request):
        actions = super(InstallationProfileAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_profile(self, request, queryset):
        for profile in queryset:
            if profile.id != 0:
                profile.delete()
                self.log_deletion(request, profile, None)
                self.message_user(request, profile.name + ' was deleted successfully.', messages.SUCCESS)
            else:
                message = 'Profile [{0}] is mandotory and cannot be deleted.'.format(profile.name)
                self.message_user(request, message, messages.ERROR)            

    delete_profile.short_description = "Delete installation profiler(s)"
    
    class Meta:
        tree_id = 'ehragent_apps_install_profile'  

class DirectAddressEndpointsDataInline(dbmBaseAdminTabularInline):
    model = Instance
    form = DirectAddressEndpointsAdminForm

    fields          = ('name_as_link', 'direct_address', 'direct_address_suffix', 'mu_reporting_endpoint', 'mu_reporting_source_system_name', 'mu_reporting_type', 
                       'thumbprint', 'mu_reporting_login', 'mu_reporting_password', 'mu_reporting_app_name', 'mu_reporting_community_oid')
    readonly_fields = ['name_as_link']

    class Meta:
        help_text = get_grid_help_text('This table consolidates all configurations of Direct addresses and Reporting endpoints in one place. The configuration can be done in this page and in each EHR Instance page. Each EHR Instance should have a unique Direct Address. When relevant, configure the end point URL to send the numerator data for this EHR Instance to external reporting systems.')


class DirectAddressEndpointsAdmin(dbmModelAdmin):
    model = DirectAddressEndpointsPage
    inlines = [DirectAddressEndpointsDataInline]
    change_form_template = 'admin/dbmconfigapp/change_form.html'

    class Meta:
        tree_id = "mu_reporting_endpoint"
    class Media:
        js = ['admin/js/externalapps/direct_addresses.js']


admin.site.register(EHR, EhrAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(InstanceProperties, InstancePropertiesAdmin)
admin.site.register(AppId, AppIdAdmin)
admin.site.register(InstallationProfile, InstallationProfileAdmin)
admin.site.register(DirectAddressEndpointsPage, DirectAddressEndpointsAdmin)
