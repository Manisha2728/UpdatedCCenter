from django.contrib import admin, messages
from dbmconfigapp.admin.dbm_ModelAdmin import dbmBaseModelAdmin, ServicesToRestart, dbmBaseAdminStackedInline, dbmBaseAdminTabularInline, get_grid_help_text, dbmBaseAdminStackedInline_Simple,dbmModelAdmin
from security.models import *
from security.forms import *
import copy
from django.utils.encoding import force_text
import logging

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


def create_multiline_cell(queryset, field_name):
    table =  '<table>'
    for value in queryset.values(field_name):
        table = table + '<tr><td>'
        table = table + value[field_name]
        table = table + '</td></tr>'
    table = table + '</table>'
    return table

def Clone_Selected(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
Clone_Selected.short_description = "Clone selected record"

def copy_Selected(modeladmin, request, queryset):
    # sd is an instance of SemesterDetails
    for sd in queryset:
        sd_copy = copy.copy(sd) # (2) django copy object
        sd_copy.id = None   # (3) set 'id' to None to create new object
        
        n=1
        while(n<256):
            try:
                sd_copy.domain_name = sd.domain_name +'_Copy('+str(n)+')'
                sd_copy.domain_id = n
                sd_copy.save()    # initial save
                n=256
            except:
                n=n+1
            

        # (4) copy M2M relationship: instructors
        for SI in sd.samlissuers_set.all():
            SI_Copy = copy.copy(SI)
            SI_Copy.id = None
            SI_Copy.domain_name = sd_copy
            SI_Copy.save()
            sd_copy.samlissuers_set.add(SI_Copy)
            
 
        sd_copy.save()  # (7) save the copy to the database for M2M relations
        
        #log history
        log_copy(request, sd_copy, sd, sd_copy.domain_name)
        
copy_Selected.short_description = "Make a Copy of selected Active Directory Provider"

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

class SIsuerInline(dbmBaseAdminTabularInline):
    #template = 'admin/edit_inline/authority_systems_tabular.html'
    extra = 1
    model = SAMLIssuers
    
    def get_services_to_restart(self):
        qs = super(SIsuerInline, self).get_services_to_restart()
        output = list(qs)
        output += Service.objects.filter(code_name__in=['CareBoard','ClinicalViewer','SecurityManagement'])
        return output
    
    class Meta:
        help_text = """This configuration is used for authentication of users who use Single Sign On (SSO) between the External EHR and the dbMotion application.<br/>Each Active Directory domain can have multiple Issuers with different names and the same or different Certificates. The Security Authority uses the Certificate to authenticate and validate SAML Tokens."""

class ADAttributesMappingInline(dbmBaseAdminTabularInline):
    model = ADProviders
    fields          = ('ad_mapping_FirstName', 'ad_mapping_LastName', 'ad_mapping_Title', 'ad_mapping_Description', 'ad_mapping_Facility','ad_mapping_NationalIdNumber')
 
    class Meta:
        help_text = get_grid_help_text('Define the attribute mappings between the dbMotion User Profile properties and the Active Directory.')


class ManagedUsersAdmin(BaseAdmin):
    
    list_display = ('domain_name','domain_port','container','trusted_ad','untrusted_ad_user_name','SAML_Issuer_Name','SAML_Issuer_Certificate_Thumbprint')
    list_display_links = ('domain_name',)
    model = ADProviders
    form = ADProvidersForm
    ordering = ('domain_id',)
    actions = [copy_Selected,'delete_adprovider']
    inlines=[SIsuerInline, ]
    fieldsets = (
        (model._meta.history_meta_label, {
            'fields': ('domain_id', 'domain_name','domain_port','container','untrusted_ad','untrusted_ad_user_name','untrusted_ad_user_password'), 'classes': ['wide', ]}),
        ('Mapping of Active Directory Attributes to dbMotion Profile Properties', {
            'fields': ('ad_mapping_FirstName', 'ad_mapping_LastName', 'ad_mapping_Title', 'ad_mapping_Description', 'ad_mapping_Facility','ad_mapping_NationalIdNumber'),  'description':"""This configuration is used to map the properties of the dbMotion User Profile in the Security Service with the user properties in the Active Directory.""", 'classes': ['wide', ]}),
        ('Additional Settings', {
            'fields': ('netbios_domain_name', 'use_dnl_format', 'helios','allow_alternative_authentication'), 'classes': ['wide', ]}),
    )
    
    def trusted_ad(self, obj):
        if obj.untrusted_ad:
            return "Untrusted"
        else:
            return "Trusted"
        
    trusted_ad.boolean = False
    trusted_ad.admin_order_field = 'untrusted_ad'
    trusted_ad.short_description  = 'Trusted Active Directory'
    
    def SAML_Issuer_Name(self, obj):
        return create_multiline_cell(obj.samlissuers_set.order_by('saml_issuer_name'), 'saml_issuer_name')
    
    def SAML_Issuer_Certificate_Thumbprint(self, obj):
        return create_multiline_cell(obj.samlissuers_set.order_by('saml_issuer_name'), 'saml_certificate_thumbprint')
    
    SAML_Issuer_Name.allow_tags = True
    SAML_Issuer_Name.short_description = 'SAML Issuer Name'
    
    SAML_Issuer_Certificate_Thumbprint.allow_tags = True
    SAML_Issuer_Certificate_Thumbprint.short_description = 'SAML Certificate Thumbprint'
    
    def get_actions(self, request):
        actions = super(ManagedUsersAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_adprovider(self, request, queryset):
        for adprovider in queryset:
            allow_delete = adprovider.has_constraints()
            if (allow_delete == "can_delete"):
                adprovider.delete()
                self.log_deletion(request, adprovider, None)
                self.message_user(request, adprovider.domain_name + ' was deleted successfully.', messages.SUCCESS)
            else:
                message = '%s with ID: %d has users assigned, please delete all assigned users to this active directory in "dbMotion Security Management" in order to delete it' %(adprovider.domain_name, adprovider.domain_id)
                self.message_user(request, message, messages.ERROR)

    delete_adprovider.short_description = "Delete Selected Active Directory Provider"
    
    def get_services_to_restart(self):
        qs = super(ManagedUsersAdmin, self).get_services_to_restart()
        output = list(qs)
        output += Service.objects.filter(code_name__in=['CareBoard','ClinicalViewer','SecurityManagement'])
        return output
    
    class Meta:
        tree_id = 'security_managedusers'
    class Media:
        js = ['admin/js/security/adprovider.js']  


# Unmanaged Users
def copy_SelectedAppDomain(modeladmin, request, queryset):

    for ad in queryset:
        ad_copy = copy.copy(ad) # (2) django copy object
        ad_copy.id = None   # (3) set 'id' to None to create new object
        ad_copy.application_domain_qualifier = ad.application_domain_qualifier +'_Copy'
        ad_copy.save()    # initial save
        
        # (4) copy M2M relationship: instructors
        for SI in ad.samlissuersunmanaged_set.all():
            SI_Copy = copy.copy(SI)
            SI_Copy.id = None
            SI_Copy.application_domain_qualifier = ad_copy
            SI_Copy.save()
            ad_copy.samlissuersunmanaged_set.add(SI_Copy)
            
 
        ad_copy.save()  # (7) save the copy to the database for M2M relations
        #log history
        log_copy(request, ad_copy, ad, ad_copy.application_domain_qualifier)


copy_SelectedAppDomain.short_description = "Make a Copy of selected Application Domain Qualifier"

class SAMLIsuerUnmanagedInline(dbmBaseAdminTabularInline):
    extra = 1
    model = SAMLIssuersUnmanaged

class UnmanagedUsersAdmin(BaseAdmin):
    
    list_display = ('application_domain_qualifier', 'default_role', 'SAML_Issuer_Name','SAML_Issuer_Certificate_Thumbprint')
    model = ApplicationDomains
    ordering = ('application_domain_qualifier',)
    actions = [copy_SelectedAppDomain]
    inlines=[SAMLIsuerUnmanagedInline]
       
    def SAML_Issuer_Name(self, obj):
        return create_multiline_cell(obj.samlissuersunmanaged_set.order_by('saml_issuer_name'), 'saml_issuer_name')
    
    def SAML_Issuer_Certificate_Thumbprint(self, obj):
        return create_multiline_cell(obj.samlissuersunmanaged_set.order_by('saml_issuer_name'), 'saml_certificate_thumbprint')
    
    SAML_Issuer_Name.allow_tags = True
    SAML_Issuer_Certificate_Thumbprint.allow_tags = True
    class Meta:
        tree_id = 'security_unmanagedusers'
    class Media:
        js = ['admin/js/security/UnmanagedUsers.js']        


# Role Mapping
# modified by tbener Jan 2017
# - added unique app id seeking
# - added error handling 
def copy_SelectedApp(modeladmin, request, queryset):
    logger = logging.getLogger('django')
    
    new_app_id_fmt = "{app}_{num:d}"
    new_app_id = ""
    
    # app is an instance of Applicationss
    for app in queryset:
        try:
            app_copy = copy.copy(app) # (2) django copy object
            app_copy.id = None   # (3) set 'id' to None to create new object
            
            # just try numbers (original_#) from 1 to 9. If all of them exist an error will be raised and trapped.
            for i in range(1, 10):
                new_app_id = new_app_id_fmt.format(app=app.application_id, num = i)
                if not Applications.objects.filter(application_id = new_app_id).exists():
                    # we found a good one. go ahead..
                    break
            
            app_copy.application_id = new_app_id
            app_copy.save()    # initial save
    
            # (4) copy M2M relationship: instructors
            for rm in app.rolemapping_set.all():
                rm_copy = copy.copy(rm)
                rm_copy.id = None
                rm_copy.application_id = app_copy
                rm_copy.save()
                app_copy.rolemapping_set.add(rm_copy)
                
     
            app_copy.save()  # (7) save the copy to the database for M2M relations
            #log history
            log_copy(request, app_copy, app, app_copy.application_id)
            
            messages.success(request, "{appfrom} copied to {appto}.".format(appfrom=app.application_id, appto=new_app_id))

        except:
            exc_class, exc, tb = sys.exc_info()     # must be first
            # write to event log
            error = "Error copying Application Role Mapping (application_id = {appid}).\n\n{err}".format(appid=app.application_id, err=exc)
            logger.error(error)
            # Message on screen
            messages.error(request, "Error copying %s." % app.application_id)

copy_SelectedApp.short_description = "Make a copy of selected Application Role Mapping"

class RoleMappingInline(dbmBaseAdminTabularInline):
    model = RoleMapping
    formset  = RoleMappingForm
    ordering = ('external_role_name',)

    extra = 1

class ApplicationsAdmin(BaseAdmin):
    
    list_display = ('application_id','External_Role_Name','Internal_Role_Name')
    model = Applications
    ordering = ('application_id',)
    actions = [copy_SelectedApp]
    inlines=[RoleMappingInline]
    page_help_text ="twst"
    
    def External_Role_Name(self, obj):
        return create_multiline_cell(obj.rolemapping_set.order_by('external_role_name'), 'external_role_name')
    
    # create_multiline_cell is not working here because of internal_role_name is taken from another table
    def Internal_Role_Name(self, obj):
        table =  '<table>'
        for sublist in obj.rolemapping_set.order_by('external_role_name'):
            table = table + '<tr><td>'
            table = table + str(sublist.internal_role_name)
            table = table + '</td></tr>'
        table = table + '</table>'
        return table
    
    External_Role_Name.allow_tags = True
    External_Role_Name.short_description = "External Application Role"
    Internal_Role_Name.allow_tags = True
    Internal_Role_Name.short_description = "dbMotion Role"
        
    class Meta:
        tree_id = 'security_rolemapping'
    class Media:
        js = ['admin/js/security/Applications.js']
        
        
class InternalRolesAdmin(BaseAdmin):
    model = InternalRoles
       
#General Definitions
class SecurityGeneralInline(dbmBaseAdminStackedInline):
    model = SecurityGeneral
    fieldsets = [              
        ('Facility Identification',   {'fields': ['activate_facility_identification','facility_identification_excluded_codes','active_encounter_validation_rule',], 'classes': ['wide', 'extrapretty']}),]

class PatientAuthorizationInline(dbmBaseAdminStackedInline):
    model = PatientAuthorization
    fieldsets = [              
        ('Patient Authorization',   {'fields': ['pas_option_local',], 'description' : '<div style=\"color:red\"><b>Important!</b> After modifying the Patient Consent Policy definition please manually <b>run the SQL Server job</b> named: <b>"AnaliticsCDR2Gateway_SetConsent"</b> in the CAG instance</div>', 'classes': ['wide', 'extrapretty']}),]
    radio_fields = {'pas_option_local': admin.VERTICAL}

class PatientProviderRelationshipInline(dbmBaseAdminStackedInline_Simple):
    model = PatientProviderRelationship
    
class SecurityGeneralAdmin(dbmModelAdmin):
    model = SecurityGeneralPage
    inlines = (SecurityGeneralInline, PatientAuthorizationInline, PatientProviderRelationshipInline)
    change_form_template = 'admin/dbmconfigapp/change_form.html'
    
    class Meta:
        tree_id = 'security_general'
    class Media:
        js = ['admin/js/security/FacilityIdentification.js']
        
admin.site.register(ADProviders, ManagedUsersAdmin)
admin.site.register(Applications, ApplicationsAdmin)
admin.site.register(InternalRoles, InternalRolesAdmin)
admin.site.register(ApplicationDomains, UnmanagedUsersAdmin)
admin.site.register(SecurityGeneralPage, SecurityGeneralAdmin)
