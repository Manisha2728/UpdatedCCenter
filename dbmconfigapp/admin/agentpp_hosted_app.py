'''
Created on Dec 1, 2015

@author: RBRILMANN
'''
from dbmconfigapp.models.culture import Culture, CurrentCulture
from dbmconfigapp.models.agentpp_hosted_app import AgentppHostedApp, AgentppHostedAppPage, AgentUserCentricApp, AgentSMARTonFHIRApp, LauncherGeneralProperties, AgentHostedAppsBehavior
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline_Simple, get_grid_help_text, dbmBaseAdminTabularInline,dbmBaseAdminStackedInline
from dbmconfigapp.form.ehragent_forms import  AgentppHostedAppInlineFormset, LauncherGeneralPropertiesForm
from django.contrib import admin
from dbmconfigapp.models.ehragent import *
from django import forms

     
class AgentHostedAppsBehaviorInline(dbmBaseAdminStackedInline_Simple):
    model = AgentHostedAppsBehavior

    fieldsets = (
        (None, {
            'fields': ('is_app_related_to_ehr',),
            'classes': ('wide', 'extrapretty')
        }),
    )

class NewLauncherGeneralPropertiesInline(dbmBaseAdminStackedInline_Simple):
    model = LauncherGeneralProperties
    form = LauncherGeneralPropertiesForm

    fieldsets = (
        (None, {
            'fields': ('default_app',),
            'classes': ('wide', 'extrapretty')
        }),
    )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(NewLauncherGeneralPropertiesInline, self).get_formset(request, obj, **kwargs)
        formset.form.base_fields['default_app'].widget.can_add_related = False
        return formset


class AgentppHostedAppInline(dbmBaseAdminTabularInline):
    model = AgentppHostedApp
    fields = ('app_name_url', 'enabled', 'LogoFile', 'launch_url','get_application_state_url')
    readonly_fields = ('app_name_url', 'launch_url', 'get_application_state_url')
    formset = AgentppHostedAppInlineFormset
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    class Meta:
        help_text = get_grid_help_text('Define one or more Patient Centric applications to be hosted by the Agent Hub:<br/>In addition,  for each application you need configure the application logo to be displayed in the Agent Hub header.<br/>The logo size must be 24x24 pixels.')
        add_link = "/admin/dbmconfigapp/agentpphostedapp/add/"
  
class AgentHostedAppAdmin(dbmModelAdmin):
    model = AgentppHostedApp    
    fieldsets = [              
        ('Hosted Application settings',
            {'fields': ['app_name', 'LogoFile', 'launch_url', 'get_application_state_url', 'permitted_roles', 'is_user_alias_required', 'is_window_resizable', 
                        ('window_default_width_size', 'window_default_height_size'), ('window_minimal_width_size', 'window_minimal_height_size')]}),
        ('HiddenSection',
            {'fields': ['app_key',]}),
        ]
    #readonly_fields = ('use_dbmotion_fhir_server',)
    class Media:        
        js = ['admin/js/dbmconfigapp/HostedApplicationEdit.js']
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True  
    
class AgentUserCentricAppInline(dbmBaseAdminTabularInline):
    model = AgentUserCentricApp
    fields = ('app_name', 'enabled', 'LogoFile',)
    readonly_fields = ('app_name',)
    #formset = AgentppHostedAppInlineFormset
    
    class Meta:
        help_text = get_grid_help_text('Enable the Patient List application to be hosted by the Agent Hub.<br/>In addition,  you can configure the application logo to be displayed in the Agent Hub header.<br/>The logo size must be 20x20 pixels.')
     


class AgentSMARTonFHIRAppInLine(dbmBaseAdminTabularInline):
    model = AgentSMARTonFHIRApp
    fields = ('app_name_url', 'enabled', 'logo_file', 'client_id', 'launch_url', 'redirect_url')
    readonly_fields = ('app_name_url', 'client_id', 'launch_url', 'redirect_url')
    extra = 0
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    class Meta:
        help_text = get_grid_help_text("""Define the list of SMART on FHIR applications to be hosted by Agent Hub.<br/>The defined hosted SMART on FHIR applications will be visible in the Patient Centric Applications workflow of the Agent Hub.<br/>Currently only applications that use dbMotion FHIR Server are supported.<br/>In addition, 
        configure the application logo to be displayed in the Agent Hub header.<br/>
        The logo size must be 20x20 pixels.<br/><br/>In order to configure the launching of a remote CV, add the remote CV address in the launch URL field, with the prefix [CV],<br/> 
        such as [CV]https://ServerName.dbMotion.loc/dbMotionClinicalViewer
        and configure a unique Client Name and Client ID.<br/>
        Refer to the product documentation for more information.""")
        add_link = "/admin/dbmconfigapp/agentsmartonfhirapp/add/"

class AgentSMARTonFHIRAppAdmin(dbmModelAdmin):
    model = AgentSMARTonFHIRApp
    
    fieldsets = [              
        ('SMART on FHIR Application settings',
            {'fields': ['app_name', 'client_id', 'launch_url', 'redirect_url', 'logo_file', 'use_dbmotion_fhir_server', 'resizable_window', ('window_default_width_size', 'window_default_height_size'), ('window_minimal_width_size', 'window_minimal_height_size'), ('window_maximal_width_size', 'window_maximal_height_size')]}),
        ]
    readonly_fields = ('use_dbmotion_fhir_server',)
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True    
        
class EhrAgentHelpInline(dbmBaseAdminTabularInline):
    model = EhrAgentHelp
    #formset = EhrAgentHelpInlineForm
    fields = ('link_name', 'link_url')
    extra = 1
    verbose_name_plural = model._meta.history_meta_label
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    class Meta:
        help_text = get_grid_help_text('This configuration enables you to configure additional help elements and other options to be displayed in system tray menu.', 'Link name: "dbMotion System Info", URL: "/dbMotionInformationServices/dbMotionInformationPage.aspx"')
    

class AgentppHostedAppAdmin(dbmModelAdmin):
    model = AgentppHostedAppPage
    inlines = (AgentHostedAppsBehaviorInline, AgentppHostedAppInline, NewLauncherGeneralPropertiesInline, AgentSMARTonFHIRAppInLine,EhrAgentHelpInline)
    exclude = ('page_help_text', 'page_name', 'services')
    class Media:        
        js = ['admin/js/dbmconfigapp/HostedApplications.js']   


