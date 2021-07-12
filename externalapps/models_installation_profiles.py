'''
Created on Aug 6, 2017

@author: EBLIACHER
'''
from django.db import models
from dbmconfigapp.models.base import ConfigurationEntityBaseModel, get_help_text
from dbmconfigapp.utils import custom_validators
from configcenter.settings import get_param
from django.forms import ModelForm
from django import forms
import datetime
from django.utils import timezone
from django.forms.utils import ErrorList
from externalapps.utils import log_exception

def fill_server_name():
    try:                    
        return get_param('application_server_statefull', '')          
    except:
        return ''

def fill_node_absolute_domain():
    try:                    
        return get_param('default_domain_name', '')          
    except:
        return ''  
    
def fill_default_language():
    try:                    
        return get_param('default_language', '')          
    except:
        return ''

def fill_default_CONFIG_SERVER_URL():
    return 'https://{0}.{1}/SmartAgent/Config/'.format(fill_server_name(),fill_node_absolute_domain())

def fill_default_PRODUCT_SERVER_URL():
    return 'https://{0}.{1}/SmartAgent/AgentSetup/[Pofile Name]/EhrAgentUpdate.zip'.format(fill_server_name(),fill_node_absolute_domain())

# we need to keep this for backward compatibility (upgrade from 17.1 CU2)
def fill_cv_app_name():
    try:
        return get_param('cv_app_name', '')
    except:
        return ''
        
class InstallationProfile(ConfigurationEntityBaseModel):        
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True, verbose_name='Name', default='', help_text=get_help_text("Name.", ''))
    product_server_url = models.CharField(max_length=500, verbose_name='Product Server URL', blank=True, null=True, help_text="Used by the update service to download new client versions when using a File System path<br/><i>(e.g. \\networkdrive\sharedfolder\EhrAgentUpdate.zip)</i><br/>If this value is not a File System path, Agent will get new client versions based on the Profile, Web Server and Domain values.<br/><b>Name of XML Element:</b>SMART_AGENT_PRODUCT_SERVER_URL<br/>For Agent client versions older than 19.2 CU2 to use this configuration, it's needed to activate access to this URL.<br/>Refer to the product documentation for more information.")
    is_auto_run = models.BooleanField(default=True, verbose_name='Auto Run', help_text=get_help_text('Determines whether the Agent Hub starts immediately after installation and also with the client machine restart.<br/><b>Name of XML Element:</b>SMART_AGENT_AUTO_RUN', 'True'))
    is_install_ccow_context_receiver = models.BooleanField(default=False, verbose_name='Install CCOW Context Receiver', help_text=get_help_text('Indicates whether or not to install the Context Manager Lite.<br/><b>Name of XML Element:</b>SMART_AGENT_INSTALL_CCOW_CONTEXT_RECEIVER', 'False'))
    is_install_dbm_context_receiver = models.BooleanField(default=False, verbose_name='Install DBM Context Receiver', help_text=get_help_text('If set to true, enables the Agent Hub Context Manager Lite and a third party context manager (for example, Sentillion) to work together on the same machine.<br/><b>Name of XML Element:</b>SMART_AGENT_INSTALL_DBM_CONTEXT_RECEIVER', 'False'))
    is_launch_api = models.BooleanField(default=False, verbose_name='Launch API Service Mode', help_text=get_help_text('Not supported yet.<br/><b>Name of XML Element:</b>SMART_AGENT_LAUNCH_API_SERVICE_MODE', 'False'))
    profile_name = models.CharField(max_length=100, verbose_name='Profile Name', default=fill_server_name, help_text=get_help_text("Server name.<br/><b>Name of XML Element:</b>SMART_AGENT_PROFILE_NAME", fill_server_name()))
    is_show_system_tray_icon = models.BooleanField(default=True, verbose_name='Show System Tray Icon', help_text=get_help_text('Determines whether the Agent Hub displays the System Tray icon.<br/><b>Name of XML Element:</b>SMART_AGENT_SHOW_SYSTEM_TRAY_ICON', 'True'))
    web_server_stateful = models.CharField(max_length=500, verbose_name='Node Web Server Stateful', default=fill_server_name, help_text=get_help_text("Server name.<br/>For NLB configurations, it defines the stateful VIP Address.<br/>Together with Node User Absolute Domain configuration, it configure the New Product versions URL and download configurations URL.<br/>The default value for New Product versions URL and download configurations URL are:<br/>- {0}<br/>- {1}<br/><b>Name of XML Element:</b>_NODE_WEB_SERVER_STATEFUL, SMART_AGENT_CONFIG_SERVER_URL and SMART_AGENT_PRODUCT_SERVER_URL".format(fill_default_PRODUCT_SERVER_URL(), fill_default_CONFIG_SERVER_URL()), fill_server_name()))
    user_absolute_domain = models.CharField(max_length=100, verbose_name='Node User Absolute Domain', default=fill_node_absolute_domain, help_text=get_help_text("AD Domain.<br/><b>Name of XML Element:</b>_NODE_USER_ABSOLUTE_DOMAIN", fill_node_absolute_domain()))
    is_multitenant = models.BooleanField(default=False, verbose_name='Is Multitenant', help_text=get_help_text('Determines whether the Agent Hub is configured in multitenant mode.<b>Note:</b> If this is set to true, the update mechanism is disabled and the update configurations are not relevant.<br/><b>Name of XML Element:</b>ISMULTITENANT', 'False'))
    is_uninstall_previous_version = models.BooleanField(default=True, verbose_name='Uninstall Previous Versions', help_text=get_help_text('If set to false, upon first time installation will remove existing Agent Hub version.<br/><b>Name of XML Element:</b>SMART_AGENT_UNINSTALL_PREVIOUS_VERSIONS', 'True'))
    is_update_configuration_enabled = models.BooleanField(default=True, verbose_name='Enable Update Configuration', help_text=get_help_text('Determines whether the Agent Hub client will update the configuration files automatically.<br/><b>Name of XML Element:</b>SMART_AGENT_UPDATE_CONFIGURATION_ENABLED', 'True'))
    is_update_new_version_enabled = models.BooleanField(default=False, verbose_name='Enable Update New Version', help_text=get_help_text('Determines whether Agent Hub will upgrade to a new version automatically via the Easy Deployment process.<br/>Note: When setting this option to <b>true</b>, the update service will run under a local system account, which runs with administrator permissions.<br/><b>Name of XML Element:</b>SMART_AGENT_UPDATE_NEW_VERSION_ENABLED', 'False'))
    is_activate_ccow_receiver = models.BooleanField(default=False, verbose_name='No Activation of CCOW Context Receiver', help_text=get_help_text('If true, Agent Hub installation will not create a registry key for auto launch of the Agent Hub by EMR context join request.<br/><b>Name of XML Element:</b>SMART_AGENT_CCOW_CONTEXT_RECEIVER_NO_ACTIVATION', 'False'))
    is_display_alert_message = models.BooleanField(default=False, verbose_name='Display EHR Alert Messages', help_text=get_help_text('If false, the Agent Hub first installation will not display a popup message to close the EHRs.<br/><b>Name of XML Element:</b>DISPLAY_EHR_ALERT_MESSAGE', 'False'))
    is_ccow_isolated_session = models.BooleanField(default=False, verbose_name='Enable CCOW Isolating Session Manager', help_text=get_help_text('If set to true, enables users to work in shared desktop mode.<br/><b>Note:</b> If set to true, SMART_AGENT_INSTALL_CCOW_CONTEXT_RECEIVER must also be set to true.<br/><b>Name of XML Element:</b>CCOW_ISOLATING_SESSION_MANAGER_ENABLED', 'False'))
    display_lang = models.CharField(max_length=100, verbose_name='Display Language', default=fill_default_language, help_text=get_help_text("Display language and also regional setting behavior.<br/><b>Name of XML Element:</b>SMART_AGENT_DISPLAY_LANGUAGE", fill_default_language()))
    install_url = models.TextField(verbose_name='Installation URL', help_text='Link to the first time installation file. This link can be used to allow secure access to installation files.<br/>The link URL will be created when saving the Installation Profile.', blank=True, null=True)
    install_url_expiration_date = models.DateField(verbose_name='Expiration Date', null=True)
        
    def save(self, *args, **kwargs):
        if(self.id == None):
            self.id = InstallationProfile.objects.latest('id').id + 1
        super(InstallationProfile, self).save(*args, **kwargs)
        
        
    def __unicode__(self):
        return self.profile_name
               
              
    class Meta:
        app_label = "externalapps"
        verbose_name = 'EHR Agent Installation Profiles'                
        verbose_name_plural = 'EHR Agent Installation Profiles'
        history_meta_label = verbose_name_plural
        help_text = """
        This configuration is used to define set of the installation profiles.
        
        <br/>To add a node, select the required row and click Action -> Duplicate existing installation profiler(s). Then click Go.. 
        <br/>To delete a node, select the required row and click Action -> Delete installation profiler(s). Then click Go.
        <br/>To change a node configuration, click on the profile name and edit the profile properties as required.<br><br>
        """
class InstallationProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstallationProfileForm, self).__init__(*args, **kwargs)
        self.fields['install_url_expiration_date'].required = False

    def clean(self):
        from sys import path
        # import clr

        cleaned_data = super(InstallationProfileForm, self).clean()
      
        server = cleaned_data.get('web_server_stateful')
        domain = cleaned_data.get('user_absolute_domain')
        profile_name = cleaned_data.get('name')
        if server is None or domain is None or profile_name is None:
            return cleaned_data

        expiration_date = cleaned_data.get('install_url_expiration_date')
        if(expiration_date is None):
            if(self.data.get('install_url_expiration_date') != ''):
                return cleaned_data
            cleaned_data['install_url'] = None
            return cleaned_data
        # django saves time as 00:00:00 but we need expiration date to be end of day
        expiration_date_str = expiration_date.strftime('%Y-%m-%d') + ' 23:59:59'

        try:
            a=''
            #path.append(r"C:\Program Files\dbMotion\Web\Sites\CVA\Server\Bin")
            #clr.AddReference("dbMotion.CVA.Server.Business")

            #from dbMotion.CVA.Server.Business.AgentInstallationProfiles.Packaging import ProfileSetupLink

            #profile_setup_link = ProfileSetupLink ()
            #cleaned_data['install_url'] = profile_setup_link.Create(server, domain, profile_name, expiration_date_str)
        except Exception as ex:
            msg = "Unexpected error occurred. See CCenter event log for details"
            self._errors['install_url'] = ErrorList([msg])

            log_exception(ex, 'Create Installation URL failed.')

        return cleaned_data

    class Meta:
        model = InstallationProfile
        fields = ['name', 'product_server_url', 'is_auto_run', 'is_install_ccow_context_receiver', 'is_install_dbm_context_receiver', 'is_launch_api', 'profile_name', 'is_show_system_tray_icon', 'web_server_stateful', 'user_absolute_domain', 'is_multitenant', 'is_uninstall_previous_version', 'is_update_configuration_enabled', 'is_update_new_version_enabled', 'is_activate_ccow_receiver', 'is_display_alert_message', 'is_ccow_isolated_session', 'display_lang', 'install_url_expiration_date', 'install_url']
        widgets = {
            'name': forms.TextInput(attrs={'size':'50'}),
            'profile_name': forms.TextInput(attrs={'size':'50'}),
            'user_absolute_domain': forms.TextInput(attrs={'size':'50'}),
            'install_url': forms.Textarea(attrs={'rows':4, 'cols':150})
        }