from django.db import models
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel, get_help_text
from .database_storage import DatabaseStorage
from configcenter import settings
from configcenter.settings import get_param


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


def fill_agent_hub_base_url():
    try:                        
        return '{0}.{1}'.format(fill_server_name(), fill_node_absolute_domain())
    except:
        return ''

def fill_agent_service_endpoint():
    try:                        
        return 'https://{0}.{1}/SmartAgent/SmartAgentWebService.svc'.format(fill_server_name(), fill_node_absolute_domain())
    except:
        return ''
        
def fill_cv_url():
    try:            
        return 'https://{0}.{1}/dbMotionClinicalViewer/ApplicativeDomains/Host/PublicPages/Dispatcher.aspx'.format(fill_server_name(), fill_node_absolute_domain())
    except:
        return ''  

def fill_collaborate_url():
    try:            
        return 'https://{0}.{1}/collaborate/dbmotion/frontend/security/authentication/dbmPrincipal.v2.api'.format(fill_server_name(), fill_node_absolute_domain())
    except:
        return '' 

MY_EHR_DATA_VIEW_CHOICES = (
    ('False', 'Delta view'),
    ('True', 'Show All view')
    )

BULK_ACTIONS_CHOICES = (
    ('Print', 'Print'),
    ('SendToMyEhr', 'Send')
    )

DISPLAY_CONTENT_DESCRIPRTOR_CHOICES = (
    ('False', 'Display the Code Designation'),
    ('True', 'Display the Original Message Text')
    )

DEFAULT_CHOICE = 0

        
class EhrAgentGeneral(ConfigurationEntityBaseModel):
    pv_parent                       = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    my_ehr_data_default_view        = models.CharField(verbose_name='Initial data view', max_length=5, choices=MY_EHR_DATA_VIEW_CHOICES, default="False", null=False, help_text=get_help_text('Determines whether the Delta view or Show All view is displayed by default when first opening the Patient View or EHR Agent.', MY_EHR_DATA_VIEW_CHOICES[0][1]))
    default_bulk_action             = models.CharField(verbose_name='Default bulk action', max_length=20, choices=BULK_ACTIONS_CHOICES, default="Print", null=False, help_text=get_help_text('Defines the default action displayed in the Bulk action button.', BULK_ACTIONS_CHOICES[0][1]))
    reset_bulk_action               = models.BooleanField( verbose_name='Reset bulk action to default after bulk action', default=True, help_text=get_help_text('Determines whether to reset the bulk action to the default action after the performing the action (after clicking the Go button).', 'True'))
    clean_checkboxes_after_bulk_action = models.BooleanField( verbose_name='Clear checkboxes after bulk action', default=True, help_text=get_help_text('Determines whether to clear the bulk action checkboxes after performing the action.', 'True'))
    get_all_data_button_available   = models.BooleanField( verbose_name='Display Get All Data button', default=True, help_text=get_help_text('Determines whether to display the Get All Data button in the Time Filter Settings window.', 'True'))
    show_launch_collaborate         = models.BooleanField( verbose_name='Display Launch Collaborate menu option', default=False, help_text=get_help_text('Determines whether to display the Launch Collaborate menu option.', 'False'))
    show_send_feedback              = models.BooleanField( verbose_name='Display Send Feedback Menu Option', default=True, help_text=get_help_text('Determines whether to display the Send Feedback option in the EHR Agent More Options menu.', 'True'))
    enable_patient_mapping          = models.BooleanField(verbose_name='Patient Mapping Agent', default=False, help_text=get_help_text('Determines whether the Patient Mapping Agent is enabled. dbMotion Context Receiver supports a Patient Mapping Agent that is able to receive different patient IDs from each participant that belongs to the same patient. The Patient Mapping Agent, as part of the common context system, maps the identifiers for patients. Whenever an application sets the patient context, the context manager instructs the patient mapping agent (if present) to provide any additional identifiers it knows for the patient.', 'False'))
    #header_logo                     = models.ImageField(default='', null=True, blank=True, upload_to='EhrAgent/HeaderLogo', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Header Logo File', help_text='Defines the logo presented in the EHR Agent Header.<br/>The following are the logo image type and size requirements:<br/>Type: png<br/>Height: 38px<br/>Width: 38px<br/><i>Default: No default value</i>')
    footer_logo                     = models.ImageField(default='', null=True, blank=True, upload_to='EhrAgent/FooterLogo', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Footer Logo File', help_text='Defines the logo displayed in the Clinical View Agent Footer.<br/>The following are the logo image type and size requirements:<br/>Type: png<br/>Height max size: 38px<br/>Width max size: 115px<br/>If one of the image dimensions (Height or Width) is larger than the maximum size, the image will be reduced with the lock aspect ratio.<br/><i>Default: No default value</i>')
    enable_cv_from_patient_name     = models.BooleanField(verbose_name='Launch CV from Patient Name in Agent Hub', default=True, help_text=get_help_text('Determines whether Clinical Viewer can be launch from the patient name ', 'True'))
    def __unicode__(self):
        return ''       
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "EHR Agent General"
        history_meta_label = "EHR Agent General"
   



class EhrAgentBaseUrl(ConfigurationEntityBaseModel):
    agenthub_general_page           = models.ForeignKey('AgentHubGeneralPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    base_url                        = models.CharField(verbose_name='Agent Hub base URL configuration', null=False, max_length=200, help_text=get_help_text("This is the full qualified domain name for dbMotion's web server. This will be used to build URLs for Collaborate, CV and Agent Service endpoint.<br/>For the default value the following URLs will be used:<br/>"+ fill_agent_service_endpoint()+"<br/>"+fill_cv_url()+"<br/>"+fill_collaborate_url(), fill_agent_hub_base_url()), default=fill_agent_hub_base_url)
    
    def __unicode__(self):
        return "EHR Agent General"   
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "EHR Agent General"        
        

class EhrAgentHelp(ConfigurationEntityBaseModel):
    agentpp_hosted_app_page         = models.ForeignKey('AgentppHostedAppPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    link_name           = models.CharField(verbose_name='Link name', max_length=200, unique=True)
    link_url            = models.CharField(verbose_name='URL', max_length=200)
    
    def __unicode__(self):
        return self.link_name
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Help Link'
        history_meta_label = 'Help Links'
        
    
