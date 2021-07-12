# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import externalapps.models
import externalapps.models_installation_profiles
import dbmconfigapp.models.fields
import dbmconfigapp.utils.encryption


class Migration(migrations.Migration):

    dependencies = [
        ('dbmconfigapp', '2120002_initial2'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_id', models.CharField(help_text=b'The EHR Application ID is the unique identifier of each EHR.<br/>It is required for registering the EHR in the VPO configurations to perform Send to My EHR.<br/>This value should be aligned with the "Application instance name" in the "VPO Data Export" configuration.', unique=True, max_length=200, verbose_name=b'Client application ID')),
                ('categories_available_for_send', dbmconfigapp.models.fields.SelectMultipleChoicesField(default=b'All', max_length=400, blank=True, help_text=b"\n            Defines the clinical categories that support Send to my EHR. For each defined category, the EHR Agent checkbox is enabled so that it can be selected for the Send to EHR functionality. The checkbox is disabled for categories that do not support Send to EHR and for categories not defined in this field.<br/>\n            The Data Integration engineer must determine all act types that can be sent from this data source. <br/>\n            Possible values are 'All' or one or more of the following, in a comma-separated list:<br/>\n            <b>Encounters, ProblemList, Diagnoses, Allergies, Medications, Laboratory, Immunizations, Procedures, ClinicalDocuments, PastMedicalHistory</b><br/>\n            If the list is empty, all categories are disabled.\n             <br/><i>Default: All</i>", null=True, verbose_name=b'Categories available for send')),
                ('send_to_my_EHR_success_message', models.CharField(help_text=b'If field is empty, the product default message will be used.<br/><i>Default: Empty</i>', max_length=200, null=True, verbose_name=b'Send to my EHR success message', blank=True)),
                ('send_to_my_EHR_failure_message', models.CharField(help_text=b'If field is empty, the product default message will be used.<br/><i>Default: Empty</i><br/><br/>This configuration enables you to define the message text that appears for a successful and an unsuccessful Send to EHR operation that was completed.', max_length=200, null=True, verbose_name=b'Send to my EHR failure message', blank=True)),
                ('send_to_my_EHR_ccda_only', models.BooleanField(default=False, help_text=b'Determines whether "Send to My EHR" will enable to send only documents that arrived to dbMotion as structured CCD/A, or any other media type, such as unstructured CCD/A, TIFF, PDF, etc.<br>True: Will support structured CCD/A only.<br>False: Will support sending any document type.<br><br>Note: The checkbox is enabled if "All" or "ClinicalDocuments" were chosen above.<br/><i>Default: False</i>', verbose_name=b'Send Only structured CCDA Documents')),
            ],
            options={
                'verbose_name': 'Application ID',
                'history_meta_label': 'Application ID',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectAddressEndpointsPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('components', models.ManyToManyField(to='dbmconfigapp.Component', null=True)),
                ('services', models.ManyToManyField(to='dbmconfigapp.Service', null=True)),
            ],
            options={
                'help_text': 'This table consolidates all configurations of Direct adresses and Reporting endpoints in one place. The configuraiton can be done in this page, and in each EHR Instance page. Each EHR Instance should have a unique Direct Adress. When relevent, configure the end point URL to send the numerator data for this EHR Instance to external reporting systems.<br/><i>Default: Empty</i>',
                'verbose_name': 'Meaningful Use Reporting Endpoints',
                'history_meta_label': 'Meaningful Use Reporting Endpoints',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Defines the name of the EHR', unique=True, max_length=100)),
                ('deployment_type', models.CharField(default=b'Local', help_text=b'\n        The EHR application can be either a desktop application or a Web-based application.<br/>\n        The Deployment type applies to both the EHR Agent and the EHR and can be one of the following: Desktop deployment or a desktop virtualization deployment, such as hosted on Citrix.<br/>\n        The Deployment Type configurations depend on both the EHR application type and the EHR Agent/EHR deployment.<br/>\n        For example, detecting when a Citrix-based EHR has been launched is difficult because it is hosted in a Citrix process and there can be multiple Citrix processes running simultaneously, each hosting a different application.<br/>\n        The following Deployment type options are available:<br/>\n        - EHR Agent on Desktop and EHR hosted on Citrix: The EHR is either a desktop or Web application. The EHR Agent is deployed on the desktop and the EHR is hosted on Citrix. <br/>\n        - Desktop EHR, with Both EHR Agent and EHR on Desktop/Both EHR Agent and EHR hosted on Citrix: The EHR is a desktop application. And both the EHR Agent and the EHR are deployed on the local desktop. Or, both the EHR Agent and the EHR are hosted on Citrix.<br/>\n        - Web EHR, with Both EHR Agent and EHR on Desktop/Both EHR Agent and EHR hosted on Citrix: The EHR is a Web application. And both the EHR Agent and the EHR are deployed on the local desktop. Or, both the EHR Agent and the EHR are hosted on Citrix.<br/>\n        ', max_length=100, choices=[(b'Citrix', b'EHR Agent on Desktop and EHR hosted on Citrix'), (b'Local', b'Desktop EHR, with Both EHR Agent and EHR on Desktop / Both EHR Agent and EHR hosted on Citrix'), (b'Web', b'Web EHR, with Both EHR Agent and EHR on Desktop / Both EHR Agent and EHR hosted on Citrix')])),
                ('detection_exe', models.CharField(help_text=b'Defines the EHR executable application file name.<br/>The value is a regular expression. For more information about regular expression refer to <a href="https://msdn.microsoft.com/en-us/library/az24scfc(v=vs.110).aspx">MSDN Regular Expression Language guide</a>.', max_length=260, null=True, verbose_name=b'Executable', blank=True)),
                ('detection_url', models.CharField(help_text=b"Defines the EHR's Url", max_length=260, null=True, verbose_name=b'URL', blank=True)),
                ('detection_title', models.CharField(help_text=b'This parameter is used to detect the window label of an EHR in order to anchor the EHR Agent to the window that matches this title.<br/>This configuration is important in scenarios when "Follow Focused Window" is checked. In this case, and if the title is empty, the EHR Agent will anchor itself to every new window and every dialog box belonging to the EHR.<br/>The value is a regular expression. For more information about regular expression refer to <a href="https://msdn.microsoft.com/en-us/library/az24scfc(v=vs.110).aspx">MSDN Regular Expression Language guide</a>.<br/><i>Default: Empty</i>', max_length=200, null=True, verbose_name=b'EHR Window Title', blank=True)),
                ('detection_launch_title', models.CharField(help_text=b'Defines the Title of the EHR application, which is used to enable the system to detect this EHR by its title. If the Title is undefined, the EHR will be detected only by its Executable Application file name.<br/>The value functions as a regular expression. For more information about regular expression refer to <a href="https://msdn.microsoft.com/en-us/library/az24scfc(v=vs.110).aspx">MSDN Regular Expression Language guide</a>.<br/><b>Note:</b> EHR Agent will ignore this value on Share Desktop mode.', max_length=200, null=True, verbose_name=b'EHR Detection Title', blank=True)),
                ('detection_window_class', models.CharField(help_text=b'This parameter is used to detect the window class of an EHR in order to identify that the running application is the desired EHR.<br/>This configuration is important in scenarios when there may be multiple windows which are otherwise indistinguishable.<br/>The value is a regular expression. For more information about regular expression refer to <a href="https://msdn.microsoft.com/en-us/library/az24scfc(v=vs.110).aspx">MSDN Regular Expression Language guide</a>.<br/><i>Default: Empty</i>', max_length=200, null=True, verbose_name=b'EHR Window Class', blank=True)),
                ('detection_follow_focused_window', models.BooleanField(default=False, help_text=b"Determines to which EHR window the EHR Agent will be anchored.<br/>True: If the target EHR has several windows, the EHR Agent will anchor to the EHR's focused window.<br/>False: The EHR Agent will anchor to the EHR's first window.<br/><i>Default: False</i>", verbose_name=b'Follow focused window')),
                ('prevent_detected_window_topmost', models.BooleanField(default=False, help_text=b'This option supports the following case:<br/>1.The EHR has multiple windows.<br/> 2. The focused window must be generally followed by the Agent.<br/> 3. There is a window in focus, which should not be detected by the Agent at the moment, according to other configuration settings. <br/> 4. Another EHR window, which is currently detected by the Agent, should not be automatically repositioned to be the topmost window, so that it does not block the focused window. <br/><i>Default: False</i>', verbose_name=b'Prevent detected window reposition to topmost window')),
                ('detection_version', models.CharField(help_text=b'Defines the EHR product version as defined in the executable application.', max_length=40, null=True, verbose_name=b'Version', blank=True)),
                ('position_app_corner', models.CharField(default=b'RightTop', help_text=b'<i>Default: Right Top</i>', max_length=20, verbose_name=b'App corner', choices=[(b'LeftTop', b'Left Top'), (b'RightTop', b'Right Top'), (b'LeftBottom', b'Left Bottom'), (b'RightBottom', b'Right Bottom')])),
                ('position_agent_corner', models.CharField(default=b'RightTop', help_text=b'<i>Default: Right Top</i>', max_length=20, verbose_name=b'Agent corner', choices=[(b'LeftTop', b'Left Top'), (b'RightTop', b'Right Top'), (b'LeftBottom', b'Left Bottom'), (b'RightBottom', b'Right Bottom')])),
                ('position_offset_x', models.IntegerField(default=0, help_text=b'<i>Default: 0</i>', verbose_name=b'Offset X')),
                ('position_offset_y', models.IntegerField(default=40, help_text=b'<i>Default: 40</i>', verbose_name=b'Offset Y')),
            ],
            options={
                'verbose_name': 'EHR',
            },
            bases=(models.Model, externalapps.models.ExternalAppsBaseModel),
        ),
        migrations.CreateModel(
            name='InstallationProfile',
            fields=[
                ('id', models.PositiveIntegerField(unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'', help_text=b'Name.', unique=True, max_length=100, verbose_name=b'Name')),
                ('product_server_url', models.CharField(help_text=b"Used by the update service to download new client versions when using a File System path<br/><i>(e.g. \\networkdrive\\sharedfolder\\EhrAgentUpdate.zip)</i><br/>If this value is not a File System path, Agent will get new client versions based on the Profile, Web Server and Domain values.<br/><b>Name of XML Element:</b>SMART_AGENT_PRODUCT_SERVER_URL<br/>For Agent client versions older than 19.2 CU2 to use this configuration, it's needed to activate access to this URL.<br/>Refer to the product documentation for more information.", max_length=500, null=True, verbose_name=b'Product Server URL', blank=True)),
                ('is_auto_run', models.BooleanField(default=True, help_text=b'Determines whether the Agent Hub starts immediately after installation and also with the client machine restart.<br/><b>Name of XML Element:</b>SMART_AGENT_AUTO_RUN<br/><i>Default: True</i>', verbose_name=b'Auto Run')),
                ('is_install_ccow_context_receiver', models.BooleanField(default=False, help_text=b'Indicates whether or not to install the Context Manager Lite.<br/><b>Name of XML Element:</b>SMART_AGENT_INSTALL_CCOW_CONTEXT_RECEIVER<br/><i>Default: False</i>', verbose_name=b'Install CCOW Context Receiver')),
                ('is_install_dbm_context_receiver', models.BooleanField(default=False, help_text=b'If set to true, enables the Agent Hub Context Manager Lite and a third party context manager (for example, Sentillion) to work together on the same machine.<br/><b>Name of XML Element:</b>SMART_AGENT_INSTALL_DBM_CONTEXT_RECEIVER<br/><i>Default: False</i>', verbose_name=b'Install DBM Context Receiver')),
                ('is_launch_api', models.BooleanField(default=False, help_text=b'Not supported yet.<br/><b>Name of XML Element:</b>SMART_AGENT_LAUNCH_API_SERVICE_MODE<br/><i>Default: False</i>', verbose_name=b'Launch API Service Mode')),
                ('profile_name', models.CharField(default=externalapps.models_installation_profiles.fill_server_name, help_text=b'Server name.<br/><b>Name of XML Element:</b>SMART_AGENT_PROFILE_NAME<br/><i>Default: $_NODE_WEB_SERVER_STATEFUL$</i>', max_length=100, verbose_name=b'Profile Name')),
                ('is_show_system_tray_icon', models.BooleanField(default=True, help_text=b'Determines whether the Agent Hub displays the System Tray icon.<br/><b>Name of XML Element:</b>SMART_AGENT_SHOW_SYSTEM_TRAY_ICON<br/><i>Default: True</i>', verbose_name=b'Show System Tray Icon')),
                ('web_server_stateful', models.CharField(default=externalapps.models_installation_profiles.fill_server_name, help_text=b'Server name.<br/>For NLB configurations, it defines the stateful VIP Address.<br/>Together with Node User Absolute Domain configuration, it configure the New Product versions URL and download configurations URL.<br/>The default value for New Product versions URL and download configurations URL are:<br/>- https://$_NODE_WEB_SERVER_STATEFUL$.$_NODE_ACCESS_ABSOLUTE_DOMAIN$/SmartAgent/AgentSetup/[Pofile Name]/EhrAgentUpdate.zip<br/>- https://$_NODE_WEB_SERVER_STATEFUL$.$_NODE_ACCESS_ABSOLUTE_DOMAIN$/SmartAgent/Config/<br/><b>Name of XML Element:</b>_NODE_WEB_SERVER_STATEFUL, SMART_AGENT_CONFIG_SERVER_URL and SMART_AGENT_PRODUCT_SERVER_URL<br/><i>Default: $_NODE_WEB_SERVER_STATEFUL$</i>', max_length=500, verbose_name=b'Node Web Server Stateful')),
                ('user_absolute_domain', models.CharField(default=externalapps.models_installation_profiles.fill_node_absolute_domain, help_text=b'AD Domain.<br/><b>Name of XML Element:</b>_NODE_USER_ABSOLUTE_DOMAIN<br/><i>Default: $_NODE_ACCESS_ABSOLUTE_DOMAIN$</i>', max_length=100, verbose_name=b'Node User Absolute Domain')),
                ('is_multitenant', models.BooleanField(default=False, help_text=b'Determines whether the Agent Hub is configured in multitenant mode.<b>Note:</b> If this is set to true, the update mechanism is disabled and the update configurations are not relevant.<br/><b>Name of XML Element:</b>ISMULTITENANT<br/><i>Default: False</i>', verbose_name=b'Is Multitenant')),
                ('is_uninstall_previous_version', models.BooleanField(default=True, help_text=b'If set to false, upon first time installation will remove existing Agent Hub version.<br/><b>Name of XML Element:</b>SMART_AGENT_UNINSTALL_PREVIOUS_VERSIONS<br/><i>Default: True</i>', verbose_name=b'Uninstall Previous Versions')),
                ('is_update_configuration_enabled', models.BooleanField(default=True, help_text=b'Determines whether the Agent Hub client will update the configuration files automatically.<br/><b>Name of XML Element:</b>SMART_AGENT_UPDATE_CONFIGURATION_ENABLED<br/><i>Default: True</i>', verbose_name=b'Enable Update Configuration')),
                ('is_update_new_version_enabled', models.BooleanField(default=False, help_text=b'Determines whether Agent Hub will upgrade to a new version automatically via the Easy Deployment process.<br/>Note: When setting this option to <b>true</b>, the update service will run under a local system account, which runs with administrator permissions.<br/><b>Name of XML Element:</b>SMART_AGENT_UPDATE_NEW_VERSION_ENABLED<br/><i>Default: False</i>', verbose_name=b'Enable Update New Version')),
                ('is_activate_ccow_receiver', models.BooleanField(default=False, help_text=b'If true, Agent Hub installation will not create a registry key for auto launch of the Agent Hub by EMR context join request.<br/><b>Name of XML Element:</b>SMART_AGENT_CCOW_CONTEXT_RECEIVER_NO_ACTIVATION<br/><i>Default: False</i>', verbose_name=b'No Activation of CCOW Context Receiver')),
                ('is_display_alert_message', models.BooleanField(default=False, help_text=b'If false, the Agent Hub first installation will not display a popup message to close the EHRs.<br/><b>Name of XML Element:</b>DISPLAY_EHR_ALERT_MESSAGE<br/><i>Default: False</i>', verbose_name=b'Display EHR Alert Messages')),
                ('is_ccow_isolated_session', models.BooleanField(default=False, help_text=b'If set to true, enables users to work in shared desktop mode.<br/><b>Note:</b> If set to true, SMART_AGENT_INSTALL_CCOW_CONTEXT_RECEIVER must also be set to true.<br/><b>Name of XML Element:</b>CCOW_ISOLATING_SESSION_MANAGER_ENABLED<br/><i>Default: False</i>', verbose_name=b'Enable CCOW Isolating Session Manager')),
                ('display_lang', models.CharField(default=externalapps.models_installation_profiles.fill_default_language, help_text=b'Display language and also regional setting behavior.<br/><b>Name of XML Element:</b>SMART_AGENT_DISPLAY_LANGUAGE<br/><i>Default: $_NODE_DEFAULT_LANGUAGE$</i>', max_length=100, verbose_name=b'Display Language')),
                ('install_url', models.TextField(help_text=b'Link to the first time installation file. This link can be used to allow secure access to installation files.<br/>The link URL will be created when saving the Installation Profile.', null=True, verbose_name=b'Installation URL', blank=True)),
                ('install_url_expiration_date', models.DateField(null=True, verbose_name=b'Expiration Date')),
            ],
            options={
                'help_text': '\n        This configuration is used to define set of the installation profiles.\n        \n        <br/>To add a node, select the required row and click Action -> Duplicate existing installation profiler(s). Then click Go.. \n        <br/>To delete a node, select the required row and click Action -> Delete installation profiler(s). Then click Go.\n        <br/>To change a node configuration, click on the profile name and edit the profile properties as required.<br><br>\n        ',
                'verbose_name': 'EHR Agent Installation Profiles',
                'history_meta_label': 'EHR Agent Installation Profiles',
                'verbose_name_plural': 'EHR Agent Installation Profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Defines the EHR instance name.', unique=True, max_length=100)),
                ('is_enabled', models.BooleanField(default=True, help_text=b'Determines if the current instance is enabled.')),
                ('env_variable_name', models.CharField(max_length=100, null=True, verbose_name=b'Environment variable name', blank=True)),
                ('env_variable_value', models.CharField(help_text=b'Defines various environment variables.<br/>If the properties based on the executable application are not enough to differentiate two different EHR Agent scenarios, the environment variables are used. In this case, a different environment variable will be set on the client computers working in different scenarios.<br/>Then, the System Engineer should set the name and the value of the variable.', max_length=100, null=True, verbose_name=b'Environment variable value', blank=True)),
                ('direct_address', models.EmailField(help_text=b"Defines Direct Address associated to the EHR instance.<br/>When users send Direct messages from ClinicalView Agent, this address will be the user's sending address.<br/>Example: Facility.name@location.direct.com<br/><i>Default: Empty</i>", max_length=100, null=True, verbose_name=b'Direct Address', blank=True)),
                ('direct_address_suffix', models.CharField(help_text=b'\n        Define suffix for a group of direct addresses.<br/> \n        Should only use in case the EHR using privates direct addresses for his providers and routed the direct messages also to dbMotion<br/>\n        Example: @location.direct.com\n        <br/><i>Default: Empty</i>', max_length=50, null=True, verbose_name=b'Direct Address Suffix', blank=True)),
                ('mu_reporting_endpoint', models.CharField(default=b'', max_length=500, blank=True, help_text=b'Defines the endpoint URL used to report Sending/Receiving of CCDA documents over Direct. <br/><i>Default: Empty</i>', null=True, verbose_name=b'Meaningful Use Reporting Endpoint')),
                ('mu_reporting_source_system_name', models.CharField(default=b'', max_length=200, blank=True, help_text=b'\n        Define the source system name as exist in the CDR common.device.devicename.<br/>\n        <b>Note:</b> This field should be configured <b>only</b> if two or more EHR instances using the same OID in "Assigning Authority for display" and the reporting process should find only the relevant patient for the EHR instance.\n        <br/><i>Default: Empty</i>', null=True, verbose_name=b'Source System Name')),
                ('mu_reporting_type', models.CharField(choices=[(b'SCM', b'SCM'), (b'TW', b'TW')], max_length=50, blank=True, help_text=b'\n        Defines the interface used to report Sending/Receiving of CCDA documents over Direct.<br/>\n        <b>Note:</b> This field is mandatory if an endpoint is configured.<br/>\n        SCM: SCM interface (reporting to CPM).<br/>\n        TW: TW interface (reporting to AAP).\n        <br/><i>Default: Empty</i>', null=True, verbose_name=b'Reporting Interface')),
                ('mu_reporting_login', models.CharField(default=b'', max_length=100, blank=True, help_text=b'\n        Define the Unity service user that will be used when reporting to TW.<br/>\n        Unity service user should be configured for the relevant TW environment: TEST / PROD.<br/>\n        <b>Note:</b> This field is mandatory when TW is the reporting interface.\n        <br/><i>Default: Empty</i>', null=True, verbose_name=b'Unity Service User')),
                ('mu_reporting_password', dbmconfigapp.utils.encryption.EncryptedCharField(default=b'', max_length=100, blank=True, help_text=b'\n        Define the Unity service Password that will be used when reporting to TW.<br/>\n        Unity service Password should be configured for the relevant TW environment: TEST / PROD.<br/>\n        <b>Note:</b> This field is mandatory when TW is the reporting interface. \n        <br/><i>Default: Empty</i>', null=True, verbose_name=b'Unity Service Password')),
                ('mu_reporting_app_name', models.CharField(default=b'', max_length=200, blank=True, help_text=b'\n        Define dbMotion application name as configured in Unity.\n        Application name should be configured for the relevant TW environment: TEST / PROD.\n        <b>Note:</b> This field is mandatory when TW is the reporting interface.\n        <br/><i>Default: Empty</i>', null=True, verbose_name=b'Application Name')),
                ('mu_reporting_community_oid', models.CharField(default=b'', max_length=200, blank=True, help_text=b'\n        Define TW Community OID as configured in TW, for the dbMotion - TW integration.<br/> \n        The value should be provided from TW resource.<br/>\n        <b>Note:</b> This field is mandatory when TW is the reporting interface.\n        <br/><i>Default: Empty</i>', null=True, verbose_name=b'Community OID')),
                ('thumbprint', models.CharField(default=None, max_length=100, blank=True, help_text=b'\n        Defines thumbprint of the certificate for the configured endpoint in the field: Meaningful Use Reporting Endpoint.<br/>\n        <b>Note:</b> This field is mandatory if an endpoint is configured and SCM is the reporting interface. \n        <br/><i>Default: Empty</i>', null=True, verbose_name=b'Certificate Thumbprint')),
                ('ccow_item_name', models.CharField(help_text=b'Defines a CCOW parameter with an added suffix (for example,  the syntax will be Patient.Id.Mrn.Suffix) that is used to identify an EHR instance.<br/><br/><b>Configure this parameter when there is a need to differentiate between EHR instances, when</b> all instances have the same values for the following parameters (meaning that the system cannot differentiate between them):<br/>- Same EHR (Application)<br/>- URL (for Web application)<br/>- Executable file name (for Desktop application)<br/>- Application Title<br/>- Application Version<br/>- Environment Variable (or cannot create it)<br/>- Context Type<br/>- Participant Name<br/>- Passcode<br/>- Same Supported profiles<br/><br/>This configuration provides an additional method for organizations to differentiate between the instances of the same EHR. When the instance is identified, the relevant product functionality will apply per instance, as usual.<br/><br/>- Delta View can be configured per instance<br/>- Unique Patient Assigning Authority can be configured per instance<br/>- Send to My EHR endpoint can be configured per instance<br/><br/>For the implementation of this functionality, the following conditions apply:<br/>- It applies only with context interception using CCOW.<br/>- Each EHR instance is configured with a separate Properties Package.<br/><br/><b>Limitation:</b><br/>This configuration is ignored for an Instance with a Property Package that has more than one configured Patient Assigning Authority.', max_length=100, null=True, verbose_name=b'CCOW Parameter for EHR Instance Identification', blank=True)),
                ('context_type', models.CharField(default=b'CcowParticipant', max_length=20, choices=[(b'CcowParticipant', b'CCOW - EHR Agent plays Participant role (Context Manager available)'), (b'CcowReceiver', b'CCOW - EHR Agent plays Context Manager role (Context Manager light)'), (b'NonCcow', b'Non CCOW - Custom context interceptor')])),
                ('interceptor_type', models.TextField(help_text=b'Full namespace and assembly name are required in Non-CCOW scenario.', null=True, verbose_name=b'Plugin type name', blank=True)),
                ('is_user_mapping_enabled', models.BooleanField(default=False, help_text=b'User mapping is needed when the user context must be obtained from the EHR display, and the user`s display name is not identical to the username in the Active Directory.', verbose_name=b'Enable user mapping')),
                ('user_mapping_file_path', models.TextField(help_text=b"Enter the mapping file's full path including the file extension, such as \\MachineName\\FolderName\\UserMapping.xml.<br>The file path must be accessible from the application servers.", null=True, verbose_name=b'Mapping file path', blank=True)),
                ('user_mapping_is_use_as_role', models.BooleanField(default=False, help_text=b'If selected, the user context will not be resolved by name. The role of the user will be used by the Agent Hub to determine the correct permissions for hosted applications.', verbose_name=b'Map user as a role')),
                ('user_mapping_is_default_to_loggedInUser', models.BooleanField(default=False, help_text=b'If the displayed user is listed multiple times in the mapping file, use the logged-in user by default.', verbose_name=b'Use logged-in user by default')),
                ('exclude_dash_from_mrn', models.BooleanField(default=True, help_text=b'Defines whether EHR Agent will exclude dash character from the MRN, which recieved in the CCOW context.<br/>NOTE: This funcionality is availible only when Agent Hub is CCOW Participant or CCOW Context Manager.<br/>By default, this functionality is enabled.<br/><i>Default: True</i>', verbose_name=b'Exclude dash character from MRN')),
                ('blink_only_first_doa', models.BooleanField(default=False, help_text=b"Defines whether EHR Agent will display the Badging only during the patient's first day of admission.<br/>By default, this functionality is disabled. This means that by default the EHR Agent will display the Badging in all cases where there is a delta in the configured attention time frame.<br/><i>Default: False</i>", verbose_name=b'Display Badging only on first day of admission')),
                ('supported_profiles', models.CharField(help_text=b'Defines a comma-separated list of Profiles that can use this EHR instance. If empty, all profiles can use it.<br/> \n                                                                                                                                             The Profile defines various installation attributes that determine how Agent Hub will be installed on the client machine.<br/>\n                                                                                                                                             Each Profile has a unique sub-folder under: \\\\Web App Server\\EHRAgentSetup\\.<br/>\n                                                                                                                                             For example: Default Profile, CCOW, CCOW Shared Desktop.<br/><i>Default: Empty</i>', max_length=400, null=True, verbose_name=b'Supported profiles', blank=True)),
                ('facility_root', models.CharField(help_text=b'Defines the root Identifier of the facility, according to [dbmVCDRData].[Common].[Organization].[Id_Root] .', max_length=400, null=True, verbose_name=b'Facility ID root', blank=True)),
                ('facility_extension', models.CharField(help_text=b'Defines the extension Identifier of the facility, according to [dbmVCDRData].[Common].[Organization].[Id_Extension].<br/><br/>\n                                                                                                                                                The active EHR instance facility is identified by the unique features of the EHR instance.<br/>\n                                                                                                                                                To distinguish between EHR instances associated with different facilities, configure one of the following:<br/>\n                                                                                                                                                &nbsp;&nbsp;- If the EHR instance has a unique EXE file name , Window title, or URL per facility, configure only the Facility ID Root and Extension fields.<br/>\n                                                                                                                                                &nbsp;&nbsp;- If the EHR instance EXE file name and Window title is not unique per facility, configure each EHR instance with the relevant environment variable name and value, as well as the Facility ID Root and Extension fields.<br/>\n                                                                                                                                                ', max_length=400, null=True, verbose_name=b'Facility ID extension', blank=True)),
                ('ofek_url', models.CharField(help_text=b'Defines the ofek url.', max_length=400, null=True, verbose_name=b'Ofek Url', blank=True)),
                ('uiAutomation_config_file_path', models.TextField(help_text=b'Enter the UI Automation configuration files full path including the file extension.', null=True, verbose_name=b'UI Automation configuration file path', blank=True)),
                ('nonCcowPluginType', models.CharField(default=b'Custom', max_length=500, verbose_name=b'Non CCOW plugin type', choices=[(b'Custom', b'Custom'), (b'ContextProviderServiceInterceptor.ContextProviderServiceInterceptor, dbMotion.SmartAgent.ContextProviderServiceInterceptor', b'UI Automation')])),
                ('ehr', models.ForeignKey(on_delete=models.CASCADE, verbose_name=b'EHR', to='externalapps.EHR', help_text=b'Select the EHR for which you want to create an instance.')),
                ('endpoints_page', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='externalapps.DirectAddressEndpointsPage', null=True)),
            ],
            options={
                'help_text': '\n        These configurations are used to do one of the following:\n        <ul>\n        <li>Create a new instance of an EHR. Each EHR (for example, Pro) might have various instances installed in different hospital departments or clinics. The properties might be different for each EHR instance and must be configured separately for each.</li>\n        <li>Edit properties of an existing EHR instance.</li>\n        <li>Delete an EHR instance.</li>\n        </ul>\n        ',
                'verbose_name': 'EHR Instance',
                'history_meta_label': 'EHR Instance',
            },
            bases=(models.Model, externalapps.models.ExternalAppsBaseModel),
        ),
        migrations.CreateModel(
            name='InstanceProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('ehr_user_assign_auth', models.CharField(help_text=b'Define the root ID of the EHR user to enable a hosted application user to login automatically to the application after logging into the EHR.<br/><i>Default: Empty.</i>', max_length=400, null=True, verbose_name=b'EHR User Assigning Authority', blank=True)),
                ('patient_assigning_Authority_for_Display', models.CharField(help_text=b'When Patient View is launched using Launch API, clients specify the source system from which the patient medical record number (MRN) is taken as leading. The MRN and demographics are displayed in the patient banner and reports. Multiple values should be divided by "|" as separator.<br/>\n\t\t\t   Values include:<br/>\n               - FIRST_FROM_VIA :First index from VIA response is selected as leading.<br/>\n\t\t\t   - OID :Multiple OIDs with "FIRST_FROM_VIA" can be added. Display priority is based on the left-to-right order of entry. Example - 1.01.01.01.0 | FIRST_FROM_VIA<br/>\n               - Empty (default) :Demographics from searched MRN is displayed.<br/>\n\t\t\t     <b>Note:</b> When single OID or multiple are configured and the index is not found in VIA response according to configuration , application will continue to display (default) searched MRN as leading index to show demographics.', max_length=400, null=True, verbose_name=b'Patient Assigning Authority for Display', blank=True)),
                ('app_id', models.ForeignKey(on_delete=models.SET_NULL, to='externalapps.AppId', null=True)),
            ],
            options={
                'verbose_name': 'Properties Package',
                'history_meta_label': 'Properties Package',
            },
            bases=(models.Model, externalapps.models.ExternalAppsBaseModel),
        ),
        migrations.CreateModel(
            name='OrderingFacilities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('act_type', models.CharField(help_text=b'Possible values are: LabEvent, PathologyEvent, ClinicalImageStudy, ClinicalDocument', max_length=50, verbose_name=b'Act Type', choices=[(b'ClinicalDocument', b'Clinical Document'), (b'ClinicalImageStudy', b'Clinical Image Study'), (b'LabEvent', b'Lab Event'), (b'PathologyEvent', b'Pathology Event')])),
                ('facility_root', models.CharField(max_length=100, null=True, verbose_name=b'Ordering Facility ID Root')),
                ('facility_extension', models.CharField(max_length=100, null=True, verbose_name=b'Ordering Facility ID Extension')),
                ('app_id', models.ForeignKey(on_delete=models.SET_NULL, to='externalapps.AppId', null=True)),
                ('instance_properties', models.ForeignKey(on_delete=models.SET_NULL, to='externalapps.InstanceProperties', null=True)),
            ],
            options={
                'verbose_name': 'Delta View By Ordering Facilitie',
            },
            bases=(models.Model, externalapps.models.ExternalAppsBaseModel),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=20, null=True, blank=True)),
                ('name', models.CharField(help_text=b'Identifies the participant in the Context Manager.', max_length=100)),
                ('ccow_passcode', models.TextField(help_text=b'CCOW Passcode is used for a secured registration to the Context Manager.', verbose_name=b'CCOW passcode')),
                ('is_shared', models.BooleanField(default=False, help_text=b'This value is used to specify if participant is shared. If true, this participant can be associated with several instances of the same EHR. Note: Is Shared functionality works only for non Web EHRs')),
                ('instance', models.ForeignKey(on_delete=models.SET_NULL, to='externalapps.Instance')),
            ],
            options={
            },
            bases=(models.Model, externalapps.models.ExternalAppsBaseModel),
        ),
        migrations.CreateModel(
            name='PatientContext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_assign_auth_resolve', models.CharField(max_length=400, verbose_name=b'Patient Assigning Authority for resolve')),
                ('patient_assign_auth_display', models.CharField(max_length=400, null=True, verbose_name=b'Patient Assigning Authority for display', blank=True)),
                ('suffix_type', models.CharField(default=b'MRN', max_length=20, choices=[(b'MRN', b'MRN'), (b'MPIID', b'MPIID')])),
                ('suffixes', models.CharField(max_length=100, null=True, verbose_name=b'suffix', blank=True)),
                ('instance_properties', models.ForeignKey(on_delete=models.CASCADE, to='externalapps.InstanceProperties')),
            ],
            options={
                'verbose_name': 'Patient Context',
            },
            bases=(models.Model, externalapps.models.ExternalAppsBaseModel),
        ),
        migrations.CreateModel(
            name='SourceSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('act_types', dbmconfigapp.models.fields.SelectMultipleChoicesField(default=b'All', help_text=b'Defines the types of clinical acts that can be sent from this dataSource to the main EHR.\nThe Data Integration engineer must determine all act types that can be sent from this data source. If all supported dbMotion act types can be sent, this attribute does not have to be defined.\nIf the data source can send only specific act types, these must be defined in this attribute.', max_length=400)),
                ('app_id', models.ForeignKey(on_delete=models.SET_NULL, to='externalapps.AppId', null=True)),
                ('instance_properties', models.ForeignKey(on_delete=models.SET_NULL, to='externalapps.InstanceProperties', null=True)),
            ],
            options={
                'verbose_name': 'Delta View Source System',
            },
            bases=(models.Model, externalapps.models.ExternalAppsBaseModel),
        ),
        migrations.CreateModel(
            name='UserContext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_context_type', models.CharField(default=b'Managed', max_length=100, choices=[(b'Managed', b'Managed'), (b'UnmanagedCredentials', b'Unmanaged credentials'), (b'UnmanagedSAML', b'Unmanaged SAML'), (b'SendToMyEHR', b'User for "Send to my EHR"')])),
                ('ad_domain', models.CharField(help_text=b'Defines the active directory domain', max_length=100, null=True, verbose_name=b'AD Domain', blank=True)),
                ('suffixes', models.CharField(max_length=100, null=True, verbose_name=b'suffix', blank=True)),
                ('instance_properties', models.ForeignKey(on_delete=models.CASCADE, to='externalapps.InstanceProperties')),
            ],
            options={
                'verbose_name': 'User Context',
            },
            bases=(models.Model, externalapps.models.ExternalAppsBaseModel),
        ),
        migrations.AlterUniqueTogether(
            name='sourcesystem',
            unique_together=set([('name', 'app_id')]),
        ),
        migrations.AddField(
            model_name='instance',
            name='instance_properties',
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name=b'Properties Package', to='externalapps.InstanceProperties', help_text=b'Configure the properties for each EHR Instance by doing one of the following:<br/>- Select one of the Properties Packages from the dropdown list to reuse a set of predefined properties for this instance.<br/>- Click the plus sign to open a dialog box where you can configure a new Properties Package for this instance which can later be reused.'),
            preserve_default=True,
        ),
    ]
