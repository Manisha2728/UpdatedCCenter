from dbmconfigapp.models.base import *
from security.models import ADProviders
from .database_storage import DatabaseStorage
from django.core import validators
from dbmconfigapp.utils.custom_validators import *
from dbmconfigapp.utils import  encryption
from via.models import InitiateMappings
# MODEL

Default_landing_page = (
    (0, 'Patient Summary'),
    (1, 'View by Category'),
    (2, 'View by Date'),
)

LOGO_MAX_WIDTH = 1080
LOGO_MAX_HEIGHT = 1920


class PatientViewPage(PageBaseModel):
    
    def page_title(self):
        return "Set Patient View Settings"
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Set Patient View Settings"


class PatientViewGeneralDefinitions(ConfigurationEntityBaseModel):
    patient_view_page = models.ForeignKey(PatientViewPage, on_delete=models.CASCADE, default=1)
    default_domain = models.ForeignKey(ADProviders, default='', null=True, blank=True, verbose_name="Default Active Directory Domain", on_delete=models.SET_NULL, help_text='This configuration is to define the default active directory domain in Login page of standalone mode.<br/>The Domain must be added first to the list in Active directory domains.<br/><i>Default: N/A</i>')
    default_logofile = models.ImageField(default='', null=True, blank=True, upload_to='PatientView/Logo', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Logo Image', help_text='Defines the default logo presented in the Login Page.<br/>The following are the logo image type and size requirements:<br/>Type: PNG<br/>Height: 28px<br/>Width: 304px<br/><i>Default: Allscripts Logo</i>')
    project_name = models.CharField(verbose_name='Project Name', blank=True, max_length=35, default='', help_text='This configuration is to define the default Project Name presented in the Login Page.<br/><i>Default: dbMotion&trade; Solution</i>')
    background_image = models.ImageField(default='', null=True, blank=True, upload_to='PatientView/BackgroundImage', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Background Image', help_text='Defines the background image displayed in the Login Page.<br/>The following are the background image type and size requirements:<br/>Type: JPEG, PNG, BMP, GIF<br/>Height: %spx<br/>Width: %spx<br/>Weight: Upto 2MB<br/><i>Default: Solid #f2f2f2 Background color</i>' % (LOGO_MAX_WIDTH, LOGO_MAX_HEIGHT))

    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = "Set Patient View Settings"

class CarequalityIntegrationSettingsPage(PageBaseModel):
    
    def page_title(self):
        return "Set Carequality Integration Settings"
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Set Carequality Integration Settings"

class CarequalityIntegrationSettingsModel(ConfigurationEntityBaseModel):
    page                                        = models.ForeignKey('CarequalityIntegrationSettingsPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    enable_carequality_integration              = models.BooleanField( verbose_name='Enable Carequality Integration', default=False, help_text=get_help_text('Determines whether to enable or disable Carequality Integration.<br/>For detailed implementation instructions, see the IHE Integration Implementation Guide.', 'False'))
    home_community_id                           = models.CharField(verbose_name='Home Community ID:', blank=True, max_length=400, default='(Enter your Home Community ID)', help_text=get_help_text('Defines the dbMotion Home Community ID (OID) for outbound requests to Carequality.<br/>This value can be obtained from Allscripts Community Configuration Manager (CCM).<br/>The OID format should be: urn:oid:n.n.n.n.n.n. For example: urn:oid:2.16.840.1.113883.3.57.1.3.0.2.','Empty'))
    certificate_thumptrint                      = models.CharField(verbose_name='Certificate Thumprint:', blank=True, max_length=400, default='(Enter your Certificate Thumbprint)', help_text=get_help_text('Defines the Certificate Thumbprint for HTTPS connections to Allscripts Brokering Responding Gateway.<br/>The Certificate must be downloaded from the Allscripts Community Configuration Manager (CCM) and installed on the Application server.','Empty'))
    patient_discovery_endpoint                  = models.CharField(verbose_name='Patient Discovery Endpoint:', blank=True, max_length=400, default='https://brokeringrespondinggateway- /iti55/<CQ Participant OID>/outbound', help_text=get_help_text('URL to Allscripts Brokering Responding Gateway for IHE Transaction ITI-55 Cross Gateway Patient Discovery (XCPD).','https://brokeringrespondinggateway- /iti55/&lt;CQ Participant OID&gt;/outbound'))
    find_documents_endpoint                     = models.CharField(verbose_name='Find Documents Endpoint:', blank=True, max_length=400, default='https://brokeringrespondinggateway- /iti38/<CQ Participant OID>/outbound',help_text=get_help_text('URL to Allscripts Brokering Responding Gateway for IHE Transaction ITI-38 Cross Gateway Query.','https://brokeringrespondinggateway- /iti38/&lt;CQ Participant OID&gt;/outbound'))
    retrieve_document_endpoint                  = models.CharField(verbose_name='Retrieve Document Endpoint:', blank=True, max_length=400, default='https://brokeringrespondinggateway- /iti39/<CQ Participant OID>/outbound', help_text=get_help_text('URL to Allscripts Brokering Responding Gateway for IHE Transaction ITI-39 Cross Gateway Retrieve.','https://brokeringrespondinggateway- /iti39/&lt;CQ Participant OID&gt;/outbound'))

    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = "Set Carequality Integration Settings"

class ParticipantListBasedPAAModel(ConfigurationEntityBaseModel):
    page                                        = models.ForeignKey('CarequalityIntegrationSettingsPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    healthcare_institude_name                   = models.CharField(verbose_name='Healthcare Institute Name', blank=True, max_length=400, default='', help_text=('Name of institute. Enter to ease the future management of the table contents. For display only.'))
    patient_assigning_authority_name            = models.CharField(verbose_name='Patient Assigning Authority Name', blank=True, max_length=400, default='', help_text=('Patient Assigning Authority Name as displayed in CCenter under EMPI- Assigning Authority'))
    identifier                                  = models.CharField(verbose_name='Identifier', blank=False, unique=True, max_length=400, default='', help_text=('Patient Assigning Authority OID as displayed in CCenter under EMPI- Assigning Authority.'))
    home_community_id_three_level               = models.CharField(verbose_name='Home Community ID', blank=True, max_length=400, default='', help_text=('Defines the facility\'s Home Community ID (OID) for outbound requests to Carequality.The OID format should be: urn:oid:n.n.n.n.n.n. For example: urn:oid:2.16.840.1.113883.3.57.1.3.0.2. If it is empty, the dbMotion Home Community ID  will be used by default.'))

    def participant_list_url(self):
        if self.id:
            return '<a href="%s" onclick="return showEditPopup(this);" title="Click to edit">Participants</a>' % ("/admin/dbmconfigapp/participantlistbasedpaamodel/%s/" % self.id)
        else:
            return '<a href="%s" onclick="return showEditPopup(this);" >Add Participant</a>' % "/admin/dbmconfigapp/participantlistbasedpaamodel/add/"
    
    participant_list_url.allow_tags = True
    participant_list_url.short_description = 'Participant List'

    def override_add_button_link(self):
        return "/admin/dbmconfigapp/participantlistbasedpaamodel/add/"

    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Settings Per EHR"
        verbose_name = "Settings Per EHR"
        verbose_name_plural = "Settings Per EHR"
        #history_meta_label = verbose_name_plural

class ParticipantListModel(ConfigurationEntityBaseModel):
    institude_name = models.ForeignKey(ParticipantListBasedPAAModel, on_delete=models.CASCADE, default=1)
    paticipant_name = models.CharField(blank=False, max_length=400, verbose_name='Name', default='', help_text='Carequality participant name.')
    paticipant_identifier = models.CharField(blank=False, max_length=400, default='', verbose_name='Identifier', help_text='Carequality participant OID.')
    
    def __unicode__(self):
        return self.paticipant_name
           
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Carequality Participant'
        verbose_name_plural = 'Carequality Participants'
        history_meta_label = verbose_name_plural

class ParticipantBaselineListModel(ConfigurationEntityBaseModel):
    page = models.ForeignKey('CarequalityIntegrationSettingsPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    paticipant_name = models.CharField(blank=False, max_length=400, verbose_name='Name', default='', help_text='Carequality participant name.')
    paticipant_identifier = models.CharField(blank=False, max_length=400, default='', verbose_name='Identifier', help_text='Carequality participant OID.')
    
    def __unicode__(self):
        return self.paticipant_name
           
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Shared Participant'
        verbose_name_plural = 'Shared Participant List'
        history_meta_label = verbose_name_plural

class PrefetchSettingsModel(ConfigurationEntityBaseModel):
    page = models.ForeignKey('CarequalityIntegrationSettingsPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    enable_prefetch = models.BooleanField( verbose_name='Enable Prefetch', default=False, help_text=get_help_text('Determines whether to enable or disable Prefetch functionality.', 'False'))
    api_url = models.CharField(blank=True, max_length=400, verbose_name='Prefetch API cloud service:', default='', help_text=get_help_text('URL for prefetch API cloud service','None'))
    api_subscription_key = encryption.EncryptedCharField(blank=True, max_length=400, verbose_name='Prefetch API subscription:', default='', help_text=get_help_text('Subscription key for prefetch API. The key is issued by the prefetch API Azure manager.','None',add_no_export_note=True))

    class Meta:
        app_label = "dbmconfigapp" 
        verbose_name =  "Prefetch Settings"
        verbose_name_plural = "Prefetch Settings"
        history_meta_label = verbose_name_plural

    



class PVPatientSearchPage(PageBaseModel):
    def page_title(self):
        return "Set Patient Search Settings"
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Set Patient Search Settings"
        
        
class PVClinicalDomainPage(PageBaseModel):
    
    def page_title(self):
        return "Set Clinical domains Settings"
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Set Clinical domains Settings"     

class PVCCDADisplayPage(PageBaseModel):
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "CCDA Display and Data Export"      
        


class PVPatientDisplayPage(PageBaseModel):
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Set the Patient Display Settings"

class PVCategoriesProperties(ConfigurationEntityBaseModel):
    parent                      = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    category_name               = models.CharField(max_length=60,default='External Documents', verbose_name='Category Type')
    display_name                = models.CharField(max_length=75, verbose_name='Category Display Name', null=False, unique=True, help_text = "Defines the name to display for the clinical category in the application. Display name configuration is applicable to Patient View only.")
    hide_fields                 = models.CharField(max_length=500, verbose_name='Hide Fields',blank=True, null=True, help_text = "For the Details pane, specify the metadata fields to hide. Use the format Label1, Label2 ; example, in Problems  enter: \"Status, Source\" to hide these fields on details page of Problems. <br/>For Encounters: Diagnosis, Chief Complaint, Location History and Providers sections can also be hidden, also hides Service, Location and Diagnosis on encounter cards and reports.")
    category_order              = models.IntegerField(null=True, verbose_name='Category Order', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)], help_text = "Defines the order of clinical categories to display in the application. Category order configuration is applicable to Patient View only.")
    expand_by_default           = models.BooleanField(verbose_name='Expand by default', default=False, help_text="Defines if the category should be expanded by default on enter patient file, in view by category. Applicable only to Patient view application.")
    nodes                       = models.CharField(max_length=500,blank=True, null=True, verbose_name='XDS.b Nodes', help_text = "Defines the list of XDS.b and XCA nodes for the dedicated External Documents page, in the following format: nodeID1,nodeID2.<br/>Possible values: Empty, nodeIDs seperated by ','.<br/>When the value is list of nodeID is then only that nodes which are configured in master config file will be queried for external documents list, when the value is Empty no nodes will be queried.<br/>User should not configure same nodes in more than one external document category.<br/>Default: Empty.")
    roles                       = models.CharField(max_length=500, verbose_name='Permitted Roles', default='All', null=True, help_text = "Defines the user roles which has access to view this External Documents category.<br/>Possible values: All, None, Role names separated by ','. <br/>When the value is 'All' all users will have access to view this category. <br/> When certain role(s) are filled, only users having that role(s) will be able to access this category.<br/>When the value is 'None' no user can view/access this category.<br/>Default: All.")
    time_frame                  = models.IntegerField(blank=True, null=True, default=1, verbose_name='Timeframe', validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)], help_text = "Defines the timeframe in years to load data for this External Documents category. If no value or 0 is configured, then entire data is loaded for the category.<br/>Default: 1 Year.")
    information_text            = models.CharField(max_length=500,blank=True, null=True, verbose_name='Information Text', help_text = "Defines the text to show on this External documents category as a tooltip and as information text to explain about the source of the data displayed under this category.")
    
    def category_name_url(self):
        if self.id:
            if self.category_name == 'External Documents':
                return '<a href="%s" onclick="return showEditPopup(this);" title="Click to edit">%s</a>' % ("/admin/dbmconfigapp/pvcategoriesproperties/%s/" % self.id, self.category_name)
            return self.category_name
        else:
            return '<a href="%s" onclick="return showEditPopup(this);" >Add new Application</a>' % "/admin/dbmconfigapp/pvcategoriesproperties/add/"

    category_name_url.allow_tags = True
    category_name_url.short_description = 'Category Type'

    def override_add_button_link(self):
        return "/admin/dbmconfigapp/pvcategoriesproperties/add/"

    def __unicode__(self):
        return self.category_name

    def page_title(self):
        return ''

    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Patient View Categories'
        verbose_name= "External Document Category"
        verbose_name_plural = "Patient View Categories"



class DemographySearchFields(ConfigurationEntityBaseModel):
    pv_parent                   = models.ForeignKey('PVPatientSearchPage', on_delete=models.SET_NULL, null= True, default = 1, editable=False)
    demo_search_field_label     = models.CharField( max_length=120, verbose_name='Label')
    dbm_patient_attribute       = models.ForeignKey(InitiateMappings, verbose_name='DbMotion Patient Attribute Name', on_delete=models.SET_NULL, null=True, default=None, limit_choices_to={'dbmotion_attribute_input': 1} )
    max_chars                   = models.IntegerField(max_length=120, verbose_name='Maximum Characters', validators=[validators.MinValueValidator(1)])

    def __unicode__(self):
        return "%s | %s" %(self.demo_search_field_label, self.dbm_patient_attribute)
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Demographic Search Field"
        history_meta_label = "Demographic Search Fields"


class SearchResultGrid(ConfigurationEntityBaseModel):

    pv_parent               = models.ForeignKey('PVPatientSearchPage', on_delete=models.SET_NULL, null= True, default = 1, editable=False) 
    label                   = models.CharField(max_length=260, unique=True)
    dbMotion_patient_attribute_name     = models.ForeignKey(InitiateMappings, null=True, unique=False, blank=True, limit_choices_to={'dbmotion_attribute_output': True}, on_delete=models.SET_NULL)    
    column_order         = models.IntegerField(null=False, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)])
    default_fields       = models.CharField(max_length=50, null=True)
    
    def __unicode__(self):
        return "%s | %s" %(self.label, self.dbMotion_patient_attribute_name)
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Search Result Field"
        verbose_name= "Search Result field"

class PatientViewDefaultLandingPage(ConfigurationEntityBaseModel):
    patient_view_page = models.ForeignKey(PatientViewPage, on_delete=models.CASCADE, default=1)
    default_page = models.IntegerField(verbose_name='Default landing page', default=0, null=False, choices=Default_landing_page, help_text=get_help_text(
        'Determines the default landing page when a user enters a patient file. This configuration applies to Patient View only. A user can override the configuration and select a different landing page in User Settings > Application Preferences.<br/><i>Default: Patient Summary</i>'))

    class Meta:
        app_label = "dbmconfigapp"

class ImagingPacsDisclaimer(ConfigurationEntityBaseModel):

    pv_parent = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null= True, default=1, editable=False) 
    Pacs_Disclaimer_Text      = models.CharField(max_length=500, verbose_name='PACS Disclaimer Text', blank=True, null=True, help_text=get_help_text('This configuration determines the text to display as disclaimer on PACS images. When it has some text we display a disclaimer, when it is empty the disclaimer wont be showed. <br/><i>Default: empty</i>'))
    Grouping_by_Modality     = models.BooleanField(verbose_name='Imaging Grouping by Modality', default=False, help_text=get_help_text('This configuration enables grouping of (UMS: Image study.typecode) designations received with imaging study type. All studies that are received with the same type code designations are grouped together. If the configuration is set to false, grouping of imaging results is by sub domain designation of imaging study  (UMS: Imaging Study code). <br><i> Default: False.</i>'))

    def __unicode__(self):
        return ""
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Imaging"

class SpecializedViews(ConfigurationEntityBaseModel):
    patient_view_page         = models.ForeignKey(PatientViewPage, on_delete=models.CASCADE, default=1)
    view_name                 = models.CharField(max_length=50, unique=True, null=False, blank=False, help_text=get_help_text('Defines the name of specialized view and allows to type alpha numeric text. Mandatory field to fill to create a view, default: Empty'))
    domain_codes_file_name    = models.FileField(default='', null=False, blank=False, upload_to='PatientView/SpecializedViews', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Domains and Codes file', help_text=get_help_text('The CSV file Defines the category type and codes (Code & Code system) to display under the specialized view. Category type should match with the defined category types in dbMotion. Mandatory field to fill, default: Empty'))
    roles                     = models.CharField(max_length=500, verbose_name='Permitted Roles', default='None', null=False, help_text = get_help_text("Defines the user roles which has access to view this specialized view.<br/>Possible values: All, None, Role names separated by ','. <br/>When the value is 'All' all users will have access to view this category. <br/> When certain role(s) are filled, only users having that role(s) will be able to access this category.<br/>When the value is 'None' no user can view/access this category.<br/>Default: None."))

    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Specialized view"

class PatientsListViews(ConfigurationEntityBaseModel):
    patient_view_page         = models.ForeignKey(PatientViewPage, on_delete=models.CASCADE, default=1)
    patients_list_type        = models.CharField(max_length=75, verbose_name='Patients List Type', null=False, blank=False)
    patients_list_label       = models.CharField(max_length=75, verbose_name='Label', unique=True, null=False, blank=False, help_text=get_help_text('Defined label is displayed to all users with page access. Default is page name.'))
    patients_list_order       = models.IntegerField(null=False, verbose_name='Order', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)], help_text=get_help_text('The order of pages are displayed.'))
    patients_list_roles       = models.CharField(max_length=500, verbose_name='User Roles', default='None', blank=False, null=False, help_text = get_help_text("Defines the user roles which has access to view this Page. Possible Values: All, None, Role names separated by ','. When the values is 'All' all users will have access to view this page. When certain role(s) are filled, only users having that role(s) will be able to access this page. Default is None , which means no user can access this page"))
    patients_relation_type    = models.CharField(max_length=75, verbose_name='Relationship Type', null=True, blank=True)

    def __unicode__(self):
        return self.patients_list_label
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "\"My Patient\" List"



