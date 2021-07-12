from django.db import models
from dbmconfigapp.models.base import ConfigurationEntityBaseModel, get_help_text, PageBaseModel
from dbmconfigapp.models.fields import SelectMultipleChoicesField
from django.utils.html import mark_safe
from django.urls import reverse
from dbmconfigapp.utils import encryption
from django.contrib.auth.hashers import make_password

_DEPLOYMENT_TYPE_CHOICES = (
    ('Citrix', 'EHR Agent on Desktop and EHR hosted on Citrix'),
    ('Local', 'Desktop EHR, with Both EHR Agent and EHR on Desktop / Both EHR Agent and EHR hosted on Citrix'),
    ('Web', 'Web EHR, with Both EHR Agent and EHR on Desktop / Both EHR Agent and EHR hosted on Citrix'),
    )

_CORNER_CHOICES = (
    ('LeftTop', 'Left Top'),
    ('RightTop', 'Right Top'),
    ('LeftBottom', 'Left Bottom'),
    ('RightBottom', 'Right Bottom'),
    )

_CONTEXT_TYPE_CHOICES = (
    ('CcowParticipant', 'CCOW - EHR Agent plays Participant role (Context Manager available)'),
    ('CcowReceiver', 'CCOW - EHR Agent plays Context Manager role (Context Manager light)'),
    ('NonCcow', 'Non CCOW - Custom context interceptor'),
    )

_USER_CONTEXT_TYPE_CHOICES =(
    ('Managed', 'Managed'),
    ('UnmanagedCredentials', 'Unmanaged credentials'),
    ('UnmanagedSAML', 'Unmanaged SAML'),
    ('SendToMyEHR', 'User for "Send to my EHR"'),
    )


_CATEGORIES_FOR_SEND_LIST = [
        'Encounters',
        'ProblemList',
        'Diagnoses',
        'Allergies',
        'Medications',
        'Laboratory',
        'Immunizations',
        'Procedures',
        'ClinicalDocuments',
        'PastMedicalHistory',
                            ]

ACT_TYPES_LIST = [
        'AllergyIntolerance',
        'ClinicalDocument',
        'ClinicalImageStudyRequest',
        'ClinicalImageStudy',
        'Diagnosis',
        'Encounter',
        'Immunization',
        'LabEvent',
        'LabRequest',
        'LabResult',
        'MeasurementEvent',
        'Medication',
        'Problem',
        'Procedure',
        'PathologyEvent',
        'PathologyResult'
                  ]

ACT_TYPES_FOR_DELTA_BY_ORDER_FACILITY_LIST = (
        ('ClinicalDocument','Clinical Document'),
        ('ClinicalImageStudy','Clinical Image Study'),
        ('LabEvent','Lab Event'),
        ('PathologyEvent', 'Pathology Event')
        )
                  
NON_CCOW_PLUGIN_TYPE = (
        ('Custom','Custom'),
        ('ContextProviderServiceInterceptor.ContextProviderServiceInterceptor, dbMotion.SmartAgent.ContextProviderServiceInterceptor','UI Automation')
        )

REPORTING_TYPE_CHOICES = (
        ('SCM','SCM'),
        ('TW','TW'),
        )

class ExternalAppsBaseModel(object):
    def page_title(self):
        return 'Set the %s Settings' % self._meta.verbose_name

class EHR(ConfigurationEntityBaseModel, ExternalAppsBaseModel):
    name                = models.CharField(max_length=100, unique=True, help_text= 'Defines the name of the EHR')
    deployment_type     = models.CharField(max_length=100, choices=_DEPLOYMENT_TYPE_CHOICES, default='Local', help_text= """
        The EHR application can be either a desktop application or a Web-based application.<br/>
        The Deployment type applies to both the EHR Agent and the EHR and can be one of the following: Desktop deployment or a desktop virtualization deployment, such as hosted on Citrix.<br/>
        The Deployment Type configurations depend on both the EHR application type and the EHR Agent/EHR deployment.<br/>
        For example, detecting when a Citrix-based EHR has been launched is difficult because it is hosted in a Citrix process and there can be multiple Citrix processes running simultaneously, each hosting a different application.<br/>
        The following Deployment type options are available:<br/>
        - EHR Agent on Desktop and EHR hosted on Citrix: The EHR is either a desktop or Web application. The EHR Agent is deployed on the desktop and the EHR is hosted on Citrix. <br/>
        - Desktop EHR, with Both EHR Agent and EHR on Desktop/Both EHR Agent and EHR hosted on Citrix: The EHR is a desktop application. And both the EHR Agent and the EHR are deployed on the local desktop. Or, both the EHR Agent and the EHR are hosted on Citrix.<br/>
        - Web EHR, with Both EHR Agent and EHR on Desktop/Both EHR Agent and EHR hosted on Citrix: The EHR is a Web application. And both the EHR Agent and the EHR are deployed on the local desktop. Or, both the EHR Agent and the EHR are hosted on Citrix.<br/>
        """)
    detection_exe       = models.CharField(verbose_name='Executable', max_length=260, null=True, blank=True, help_text='Defines the EHR executable application file name.<br/>The value is a regular expression. For more information about regular expression refer to <a href="https://msdn.microsoft.com/en-us/library/az24scfc(v=vs.110).aspx">MSDN Regular Expression Language guide</a>.')
    detection_url       = models.CharField(verbose_name='URL', max_length=260, null=True, blank=True, help_text="Defines the EHR's Url")
    detection_title     = models.CharField(verbose_name='EHR Window Title', max_length=200, null=True, blank=True, help_text= get_help_text('This parameter is used to detect the window label of an EHR in order to anchor the EHR Agent to the window that matches this title.<br/>This configuration is important in scenarios when "Follow Focused Window" is checked. In this case, and if the title is empty, the EHR Agent will anchor itself to every new window and every dialog box belonging to the EHR.<br/>The value is a regular expression. For more information about regular expression refer to <a href="https://msdn.microsoft.com/en-us/library/az24scfc(v=vs.110).aspx">MSDN Regular Expression Language guide</a>.', 'Empty'))
    detection_launch_title = models.CharField(verbose_name='EHR Detection Title', max_length=200, null=True, blank=True, help_text= 'Defines the Title of the EHR application, which is used to enable the system to detect this EHR by its title. If the Title is undefined, the EHR will be detected only by its Executable Application file name.<br/>The value functions as a regular expression. For more information about regular expression refer to <a href="https://msdn.microsoft.com/en-us/library/az24scfc(v=vs.110).aspx">MSDN Regular Expression Language guide</a>.<br/><b>Note:</b> EHR Agent will ignore this value on Share Desktop mode.')    
    detection_window_class = models.CharField(verbose_name='EHR Window Class', max_length=200, null=True, blank=True, help_text= get_help_text('This parameter is used to detect the window class of an EHR in order to identify that the running application is the desired EHR.<br/>This configuration is important in scenarios when there may be multiple windows which are otherwise indistinguishable.<br/>The value is a regular expression. For more information about regular expression refer to <a href="https://msdn.microsoft.com/en-us/library/az24scfc(v=vs.110).aspx">MSDN Regular Expression Language guide</a>.', 'Empty'))
    detection_follow_focused_window = models.BooleanField(verbose_name='Follow focused window', default=False, help_text= get_help_text('Determines to which EHR window the EHR Agent will be anchored.<br/>True: If the target EHR has several windows, the EHR Agent will anchor to the EHR\'s focused window.<br/>False: The EHR Agent will anchor to the EHR\'s first window.','False'))
    prevent_detected_window_topmost = models.BooleanField(verbose_name='Prevent detected window reposition to topmost window', default=False, help_text= get_help_text('This option supports the following case:<br/>1.The EHR has multiple windows.<br/> 2. The focused window must be generally followed by the Agent.<br/> 3. There is a window in focus, which should not be detected by the Agent at the moment, according to other configuration settings. <br/> 4. Another EHR window, which is currently detected by the Agent, should not be automatically repositioned to be the topmost window, so that it does not block the focused window. ', 'False'))
    detection_version   = models.CharField(verbose_name='Version', max_length=40, null=True, blank=True, help_text='Defines the EHR product version as defined in the executable application.')
    position_app_corner = models.CharField(verbose_name='App corner', max_length=20, choices=_CORNER_CHOICES, default=_CORNER_CHOICES[1][0], help_text= '<i>Default: '+_CORNER_CHOICES[1][1]+'</i>')
    position_agent_corner = models.CharField(verbose_name='Agent corner', max_length=20, choices=_CORNER_CHOICES, default=_CORNER_CHOICES[1][0], help_text= '<i>Default: '+_CORNER_CHOICES[1][1]+'</i>')
    position_offset_x   = models.IntegerField(verbose_name='Offset X', default=0, help_text= '<i>Default: 0</i>')
    position_offset_y   = models.IntegerField(verbose_name='Offset Y', default=40, help_text= '<i>Default: 40</i>')
    
    def instances(self):
        text = '%d Instances' % len(Instance.objects.filter(ehr=self))
        html = '<a href="%s">%s</a>' % ('/admin/externalapps/instance/?ehr__id__exact=%d' % self.pk, text)
        return html
    
    instances.allow_tags = True
    
    
    def deploy_type_display(self):
        from dbmconfigapp.admin.dbm_ModelAdmin import get_choice_value
        return get_choice_value(_DEPLOYMENT_TYPE_CHOICES, self.deployment_type) 
    
    deploy_type_display.short_description = 'Deployment type'
    
    
    def __unicode__(self):
        return self.name
           
    class Meta:
        app_label = "externalapps"
        verbose_name = 'EHR'
        


class AppId(ConfigurationEntityBaseModel):
    app_id                  = models.CharField(verbose_name='Client application ID', max_length=200, unique=True, help_text='The EHR Application ID is the unique identifier of each EHR.<br/>It is required for registering the EHR in the VPO configurations to perform Send to My EHR.<br/>This value should be aligned with the "Application instance name" in the "VPO Data Export" configuration.')
    categories_available_for_send   = SelectMultipleChoicesField(verbose_name='Categories available for send', default='All', choices=_CATEGORIES_FOR_SEND_LIST, null=True, blank=True, help_text=get_help_text("""
            Defines the clinical categories that support Send to my EHR. For each defined category, the EHR Agent checkbox is enabled so that it can be selected for the Send to EHR functionality. The checkbox is disabled for categories that do not support Send to EHR and for categories not defined in this field.<br/>
            The Data Integration engineer must determine all act types that can be sent from this data source. <br/>
            Possible values are 'All' or one or more of the following, in a comma-separated list:<br/>
            <b>""" + ', '.join(_CATEGORIES_FOR_SEND_LIST) + """</b><br/>
            If the list is empty, all categories are disabled.
             """, 'All'))
    extra_help = 'This configuration enables you to define the message text that appears for a successful and an unsuccessful Send to EHR operation that was completed.'
    send_to_my_EHR_success_message = models.CharField(verbose_name='Send to my EHR success message' ,max_length=200, null=True, blank=True, help_text=get_help_text('If field is empty, the product default message will be used.', 'Empty'))
    send_to_my_EHR_failure_message = models.CharField(verbose_name='Send to my EHR failure message' ,max_length=200, null=True, blank=True, help_text=get_help_text('If field is empty, the product default message will be used.', 'Empty') + '<br/><br/>' + extra_help)
    send_to_my_EHR_ccda_only   = models.BooleanField(verbose_name='Send Only structured CCDA Documents', default=False,help_text=get_help_text('Determines whether \"Send to My EHR\" will enable to send only documents that arrived to dbMotion as structured CCD/A, or any other media type, such as unstructured CCD/A, TIFF, PDF, etc.<br>True: Will support structured CCD/A only.<br>False: Will support sending any document type.<br><br>Note: The checkbox is enabled if "All" or "ClinicalDocuments" were chosen above.', 'False'))
    
    def description(self):
        output = ['<span id="%s_%d"><br/>' % (self._meta.object_name.lower(), self.pk)]
        for fld in self._meta.fields:
            if not fld.name in ['id', 'app_id']:
                output.append('<div><b>%s:</b> %s</div>' % (fld.verbose_name, self.serializable_value(fld.name)))

        # Build HTML for Delta View Source
        output.append('<br/><div class="tabular inline-relatedx"><fieldset class"module"><h2>%ss</h2>' % SourceSystem._meta.verbose_name)
        inlines = SourceSystem.objects.filter(app_id=self)
        from .admin import SourceSystemInline
        if inlines:
            output.append('<table><thead><tr>')
            for f in SourceSystemInline.fields:
                output.append('<th>%s</th>' % SourceSystem._meta.get_field(f).verbose_name.capitalize())
            output.append('</tr></thead><tbody>')
            for s in inlines.all():
                output.append('<tr>')
                for f in SourceSystemInline.fields:
                    output.append('<td>%s</td>' % s.serializable_value(f))
                output.append('</tr>')    
                
            output.append('</tbody></table>')
        else:
            output.append('No Source Systems defined.')
        
        output.append('</fieldset></div>') 

        
        # Build HTML for Delta View Ordering Facility
        output.append('<br/><div class="tabular inline-related"><fieldset class"module"><h2>%ss</h2>' % OrderingFacilities._meta.verbose_name)
        inlines = OrderingFacilities.objects.filter(app_id=self)
        from .admin import OrderingFacilitiesInline
        if inlines:
            output.append('<table><thead><tr>')
            for f in OrderingFacilitiesInline.fields:
                output.append('<th>%s</th>' % OrderingFacilities._meta.get_field(f).verbose_name.capitalize())
            output.append('</tr></thead><tbody>')
            for s in inlines.all():
                output.append('<tr>')
                for f in OrderingFacilitiesInline.fields:
                    output.append('<td>%s</td>' % s.serializable_value(f))
                output.append('</tr>')    
                
            output.append('</tbody></table>')
        else:
            output.append('No Ordering Facilities defined.')
        
        output.append('</fieldset></div>') 


        output.append('</span>')
        return mark_safe(''.join(output))
    
    description.allow_tags = True
    
    def __unicode__(self):
        return self.app_id

    class Meta:
        verbose_name = 'Application ID'
        history_meta_label = verbose_name
        app_label = "externalapps"

class InstanceProperties(ConfigurationEntityBaseModel, ExternalAppsBaseModel):
    name                    = models.CharField(max_length=100, unique=True)
    app_id                  = models.ForeignKey(AppId, on_delete=models.SET_NULL, null=True)
    ehr_user_assign_auth    = models.CharField(verbose_name='EHR User Assigning Authority', max_length=400, null=True, blank=True,help_text=get_help_text('Define the root ID of the EHR user to enable a hosted application user to login automatically to the application after logging into the EHR.', 'Empty.'))
    patient_assigning_Authority_for_Display  = models.CharField(verbose_name='Patient Assigning Authority for Display', max_length=400, null=True, blank=True,help_text=get_help_text("""When Patient View is launched using Launch API, clients specify the source system from which the patient medical record number (MRN) is taken as leading. The MRN and demographics are displayed in the patient banner and reports. Multiple values should be divided by "|" as separator.<br/>
			   Values include:<br/>
               - FIRST_FROM_VIA :First index from VIA response is selected as leading.<br/>
			   - OID :Multiple OIDs with "FIRST_FROM_VIA" can be added. Display priority is based on the left-to-right order of entry. Example - 1.01.01.01.0 | FIRST_FROM_VIA<br/>
               - Empty (default) :Demographics from searched MRN is displayed.<br/>
			     <b>Note:</b> When single OID or multiple are configured and the index is not found in VIA response according to configuration , application will continue to display (default) searched MRN as leading index to show demographics."""))
    
    def app_id_description(self):
        output = ['<div id="app_id_description">']
        for app in AppId.objects.all():
            output.append(app.description())
        output.append('</div>')
        return mark_safe(''.join(output))
    
    app_id_description.allow_tags = True
        
    def user_contexts(self):
        return '%d User Contexts' % len(UserContext.objects.filter(instance_properties=self))
    
    def patient_contexts(self):
        return '%d Patient Contexts' % len(PatientContext.objects.filter(instance_properties=self))
    
    def instances(self):
        inst_count = len(Instance.objects.filter(instance_properties=self))
        text = '%d Instances' % inst_count
        if inst_count == 0: return text
        html = '<a href="%s" title="See all instances connected to %s">%s</a>' % ('/admin/externalapps/instance/?instance_properties__id__exact=%s' % self.pk, self.name, text)
        return html
    
    instances.allow_tags = True
    
    def __unicode__(self):
        return self.name
    
    def description(self):
        lines = []
        for m in [SourceSystem, UserContext, PatientContext]:
            qs = m.objects.filter(instance_properties=self)
            lines.append('%s: %s' % (m._meta.verbose_name_plural.capitalize(), 'No ' + m._meta.verbose_name_plural.capitalize() if not qs else ', '.join([s.__unicode__() for s in qs])))
        html = """
            <div class="description">
            <p>""" + self.name + """</p>
            <p>""" + '<br/>'.join(lines) + """</p>
            </div>
        """
        return html
    
    class Meta:
        verbose_name = 'Properties Package'
        history_meta_label = verbose_name
        app_label = "externalapps"
        
        
class Instance(ConfigurationEntityBaseModel, ExternalAppsBaseModel):
    ehr                 = models.ForeignKey(EHR, verbose_name='EHR', on_delete=models.CASCADE, help_text='Select the EHR for which you want to create an instance.') 
    endpoints_page      = models.ForeignKey('DirectAddressEndpointsPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    instance_properties = models.ForeignKey(InstanceProperties, on_delete=models.CASCADE, verbose_name='Properties Package', help_text='Configure the properties for each EHR Instance by doing one of the following:<br/>- Select one of the Properties Packages from the dropdown list to reuse a set of predefined properties for this instance.<br/>- Click the plus sign to open a dialog box where you can configure a new Properties Package for this instance which can later be reused.')
    name                = models.CharField(max_length=100, unique=True, help_text=get_help_text('Defines the EHR instance name.'))
    is_enabled          = models.BooleanField(default=True, help_text=get_help_text('Determines if the current instance is enabled.'))
    env_variable_name   = models.CharField(verbose_name='Environment variable name', max_length=100, null=True, blank=True)
    env_variable_value  = models.CharField(verbose_name='Environment variable value', max_length=100, null=True, blank=True, help_text=get_help_text('Defines various environment variables.<br/>If the properties based on the executable application are not enough to differentiate two different EHR Agent scenarios, the environment variables are used. In this case, a different environment variable will be set on the client computers working in different scenarios.<br/>Then, the System Engineer should set the name and the value of the variable.'))
    direct_address      = models.EmailField(verbose_name='Direct Address', max_length=100, null=True, blank=True, help_text=get_help_text('Defines Direct Address associated to the EHR instance.<br/>When users send Direct messages from ClinicalView Agent, this address will be the user\'s sending address.<br/>Example: Facility.name@location.direct.com', 'Empty'))
    direct_address_suffix = models.CharField(verbose_name='Direct Address Suffix', max_length=50, null=True, blank=True, help_text=get_help_text("""
        Define suffix for a group of direct addresses.<br/> 
        Should only use in case the EHR using privates direct addresses for his providers and routed the direct messages also to dbMotion<br/>
        Example: @location.direct.com
        """, 'Empty'))
    mu_reporting_endpoint = models.CharField(verbose_name='Meaningful Use Reporting Endpoint', help_text=get_help_text('Defines the endpoint URL used to report Sending/Receiving of CCDA documents over Direct. ', 'Empty'), blank=True, null=True, max_length=500, default='')
    mu_reporting_source_system_name = models.CharField(verbose_name='Source System Name', blank=True, null=True, max_length=200, default='', help_text=get_help_text("""
        Define the source system name as exist in the CDR common.device.devicename.<br/>
        <b>Note:</b> This field should be configured <b>only</b> if two or more EHR instances using the same OID in "Assigning Authority for display" and the reporting process should find only the relevant patient for the EHR instance.
        """, 'Empty'))
    mu_reporting_type   = models.CharField(verbose_name='Reporting Interface', max_length=50, null=True, blank=True, choices=REPORTING_TYPE_CHOICES, help_text=get_help_text("""
        Defines the interface used to report Sending/Receiving of CCDA documents over Direct.<br/>
        <b>Note:</b> This field is mandatory if an endpoint is configured.<br/>
        SCM: SCM interface (reporting to CPM).<br/>
        TW: TW interface (reporting to AAP).
        """, "Empty"))
    mu_reporting_login = models.CharField(verbose_name='Unity Service User', blank=True, null=True, max_length=100, default='', help_text=get_help_text("""
        Define the Unity service user that will be used when reporting to TW.<br/>
        Unity service user should be configured for the relevant TW environment: TEST / PROD.<br/>
        <b>Note:</b> This field is mandatory when TW is the reporting interface.
        """, 'Empty'))
    mu_reporting_password = encryption.EncryptedCharField(verbose_name='Unity Service Password', blank=True, null=True, max_length=100, default='', help_text=get_help_text("""
        Define the Unity service Password that will be used when reporting to TW.<br/>
        Unity service Password should be configured for the relevant TW environment: TEST / PROD.<br/>
        <b>Note:</b> This field is mandatory when TW is the reporting interface. 
        """, 'Empty'))
    mu_reporting_app_name = models.CharField(verbose_name='Application Name', blank=True, null=True, max_length=200, default='', help_text=get_help_text("""
        Define dbMotion application name as configured in Unity.
        Application name should be configured for the relevant TW environment: TEST / PROD.
        <b>Note:</b> This field is mandatory when TW is the reporting interface.
        """, 'Empty'))
    mu_reporting_community_oid = models.CharField(verbose_name='Community OID', blank=True, null=True, max_length=200, default='', help_text=get_help_text("""
        Define TW Community OID as configured in TW, for the dbMotion - TW integration.<br/> 
        The value should be provided from TW resource.<br/>
        <b>Note:</b> This field is mandatory when TW is the reporting interface.
        """, 'Empty'))
    thumbprint =       models.CharField(verbose_name='Certificate Thumbprint',max_length=100, blank=True, null=True, default=None, help_text=get_help_text("""
        Defines thumbprint of the certificate for the configured endpoint in the field: Meaningful Use Reporting Endpoint.<br/>
        <b>Note:</b> This field is mandatory if an endpoint is configured and SCM is the reporting interface. 
        """, "Empty"))
    ccow_item_name      = models.CharField(verbose_name='CCOW Parameter for EHR Instance Identification', max_length=100, null=True, blank=True, help_text=get_help_text('Defines a CCOW parameter with an added suffix (for example,  the syntax will be Patient.Id.Mrn.Suffix) that is used to identify an EHR instance.<br/><br/><b>Configure this parameter when there is a need to differentiate between EHR instances, when</b> all instances have the same values for the following parameters (meaning that the system cannot differentiate between them):<br/>- Same EHR (Application)<br/>- URL (for Web application)<br/>- Executable file name (for Desktop application)<br/>- Application Title<br/>- Application Version<br/>- Environment Variable (or cannot create it)<br/>- Context Type<br/>- Participant Name<br/>- Passcode<br/>- Same Supported profiles<br/><br/>This configuration provides an additional method for organizations to differentiate between the instances of the same EHR. When the instance is identified, the relevant product functionality will apply per instance, as usual.<br/><br/>- Delta View can be configured per instance<br/>- Unique Patient Assigning Authority can be configured per instance<br/>- Send to My EHR endpoint can be configured per instance<br/><br/>For the implementation of this functionality, the following conditions apply:<br/>- It applies only with context interception using CCOW.<br/>- Each EHR instance is configured with a separate Properties Package.<br/><br/><b>Limitation:</b><br/>This configuration is ignored for an Instance with a Property Package that has more than one configured Patient Assigning Authority.'))
    context_type        = models.CharField(max_length=20, choices=_CONTEXT_TYPE_CHOICES, default=_CONTEXT_TYPE_CHOICES[0][0])
    interceptor_type    = models.TextField(verbose_name='Plugin type name', null=True, blank=True, help_text='Full namespace and assembly name are required in Non-CCOW scenario.')
    is_user_mapping_enabled   = models.BooleanField(verbose_name='Enable user mapping', default=False,help_text='User mapping is needed when the user context must be obtained from the EHR display, and the user`s display name is not identical to the username in the Active Directory.')
    user_mapping_file_path    = models.TextField(verbose_name='Mapping file path', null=True, blank=True,help_text=get_help_text("""Enter the mapping file's full path including the file extension, such as \\MachineName\\FolderName\\UserMapping.xml.<br>The file path must be accessible from the application servers."""))
    user_mapping_is_use_as_role = models.BooleanField(verbose_name='Map user as a role', default=False,help_text='If selected, the user context will not be resolved by name. The role of the user will be used by the Agent Hub to determine the correct permissions for hosted applications.')
    user_mapping_is_default_to_loggedInUser = models.BooleanField(verbose_name='Use logged-in user by default', default=False, help_text='If the displayed user is listed multiple times in the mapping file, use the logged-in user by default.')
    exclude_dash_from_mrn = models.BooleanField(verbose_name='Exclude dash character from MRN', default=True, help_text=get_help_text('Defines whether EHR Agent will exclude dash character from the MRN, which recieved in the CCOW context.<br/>NOTE: This funcionality is availible only when Agent Hub is CCOW Participant or CCOW Context Manager.<br/>By default, this functionality is enabled.', 'True'))
    blink_only_first_doa = models.BooleanField(verbose_name='Display Badging only on first day of admission', default=False, help_text=get_help_text('Defines whether EHR Agent will display the Badging only during the patient\'s first day of admission.<br/>By default, this functionality is disabled. This means that by default the EHR Agent will display the Badging in all cases where there is a delta in the configured attention time frame.', 'False'))
    supported_profiles   = models.CharField(verbose_name='Supported profiles', max_length=400, null=True, blank=True,help_text=get_help_text("""Defines a comma-separated list of Profiles that can use this EHR instance. If empty, all profiles can use it.<br/> 
                                                                                                                                             The Profile defines various installation attributes that determine how Agent Hub will be installed on the client machine.<br/>
                                                                                                                                             Each Profile has a unique sub-folder under: \\\Web App Server\EHRAgentSetup\.<br/>
                                                                                                                                             For example: Default Profile, CCOW, CCOW Shared Desktop.""", 'Empty'))
    facility_root        = models.CharField(verbose_name='Facility ID root', max_length=400, null=True, blank=True,help_text=get_help_text('Defines the root Identifier of the facility, according to [dbmVCDRData].[Common].[Organization].[Id_Root] .'))
    facility_extension   = models.CharField(verbose_name='Facility ID extension', max_length=400, null=True, blank=True,help_text=get_help_text("""Defines the extension Identifier of the facility, according to [dbmVCDRData].[Common].[Organization].[Id_Extension].<br/><br/>
                                                                                                                                                The active EHR instance facility is identified by the unique features of the EHR instance.<br/>
                                                                                                                                                To distinguish between EHR instances associated with different facilities, configure one of the following:<br/>
                                                                                                                                                &nbsp;&nbsp;- If the EHR instance has a unique EXE file name , Window title, or URL per facility, configure only the Facility ID Root and Extension fields.<br/>
                                                                                                                                                &nbsp;&nbsp;- If the EHR instance EXE file name and Window title is not unique per facility, configure each EHR instance with the relevant environment variable name and value, as well as the Facility ID Root and Extension fields.<br/>
                                                                                                                                                """))
    ofek_url             = models.CharField(verbose_name='Ofek Url', max_length=400, null=True, blank=True,help_text=get_help_text('Defines the ofek url.'))
    uiAutomation_config_file_path    = models.TextField(verbose_name='UI Automation configuration file path', null=True, blank=True,help_text=get_help_text("""Enter the UI Automation configuration files full path including the file extension."""))
    nonCcowPluginType        = models.CharField(max_length=500, verbose_name='Non CCOW plugin type', choices=NON_CCOW_PLUGIN_TYPE, default=NON_CCOW_PLUGIN_TYPE[0][1])
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.instance_properties)

    def admin_change_url(self):
        return reverse('admin:externalapps_instance_change', args=(self.id,))

    def name_as_link(self):
        return '<a href="{link}">{name}</a>'.format(name=self.name, link=self.admin_change_url())

    name_as_link.allow_tags = True
    name_as_link.short_description = "EHR Instance"

    def set_password(self, raw_password):
        self.mu_reporting_password = make_password(raw_password)
           
    class Meta:
        app_label = "externalapps"
        verbose_name = 'EHR Instance'
        history_meta_label = verbose_name
        help_text = """
        These configurations are used to do one of the following:
        <ul>
        <li>Create a new instance of an EHR. Each EHR (for example, Pro) might have various instances installed in different hospital departments or clinics. The properties might be different for each EHR instance and must be configured separately for each.</li>
        <li>Edit properties of an existing EHR instance.</li>
        <li>Delete an EHR instance.</li>
        </ul>
        """

class DirectAddressEndpointsPage(PageBaseModel):
    class Meta:
        app_label = "externalapps"
        verbose_name = "Meaningful Use Reporting Endpoints"
        history_meta_label = verbose_name
        help_text = get_help_text("This table consolidates all configurations of Direct adresses and Reporting endpoints in one place. The configuraiton can be done in this page, and in each EHR Instance page. Each EHR Instance should have a unique Direct Adress. When relevent, configure the end point URL to send the numerator data for this EHR Instance to external reporting systems.", 'Empty')

class Participant(ConfigurationEntityBaseModel, ExternalAppsBaseModel):
    instance            = models.ForeignKey('Instance', on_delete=models.CASCADE)
    type                = models.CharField(max_length=20, default='', null=True, blank=True)
    name                = models.CharField(max_length=100, help_text=get_help_text('Identifies the participant in the Context Manager.', is_tooltip=True))
    ccow_passcode       = models.TextField(verbose_name='CCOW passcode', help_text=get_help_text('CCOW Passcode is used for a secured registration to the Context Manager.', is_tooltip=True))
    is_shared           = models.BooleanField(default=False, help_text=get_help_text('This value is used to specify if participant is shared. If true, this participant can be associated with several instances of the same EHR. Note: Is Shared functionality works only for non Web EHRs', is_tooltip=True))
    
    def __unicode__(self):
        return self.name
           
    class Meta:
        app_label = "externalapps"
        
                
class SourceSystem(ConfigurationEntityBaseModel, ExternalAppsBaseModel):
    instance_properties = models.ForeignKey(InstanceProperties, on_delete=models.SET_NULL, null=True)
    app_id              = models.ForeignKey(AppId, on_delete=models.SET_NULL, null=True)
    name                = models.CharField(max_length=100)
    act_types           = SelectMultipleChoicesField(default='All', choices=ACT_TYPES_LIST, help_text=get_help_text("""Defines the types of clinical acts that can be sent from this dataSource to the main EHR.
The Data Integration engineer must determine all act types that can be sent from this data source. If all supported dbMotion act types can be sent, this attribute does not have to be defined.
If the data source can send only specific act types, these must be defined in this attribute.""", is_tooltip=True))
    
    def __unicode__(self):
        return self.name
           
    class Meta:
        app_label = "externalapps"
        unique_together = ("name", "app_id")
        verbose_name = 'Delta View Source System'
        

class OrderingFacilities(ConfigurationEntityBaseModel, ExternalAppsBaseModel):
    instance_properties = models.ForeignKey(InstanceProperties, on_delete=models.SET_NULL, null=True)
    app_id              = models.ForeignKey(AppId, on_delete=models.SET_NULL, null=True)
    act_type           = models.CharField(verbose_name='Act Type', choices=ACT_TYPES_FOR_DELTA_BY_ORDER_FACILITY_LIST,  max_length=50, help_text=get_help_text("""Possible values are: LabEvent, PathologyEvent, ClinicalImageStudy, ClinicalDocument""", is_tooltip=True))
    facility_root                = models.CharField(verbose_name='Ordering Facility ID Root', max_length=100, null=True)
    facility_extension                = models.CharField(verbose_name='Ordering Facility ID Extension', max_length=100, null=True)
    
    class Meta:
        app_label = "externalapps"
        #unique_together = ("name", "app_id")
        verbose_name = 'Delta View By Ordering Facilitie'


class UserContext(ConfigurationEntityBaseModel, ExternalAppsBaseModel):
    instance_properties     = models.ForeignKey(InstanceProperties, on_delete=models.CASCADE)
    user_context_type       = models.CharField(max_length=100, default=_USER_CONTEXT_TYPE_CHOICES[0][0], choices=_USER_CONTEXT_TYPE_CHOICES)
    ad_domain               = models.CharField(verbose_name='AD Domain', max_length=100, null=True, blank=True, help_text=get_help_text('Defines the active directory domain'))
    suffixes                = models.CharField(verbose_name='suffix', max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return self.user_context_type
           
    class Meta:
        app_label = "externalapps"
        verbose_name = "User Context"
        

class PatientContext(ConfigurationEntityBaseModel, ExternalAppsBaseModel):
    instance_properties         = models.ForeignKey(InstanceProperties, on_delete=models.CASCADE)
    patient_assign_auth_resolve = models.CharField(verbose_name='Patient Assigning Authority for resolve', max_length=400)
    patient_assign_auth_display = models.CharField(verbose_name='Patient Assigning Authority for display', max_length=400, null=True, blank=True)
    suffix_type                 = models.CharField(max_length=20, choices=(('MRN', 'MRN'), ('MPIID', 'MPIID')), default='MRN')
    suffixes                = models.CharField(verbose_name='suffix', max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return self.patient_assign_auth_resolve
    
    class Meta:
        app_label = "externalapps"
        verbose_name = "Patient Context"
        
        
        
        