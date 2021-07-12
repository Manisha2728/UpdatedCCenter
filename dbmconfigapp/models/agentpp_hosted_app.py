'''
Created on Dec 1, 2015

@author: RBRILMANN
'''
from django.db import models
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel,\
    get_help_text
from django.core import validators
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from .database_storage import DatabaseStorage
from configcenter import settings
import re
from .common import Message
from django.template.defaultfilters import default


_CONTEXT_TYPE_CHOICES = (
    ('PHMode', 'PH - Agent Hub Population Health Mode'),
    ('PCMode', 'PC - Agent Hub Patient Centric Mode'),    
    )

class AgentppHostedAppPage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    
    def page_title(self):
        return 'Configure %s' % self._meta.verbose_name
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Hosted Applications"

class LauncherGeneralProperties(ConfigurationEntityBaseModel):
    page                = models.ForeignKey(AgentppHostedAppPage, on_delete=models.SET_NULL, null=True, default=1, editable=False)
    default_app         = models.ForeignKey('AgentppHostedApp', on_delete=models.SET_NULL, verbose_name='Default Application', null=True, blank=True, default=None, help_text = get_help_text("Defines the default application to be launched via the Application Launcher's middle button.", "Patient View (if the application is enabled)."))

    def __unicode__(self):
        return ''
        
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Default Application"
        verbose_name = "Default Application"
        verbose_name_plural = "Default Application"

class AgentHostedAppsBehavior(ConfigurationEntityBaseModel):
    page                = models.ForeignKey(AgentppHostedAppPage, on_delete=models.SET_NULL, null=True, default=1, editable=False)
    is_app_related_to_ehr = models.BooleanField(verbose_name='Applications visibility is related to the EHR', default=True, help_text=get_help_text(
        """Determines how Agent Hub hosted applications are displayed in relation to the EHR. Applications are operational and displayed with a patient in context in the EHR.<br/>
- False - Applications display independent of the EHR and can be minimized regardless of EHR state.<br/>
- True (default) -  Application display is dependent on Agent Hub and EHR display. Agent Hub must be displayed for the application to be displayed.""", 'True'))

    def __unicode__(self):
        return ''
        
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Hosted Applications Visibility Behavior"
        verbose_name_plural = "Hosted Applications Visibility Behavior"
        history_meta_label = verbose_name


# This manager ensures that the QuerySet will always put PV first!
class AgentppHostedAppManager(models.Manager):
    def get_queryset(self):
        return super(AgentppHostedAppManager, self).get_queryset().extra(select={'ord': "case when app_key='pv' then -1 when app_key='cva' then 0 else id end"}).order_by('ord')

 
class AgentppHostedApp(ConfigurationEntityBaseModel):
    agentpp_hosted_app_page         = models.ForeignKey('AgentppHostedAppPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    app_name                        = models.CharField(max_length=30, verbose_name='Hosted Application Name', unique=True, help_text='Hosted application name.')
    app_key                         = models.CharField(max_length=30, null=True, blank=True, help_text="Used to identify special applications")
    enabled                         = models.BooleanField(verbose_name='Enabled', default=False, help_text='Enable one or more of the following applications to be hosted by the Agent Hub.')
    LogoFile                        = models.ImageField(default='', null=False, blank=False, upload_to='AgentHostedApps/Logo', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Logo File', help_text='Define the logo file that will be displayed for the application in the Agent Hub header.')
    launch_url                      = models.CharField(default='',max_length=1000, verbose_name='Application Page URL', help_text='Define the launch URL of the hosted application.')
    get_application_state_url       = models.CharField(default='',max_length=1000, verbose_name='Application State URL', help_text='Define the URL that will be used to send the updated context information (user/patient) to the hosted application.')
    permitted_roles                 = models.CharField(null=False, blank=False, max_length=500, verbose_name='Permitted Roles', default='All', help_text = "<b>Defines the user roles which can access this application.</b><br/>Possible values: All, None, Role names separated by ','. <br/>When the value is 'All' all users will have access to this application. <br/>When certain role(s) are filled, only users having those role(s) will be able to access this application.<br/>When the value is 'None' no user can access this application.<br/>Default: All.")    
    is_user_alias_required          = models.BooleanField(verbose_name='Define if dbMotion User Aliasing Service is Required', default=False, help_text='Enable dbMotion User Aliasing Service.')   
    is_window_resizable             = models.BooleanField(verbose_name='Resizable Window', default=True, help_text='Enable the following application to have resizable window.')
    window_default_width_size       = models.IntegerField(verbose_name='Window Default Width Size', default='1024', help_text='Set window default width size.')
    window_minimal_width_size       = models.IntegerField(verbose_name='Window Minimal Width Size', default='640', help_text='Set window minimal width size.')
    window_maximal_width_size       = models.IntegerField(verbose_name='Window Maximal Width Size', null=True, blank=True, help_text='Set window maximal width size.')
    window_default_height_size      = models.IntegerField(verbose_name='Window Default Height Size', default='768', help_text='Set window default height size.')
    window_minimal_height_size      = models.IntegerField(verbose_name='Window Minimal Height Size', default='480', help_text='Set window minimal height size.')
    window_maximal_height_size      = models.IntegerField(verbose_name='Window Maximal Height Size', null=True, blank=True, help_text='Set window maximal height size.')
    display_name                    = models.CharField(max_length=100, null=True, blank=True, default=None, help_text='The name to be displayed in the Launcher.')

    objects = AgentppHostedAppManager()

    def app_name_url(self):
        if self.id:
            return '<a href="%s" onclick="return showEditPopup(this);" title="Click to edit">%s</a>' % ("/admin/dbmconfigapp/agentpphostedapp/%s/" % self.id, self.app_name)
        else:
            return '<a href="%s" onclick="return showEditPopup(this);" >Add new Application</a>' % "/admin/dbmconfigapp/agentpphostedapp/add/"
    
    app_name_url.allow_tags = True
    app_name_url.short_description = 'Hosted Application Name'
    
    def override_add_button_link(self):
        return "/admin/dbmconfigapp/agentpphostedapp/add/"
    
    def __unicode__(self):
        return self.app_name
    
    def page_title(self):
        return ''
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Patient Centric Application"
        verbose_name = "Patient Centric Application"


class AgentUserCentricApp(ConfigurationEntityBaseModel):
    agentpp_hosted_app_page         = models.ForeignKey('AgentppHostedAppPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    app_name                        = models.CharField(max_length=30, verbose_name='Hosted Application Name', unique=True, help_text='Hosted application name.')
    enabled                         = models.BooleanField(verbose_name='Enabled', default=True, help_text='Enable the following application to be hosted by the Agent Hub.')
    LogoFile                        = models.ImageField(default='', null=True, blank=True, upload_to='AgentHostedApps/Logo', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Logo File', help_text='Define the logo file that will be displayed for the application in the Agent Hub header.')
    
    def __unicode__(self):
        return ''
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Population Health Application"
        verbose_name = "Population Health Application"
       
class AgentSMARTonFHIRApp(ConfigurationEntityBaseModel):
    agentpp_hosted_app_page         = models.ForeignKey('AgentppHostedAppPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    app_name                        = models.CharField(max_length=100, verbose_name='Client Name', unique=True, help_text='Name of the SMART on FHIR application. Obtain this information from the application owner.')
    enabled                         = models.BooleanField(verbose_name='Enabled', default=False, help_text='Enable or disable the following SMART on FHIR application to be hosted by the Agent Hub.')
    client_id                       = models.CharField(max_length=100, verbose_name='Client ID', unique=True, help_text='The SMART on FHIR application ID. The Client ID should be unique for this node. Obtain this information from the application owner.')
    launch_url                      = models.CharField(max_length=100, verbose_name='Launch URL', help_text='Launch URL of the SMART on FHIR application. Obtain this information from the application owner.')
    redirect_url                    = models.CharField(max_length=100, verbose_name='Redirect URL', help_text='Redirect URL of the SMART on FHIR application. Obtain this information from the application owner.')
    logo_file                       = models.ImageField(default='', null=False, blank=False, upload_to='AgentSMARTonFHIRApps/Logo', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Logo File', help_text='Define the logo file that will be displayed for the of the SMART on FHIR application in the Agent Hub header. The logo size must be 20x20 pixels.')
    resizable_window                = models.BooleanField(verbose_name='Resizable Window', default=True, help_text='Enable the following SMART on FHIR application to have resizable window.')
    window_default_width_size       = models.IntegerField(verbose_name='Window Default Width Size', default='1024', help_text='Set window default width size.')
    window_minimal_width_size       = models.IntegerField(verbose_name='Window Minimum Width Size', default='640', help_text='Set window minimum width size.')
    window_maximal_width_size       = models.IntegerField(verbose_name='Window Maximum Width Size', default='1400', help_text='Set window maximum width size.')
    window_default_height_size      = models.IntegerField(verbose_name='Window Default Height Size', default='768', help_text='Set window default height size.')
    window_minimal_height_size      = models.IntegerField(verbose_name='Window Minimum Height Size', default='480', help_text='Set window minimum height size.')
    window_maximal_height_size      = models.IntegerField(verbose_name='Window Maximum Height Size', default='1050', help_text='Set window maximum height size.')
    use_dbmotion_fhir_server        = models.BooleanField(verbose_name='Use dbMotion FHIR Server', default=True, help_text='Enable using the dbMotion FHIR Server.')
    
    def app_name_url(self):
        if self.id:
            return '<a href="%s" onclick="return showEditPopup(this);" title="Click to edit">%s</a>' % ("/admin/dbmconfigapp/agentsmartonfhirapp/%s/" % self.id, self.app_name)
        else:
            return '<a href="%s" onclick="return showEditPopup(this);" >Add new Application</a>' % "/admin/dbmconfigapp/agentsmartonfhirapp/add/"
    
    app_name_url.allow_tags = True
    app_name_url.short_description = 'Client Name'
    
    def override_add_button_link(self):
        return "/admin/dbmconfigapp/agentsmartonfhirapp/add/"
    
    def __unicode__(self):
        return self.app_name
    
    def page_title(self):
        return ''
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "SMART on FHIR Application"
        verbose_name = "SMART on FHIR Application"       
