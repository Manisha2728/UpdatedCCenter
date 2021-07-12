# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import dbmconfigapp.models.fields
import dbmconfigapp.models.clinical_viewer_general
import dbmconfigapp.utils.custom_validators
import dbmconfigapp.models.apps_patient_display
import dbmconfigapp.models.operational_manager
import dbmconfigapp.models.ehragent
import dbmconfigapp.models.pl_general
import django.core.validators
import dbmconfigapp.models.db_files
import dbmconfigapp.models.database_storage


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentHubGeneralPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'General Definitions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentppHostedApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(help_text=b'Hosted application name.', unique=True, max_length=30, verbose_name=b'Hosted Application Name')),
                ('app_key', models.CharField(help_text=b'Used to identify special applications', max_length=30, null=True, blank=True)),
                ('enabled', models.BooleanField(default=False, help_text=b'Enable one or more of the following applications to be hosted by the Agent Hub.', verbose_name=b'Enabled')),
                ('LogoFile', models.ImageField(default=b'', help_text=b'Define the logo file that will be displayed for the application in the Agent Hub header.', storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), verbose_name=b'Logo File', upload_to=b'AgentHostedApps/Logo')),
                ('launch_url', models.CharField(default=b'', help_text=b'Define the launch URL of the hosted application.', max_length=1000, verbose_name=b'Application Page URL')),
                ('get_application_state_url', models.CharField(default=b'', help_text=b'Define the URL that will be used to send the updated context information (user/patient) to the hosted application.', max_length=1000, verbose_name=b'Application State URL')),
                ('permitted_roles', models.CharField(default=b'All', help_text=b"<b>Defines the user roles which can access this application.</b><br/>Possible values: All, None, Role names separated by ','. <br/>When the value is 'All' all users will have access to this application. <br/>When certain role(s) are filled, only users having those role(s) will be able to access this application.<br/>When the value is 'None' no user can access this application.<br/>Default: All.", max_length=500, verbose_name=b'Permitted Roles')),
                ('is_user_alias_required', models.BooleanField(default=False, help_text=b'Enable dbMotion User Aliasing Service.', verbose_name=b'Define if dbMotion User Aliasing Service is Required')),
                ('is_window_resizable', models.BooleanField(default=True, help_text=b'Enable the following application to have resizable window.', verbose_name=b'Resizable Window')),
                ('window_default_width_size', models.IntegerField(default=b'1024', help_text=b'Set window default width size.', verbose_name=b'Window Default Width Size')),
                ('window_minimal_width_size', models.IntegerField(default=b'640', help_text=b'Set window minimal width size.', verbose_name=b'Window Minimal Width Size')),
                ('window_maximal_width_size', models.IntegerField(help_text=b'Set window maximal width size.', null=True, verbose_name=b'Window Maximal Width Size', blank=True)),
                ('window_default_height_size', models.IntegerField(default=b'768', help_text=b'Set window default height size.', verbose_name=b'Window Default Height Size')),
                ('window_minimal_height_size', models.IntegerField(default=b'480', help_text=b'Set window minimal height size.', verbose_name=b'Window Minimal Height Size')),
                ('window_maximal_height_size', models.IntegerField(help_text=b'Set window maximal height size.', null=True, verbose_name=b'Window Maximal Height Size', blank=True)),
                ('display_name', models.CharField(default=None, max_length=100, null=True, help_text=b'The name to be displayed in the Launcher.', blank=True)),
            ],
            options={
                'verbose_name': 'Patient Centric Application',
                'history_meta_label': 'Patient Centric Application',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentppHostedAppPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Hosted Applications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentHostedAppsBehavior',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_app_related_to_ehr', models.BooleanField(default=True, help_text=b'Determines how Agent Hub hosted applications are displayed in relation to the EHR. Applications are operational and displayed with a patient in context in the EHR.<br/>\n- False - Applications display independent of the EHR and can be minimized regardless of EHR state.<br/>\n- True (default) -  Application display is dependent on Agent Hub and EHR display. Agent Hub must be displayed for the application to be displayed.<br/><i>Default: True</i>', verbose_name=b'Applications visibility is related to the EHR')),
                ('page', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.AgentppHostedAppPage', null=True)),
            ],
            options={
                'verbose_name': 'Hosted Applications Visibility Behavior',
                'verbose_name_plural': 'Hosted Applications Visibility Behavior',
                'history_meta_label': 'Hosted Applications Visibility Behavior',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentSMARTonFHIRApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(help_text=b'Name of the SMART on FHIR application. Obtain this information from the application owner.', unique=True, max_length=100, verbose_name=b'Client Name')),
                ('enabled', models.BooleanField(default=False, help_text=b'Enable or disable the following SMART on FHIR application to be hosted by the Agent Hub.', verbose_name=b'Enabled')),
                ('client_id', models.CharField(help_text=b'The SMART on FHIR application ID. The Client ID should be unique for this node. Obtain this information from the application owner.', unique=True, max_length=100, verbose_name=b'Client ID')),
                ('launch_url', models.CharField(help_text=b'Launch URL of the SMART on FHIR application. Obtain this information from the application owner.', max_length=100, verbose_name=b'Launch URL')),
                ('redirect_url', models.CharField(help_text=b'Redirect URL of the SMART on FHIR application. Obtain this information from the application owner.', max_length=100, verbose_name=b'Redirect URL')),
                ('logo_file', models.ImageField(default=b'', help_text=b'Define the logo file that will be displayed for the of the SMART on FHIR application in the Agent Hub header. The logo size must be 20x20 pixels.', storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), verbose_name=b'Logo File', upload_to=b'AgentSMARTonFHIRApps/Logo')),
                ('resizable_window', models.BooleanField(default=True, help_text=b'Enable the following SMART on FHIR application to have resizable window.', verbose_name=b'Resizable Window')),
                ('window_default_width_size', models.IntegerField(default=b'1024', help_text=b'Set window default width size.', verbose_name=b'Window Default Width Size')),
                ('window_minimal_width_size', models.IntegerField(default=b'640', help_text=b'Set window minimum width size.', verbose_name=b'Window Minimum Width Size')),
                ('window_maximal_width_size', models.IntegerField(default=b'1400', help_text=b'Set window maximum width size.', verbose_name=b'Window Maximum Width Size')),
                ('window_default_height_size', models.IntegerField(default=b'768', help_text=b'Set window default height size.', verbose_name=b'Window Default Height Size')),
                ('window_minimal_height_size', models.IntegerField(default=b'480', help_text=b'Set window minimum height size.', verbose_name=b'Window Minimum Height Size')),
                ('window_maximal_height_size', models.IntegerField(default=b'1050', help_text=b'Set window maximum height size.', verbose_name=b'Window Maximum Height Size')),
                ('use_dbmotion_fhir_server', models.BooleanField(default=True, help_text=b'Enable using the dbMotion FHIR Server.', verbose_name=b'Use dbMotion FHIR Server')),
            ],
            options={
                'verbose_name': 'SMART on FHIR Application',
                'history_meta_label': 'SMART on FHIR Application',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentUserCentricApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(help_text=b'Hosted application name.', unique=True, max_length=30, verbose_name=b'Hosted Application Name')),
                ('enabled', models.BooleanField(default=True, help_text=b'Enable the following application to be hosted by the Agent Hub.', verbose_name=b'Enabled')),
                ('LogoFile', models.ImageField(default=b'', storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), upload_to=b'AgentHostedApps/Logo', blank=True, help_text=b'Define the logo file that will be displayed for the application in the Agent Hub header.', null=True, verbose_name=b'Logo File')),
            ],
            options={
                'verbose_name': 'Population Health Application',
                'history_meta_label': 'Population Health Application',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppsAdvanceDirectiveNodes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nodes', models.CharField(default=b'', max_length=500, blank=True, help_text=b'Define a comma-separated list of the dbMotion nodes (as a Node ID) to be queried for Advance Directive documents. <br/>An empty value will send the request to all the nodes. <br/>For example, for Node ID=1 and Node ID=12, enter the following value:  1,12<br/><i>Default: empty</i>', null=True, verbose_name=b'Advance Directive nodes')),
                ('is_display_adv_dir', models.BooleanField(default=True, help_text=b'Enable the Advance Directive feature.<br/><i>Default: False</i>', verbose_name=b'Display Advance Directive')),
                ('adv_dir', models.CharField(default=b'ADVDIR', help_text=b'Define the displayed value of the Advance Directive indication.<br/><i>Default: ADVDIR</i>', max_length=6, verbose_name=b'Advance Directive indicator')),
            ],
            options={
                'history_meta_label': 'Advance Directives',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppsPatientDisplay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_search_name_format', models.CharField(default=b'{0}, |{1}', help_text=b'This configuration is used to define the display of the patient name returned after performing a Patient Search in Collaborate or the Clinical Viewer.<br/>The order of the Patient Name parts is defined according to the following values. You can make changes by removing a value, adding a value, or changing the order of the values.<br/>Where:<br/>- {0} = Last Name<br/>- {1} = First Name<br/>The | symbol is required to separate the data in the value, but is not displayed in the output.<br/><i>Default: {0}, |{1}</i>', max_length=60, verbose_name=b'Patient Name Display in Patient Search', validators=[dbmconfigapp.models.apps_patient_display.validate_name_format])),
                ('collaborate_address_format', models.CharField(default=b'{0} |{1}, |{2}, |{3}, |{4} |{5}', help_text=b"Defines the patient's address display in Collaborate and Agent Hub according to the following values.<br/>You can make changes to the display by removing a value, adding a value, or changing the order of the values.<br/>Where:<br/>- {0} = AddressLine1<br/>- {1} = AddressLine2<br/>- {2} = City<br/>- {3} = State<br/>- {4} = Country<br/>- {5} = Postal Code<br/>The | symbol is required to separate the data in the value, but is not displayed in the output. The comma is not required in the value. If it is in the value it will be displayed in the output. <br><i>Default: {0} |{1}, |{2}, |{3}, |{4} |{5}</i>", max_length=60, null=True, verbose_name=b'Patient Address Display (Collaborate, Agent Hub)', blank=True)),
                ('cv_address_format', models.CharField(default=b'{0}, |{1}, |{2}', help_text=b'Defines the patient address display in the Patient Search clinical view (in the Search Results table, Search History table, and Consent Manager form) according to the following values.<br/>You can make changes to the display by removing a value, adding a value, or changing the order of the values.<br/>Where:<br/>- {0} = Address<br/>- {1} = City<br/>- {2} = State<br/>The | symbol is required to separate the data in the value, but is not displayed in the output. The comma is not required in the value. If it is in the value it will be displayed in the output. <br><i>Default: {0}, |{1}, |{2}</i>', max_length=60, null=True, verbose_name=b'Patient Address Display (Clinical Viewer)', blank=True)),
                ('phone_format', models.CharField(default=b'{0}-|{1}-|{2}|(#{3})', help_text=b"The appearance of the patient's telephone number in Collaborate is defined according to the values below. You can make changes to the appearance by removing a value, adding a value, changing the order of the values, etc.<br/>Where:<br/>- {0} = Country Code<br/>- {1} = Area Code<br/>- {2} = Phone Number<br/>- {3} = Extension<br/>The | symbol is required to separate the data in the value, but is not displayed in the output in Collaborate. <br/><i>Default: {0}-|{1}-|{2}|(#{3})</i>", max_length=60, null=True, verbose_name=b'Patient Phone Number Format', blank=True)),
            ],
            options={
                'history_meta_label': 'Patient Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppsPatientDisplayAgeCalculation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_text', models.CharField(default=b'Patient younger than:', max_length=60, verbose_name=b'')),
                ('age_calc_time_span', dbmconfigapp.models.fields.TimeSpanField(default=b'1|0', help_text=b'', max_length=50, verbose_name=b'Patient Age Range (Upper Value)')),
                ('date_format', models.CharField(help_text=b'', max_length=5, verbose_name=b'Date Unit To Display', choices=[(b'PY', b'Years'), (b'PM', b'Months'), (b'PW', b'Weeks'), (b'PD', b'Days'), (b'PYM', b'Years and Months'), (b'TH', b'Hours'), (b'THM', b'Hours and Minutes')])),
                ('priority_order', models.IntegerField(help_text=b'', verbose_name=b'Order', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
            ],
            options={
                'verbose_name': 'Age Calculation Rule',
                'history_meta_label': 'Patient Age Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppsPatientDisplayCommon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_display_patient_mrn', models.BooleanField(default=True, help_text=b'Determines whether the MRN is displayed in the Patient Details header of the Clinical Views and Clinical View Agent.<br/><i>Default: True</i>', verbose_name=b'Display patient MRN in the applications')),
                ('is_display_patient_mrn_report', models.BooleanField(default=True, help_text=b'Determines whether the MRN is displayed in the Report Headers of Clinical Viewer and Clinical View Agent.<br/><i>Default: True</i>', verbose_name=b'Display patient MRN in the reports')),
            ],
            options={
                'history_meta_label': 'Patient MRN Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppsPatientDisplayMetricCodeBasedIndicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mci_oid_system', models.CharField(default=b'', help_text=b'Defines the code of the metric result that is formatted Code System|Code. Code can be local or baseline and it is a mandatory field to fill. Example: 2.16.840.1.113883.3.57.1.3.5.52.2.119|0130. Default: Empty', max_length=200, verbose_name=b'Metric code system|Code')),
                ('mci_interpretation', models.CharField(help_text=b'Defines the interpretation of the metric result to display. Select the value from the drop down. Default: Empty', max_length=15, verbose_name=b'Interpretation', choices=[(b'2', b'Low'), (b'4', b'Medium'), (b'8', b'High'), (b'16', b'Very High')])),
                ('mci_label', models.CharField(default=b'', help_text=b'Defines the Indicator text to display in Agent Hub and the patient banner. Maximum text length allowed is 15 characters. Default: Empty', max_length=15, verbose_name=b'Indicator label')),
                ('mci_priority', models.PositiveIntegerField(help_text=b'Defines the priority of the indicator to display within many metric code based indications. Allows entering only unique numeric values. Default: Empty', verbose_name=b'Priority', validators=[django.core.validators.MinValueValidator(1)])),
                ('mci_tooltip', models.CharField(default=b'', max_length=1000, blank=True, help_text=b'Defines the tooltip to display when hovering over an indicator when metric result text in the database is empty. Default: Empty', null=True, verbose_name=b'Tool tip')),
            ],
            options={
                'verbose_name': 'Metric Code Based Indicator entry',
                'history_meta_label': 'Metric Code Based Indicator',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppsPatientDisplayValueBaseProgram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vbp_oid_system', models.CharField(default=b'', max_length=120, blank=True, help_text=b"Defines the patient system OID (root id), which represents the patient's ID in the Value Based Program (VBP). This OID should also be configured in VIA.<br/> For example: 2.16.840.1.113883.3.57.1.3.5.52.1.8.6<br/><i>Default: empty</i>", null=True, verbose_name=b'System OID')),
                ('vbp_display_name', models.CharField(default=b'', max_length=5, blank=True, help_text=b'If the patient is in a VBP, defines the VBP name displayed in the EHR Agent and Clinical Viewer header. The value cannot exceed 5 chars.<br/><i>Default: empty</i>', null=True, verbose_name=b'Display Name')),
                ('vbp_risk_score_code', models.CharField(default=b'', max_length=200, blank=True, help_text=b"Defines the Code (in CodeSystem|Code format) of the patient's Risk Score.<br/>Code can be local or baseline<br/>For example: 2.16.840.1.113883.3.57.1.2.17.89|0006<br/><b>Note: The code that is configured and the code used to store the Risk Score in the CDR are assumed to be the same.</b><br/><i>Default: empty</i>", null=True, verbose_name=b'Risk Score Code')),
                ('vbp_low_risk_score', models.BooleanField(default=False, help_text=b'', verbose_name=b'Low')),
                ('vbp_medium_risk_score', models.BooleanField(default=False, help_text=b'', verbose_name=b'Medium')),
                ('vbp_high_risk_score', models.BooleanField(default=False, help_text=b'', verbose_name=b'High')),
                ('vbp_very_high_risk_score', models.BooleanField(default=False, help_text=b'', verbose_name=b'Very High')),
            ],
            options={
                'history_meta_label': 'Value Based Program',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppsPatientDisplayVBP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vbp_oid_system', models.CharField(default=b'', help_text=b"Defines the patient system OID (root id), which represents the patient's ID in the Value Based Program (VBP). This OID should also be configured in VIA.<br/> For example: 2.16.840.1.113883.3.57.1.3.5.52.1.8.6<br/><i>Default: empty</i>", max_length=120, verbose_name=b'System OID')),
                ('vbp_display_name', models.CharField(default=b'', help_text=b'If the patient is in a VBP, defines the VBP name displayed in the EHR Agent and Clinical Viewer header. The value cannot exceed 5 chars.<br/><i>Default: empty</i>', max_length=5, verbose_name=b'Display Name')),
                ('vbp_description', models.CharField(default=b'', max_length=1000, null=True, verbose_name=b'Description', blank=True)),
                ('vbp_display_name_long', models.CharField(default=b'', max_length=60, blank=True, help_text=b'If the patient is in a VBP, defines the VBP name displayed in the EHR Agent and Clinical Viewer header. The value should not exceed 15 chars.<br/><i>Default: empty</i>', null=True, verbose_name=b'Display Name')),
            ],
            options={
                'verbose_name': 'Value Based Program (VBP) entry',
                'history_meta_label': 'Value Based Program',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppsPatientDisplayWithAgent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_name_format', models.CharField(default=b'{0}, |{1} |{2}', help_text=b'This configuration is used to define the patient name display in:<br/>- Clinical Viewer Patient Header<br/>- EHR Agent Patient Header<br/>- Patient List<br/> The order of the Patient Name parts is defined according to the following values. You can make changes by removing a value, adding a value, or changing the order of the values.<br/>Where:<br/>- {0} = Last Name<br/>- {1} = First Name<br/>- {2} = Middle Initial<br/>The | symbol is required to separate the data in the value, but is not displayed in the output.<br/><i>Default: {0}, |{1} |{2}</i>', max_length=60, verbose_name=b'Patient Name Display', validators=[dbmconfigapp.models.apps_patient_display.validate_name_format])),
            ],
            options={
                'history_meta_label': 'Patient Display (Patient Header)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AppsReporting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('font_size', models.IntegerField(default=9, help_text=b'Defines the Font Size to use in the report.<br/>This applies to:<br/>- Collaborate: TXT reports.<br/>- EHR Agent: TXT reports.<br/>- Patient List: TXT reports.<br/>- Patient View: TXT reports.<br/><i>Default: 9</i>', verbose_name=b'Report Font Size', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)])),
                ('header_footer_font_type', models.CharField(default=b'Arial', help_text=b'Defines the Font Type in the header and footer of the report.<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><i>Default: Arial</i>', max_length=60, verbose_name=b'Report Header and Footer Font Type', choices=[(b'Arial', b'Arial'), (b'Courier New', b'Courier New')])),
                ('date_time_format', models.CharField(default=b'G', help_text=b'Defines the Date and Time format of the Report footer.<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><i>Default: General date/long time</i>', max_length=1, verbose_name=b'Date Time Format', choices=[(b'd', b'Short date: 4/17/2006'), (b'D', b'Long date: Monday, April 17, 2006'), (b't', b'Short time: 2:22 PM'), (b'T', b'Long time: 2:22:48 PM'), (b'f', b'Full date/short time: Monday, April 17, 2006 2:22 PM'), (b'F', b'Full date/long time: Monday, April 17, 2006 2:22:48 PM'), (b'g', b'General date/short time: 4/17/2006 2:22 PM'), (b'G', b'General date/long time (default): 4/17/2006 2:22:48 PM'), (b'M', b'Month: April 17'), (b'R', b'RFC1123: Mon, 17 Apr 2006 21:22:48 GMT'), (b's', b'Sortable: 2006-04-17T14:22:48'), (b'u', b'Universal sortable (invariant): 2006-04-17 21:22:48Z'), (b'U', b'Universal full date/time: Monday, April 17, 2006 9:22:48 PM'), (b'Y', b'Year: April, 2006'), (b'o', b'Roundtrip (local): 2006-04-17T14:22:48.2698750-07:00')])),
                ('microbiology_report_layout', models.IntegerField(default=0, help_text=b'Defines the Microbiology Report Layout.<br><i>Default: Standard product Microbiology Display</i>', verbose_name=b'Microbiology Report Layout', choices=[(0, b'Standard product Microbiology Display'), (1, b'UPMC specific Microbiology Display')])),
                ('show_confidentiality_disclamer', models.BooleanField(default=False, help_text=b'Determines whether the Clinical Viewer, Patient View, Collaborate and EHR Agent reports use the special disclaimer template (Word file) which displays the confidentiality disclaimer.<br/>True: The system uses the special Disclaimer templates for reports.<br/>False: The system uses the regular OOB templates for the reports (default).<br/><i>Default: False</i>', verbose_name=b'Show Confidentiality Disclaimer in Report')),
                ('customer_logo', models.ImageField(storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), upload_to=b'Logos/Customer', blank=True, help_text=b'Defines the customer logo image that will be displayed in the report:<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><b>Note:</b> Only .gif files are supported. The recommended size is: 120x40 px. The size cannot exceed 220x60 px.', null=True, verbose_name=b'Customer Logo')),
                ('dbmotion_logo', models.ImageField(storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), upload_to=b'Logos/dbMotion', blank=True, help_text=b'Defines the dbMotion logo image that will be displayed in the report.<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><b>Note:</b> Only .gif files are supported. The recommended size is: 120x40 px. The size cannot exceed 220x60 px.', null=True, verbose_name=b'dbMotion Logo')),
                ('MrnText', models.CharField(default=b'MRN', help_text=b'Defines the caption used for the Patient Identifier field in the report header. For example, MRN or PHIN.<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><i>Default: MRN</i>', max_length=60, verbose_name=b'Patient identifier caption in reports')),
                ('rtf_report_remove_reference_fields', models.BooleanField(default=False, help_text=b'Determines whether to remove internal links in RTF documents, because these internal links occasionally produce error messages in the document upon conversion to PDF.<br/>True: Removes RTF internal links. The links will still exist in the PDF file as text.<br/>False: Does not remove RTF internal links.<br/><i>Default: False</i>', verbose_name=b'Remove internal links from RTF documents')),
            ],
            options={
                'history_meta_label': 'Reporting',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CAGDataAccessAuditing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auditing_type', models.IntegerField(default=0, help_text=b'\n        Suspicious activity is any access to the database by non-dbMotion service accounts.<br/>\n        Application authorized users are dbMotion application service accounts.<br/><i>Default: Enable suspicious activity auditing</i>', verbose_name=b'', choices=[(0, b'Enable suspicious activity auditing'), (1, b'Enable suspicious activity and application authorized user auditing'), (999, b'No auditing')])),
                ('suspected_max_storage_size', models.IntegerField(default=500, verbose_name=b'Suspicious activity auditing files maximum storage(in MB)', validators=[django.core.validators.MinValueValidator(50)])),
                ('authorized_max_storage_size', models.IntegerField(default=500, help_text=b'<br/>\n        SQL Server audit files are kept in the file system.<br/> \n        Specify the maximum storage limit to keep disk space use under control.<br/> \n        After the limit reached, SQL Server overwrites the current files.<br/>\n        Default calculated according to expected amount of activity.<br/><i>Default: 500</i>', verbose_name=b'Authorized activity auditing files maximum storage(in MB)', validators=[django.core.validators.MinValueValidator(50)])),
                ('server_principals', models.TextField(default=b'', help_text=b'\n    Users listed are not monitored for suspicious activites.<br/>\n    Use comma seperated list of users in a format domain\\user name, domain\\user name, ...', max_length=500, verbose_name=b'Authorized User Name')),
            ],
            options={
                'history_meta_label': 'CAG Data Access Auditing',
                'verbose_name_plural': 'CAG Data Access Auditing',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CAGDataAccessAuditingPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('help_text_1', models.TextField(default=b'Use this configuration to audit database access.', blank=True)),
            ],
            options={
                'verbose_name': 'CAG Instance Data Access Auditing',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CapsulePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Capsule Service',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CapsuleService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scheduled_time', models.TimeField(verbose_name=b'Start Time (for Daily)')),
                ('end_scheduled_time', models.TimeField(default=None, help_text=b'Note: The EndTime setting enables working time frame control of the capsule service. This time frame controls the working time of the capsule service when processing a large number of capsule generation requests, as expected in the quarterly process.<br/><i>Default: Empty</i>', null=True, verbose_name=b'End Time (for Daily)', blank=True)),
                ('local_folder', models.CharField(default=b'C:\\Capsules', max_length=255, verbose_name=b'Set the archive / local folder for the auto generated Capsules')),
                ('vault_folder', models.CharField(default=b'C:\\Capsules', max_length=255, verbose_name=b'Set the destination folder for auto generated Capsules')),
                ('on_demand_local_folder', models.CharField(default=b'C:\\Capsules\\OnDemand\\CCD_LOCAL', max_length=255, verbose_name=b'Set the local folder for the On Demand Capsules')),
                ('on_demand_vault_folder', models.CharField(default=b'C:\\Capsules\\OnDemand\\CCD_DEST', max_length=255, verbose_name=b'Set the archive / destination folder for the On Demand Capsules')),
                ('num_of_days_to_delete_capsules', models.PositiveIntegerField(default=30, verbose_name=b'Set number of days to delete archive from local folder')),
                ('capsules_paging_size', models.PositiveIntegerField(default=10, verbose_name=b'Set how many capsules can be generated at the same time')),
                ('confidentiality_filter', models.BooleanField(default=False, verbose_name=b'Enable Confidentiality filter to filter confidential data')),
                ('capsule_type', models.IntegerField(default=1, help_text=b'Defines the Capsule Type.<br/>Possible types:<br/>1) Hospital To HMO<br/>2) HMO to HMO<br/><i>Default: Hospital To HMO.</i>', verbose_name=b'Capsule Types', choices=[(1, b'Hospital To HMO'), (2, b'HMO To HMO')])),
                ('outbound_csv_vault_folder', models.CharField(default=None, max_length=255, null=True, verbose_name=b'Set the HMO outbound csv folder', blank=True)),
                ('inbound_csv_vault_folder', models.CharField(default=None, max_length=255, null=True, verbose_name=b'Set the HMO inbound csv folder', blank=True)),
            ],
            options={
                'history_meta_label': 'Capsule Service',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarequalityIntegrationSettingsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable_carequality_integration', models.BooleanField(default=False, help_text=b'Determines whether to enable or disable Carequality Integration.<br/>For detailed implementation instructions, see the IHE Integration Implementation Guide.<br/><i>Default: False</i>', verbose_name=b'Enable Carequality Integration')),
                ('home_community_id', models.CharField(default=b'(Enter your Home Community ID)', help_text=b'Defines the dbMotion Home Community ID (OID) for outbound requests to Carequality.<br/>This value can be obtained from Allscripts Community Configuration Manager (CCM).<br/>The OID format should be: urn:oid:n.n.n.n.n.n. For example: urn:oid:2.16.840.1.113883.3.57.1.3.0.2.<br/><i>Default: Empty</i>', max_length=400, verbose_name=b'Home Community ID:', blank=True)),
                ('certificate_thumptrint', models.CharField(default=b'(Enter your Certificate Thumbprint)', help_text=b'Defines the Certificate Thumbprint for HTTPS connections to Allscripts Brokering Responding Gateway.<br/>The Certificate must be downloaded from the Allscripts Community Configuration Manager (CCM) and installed on the Application server.<br/><i>Default: Empty</i>', max_length=400, verbose_name=b'Certificate Thumprint:', blank=True)),
                ('patient_discovery_endpoint', models.CharField(default=b'https://brokeringrespondinggateway- /iti55/<CQ Participant OID>/outbound', help_text=b'URL to Allscripts Brokering Responding Gateway for IHE Transaction ITI-55 Cross Gateway Patient Discovery (XCPD).<br/><i>Default: https://brokeringrespondinggateway- /iti55/&lt;CQ Participant OID&gt;/outbound</i>', max_length=400, verbose_name=b'Patient Discovery Endpoint:', blank=True)),
                ('find_documents_endpoint', models.CharField(default=b'https://brokeringrespondinggateway- /iti38/<CQ Participant OID>/outbound', help_text=b'URL to Allscripts Brokering Responding Gateway for IHE Transaction ITI-38 Cross Gateway Query.<br/><i>Default: https://brokeringrespondinggateway- /iti38/&lt;CQ Participant OID&gt;/outbound</i>', max_length=400, verbose_name=b'Find Documents Endpoint:', blank=True)),
                ('retrieve_document_endpoint', models.CharField(default=b'https://brokeringrespondinggateway- /iti39/<CQ Participant OID>/outbound', help_text=b'URL to Allscripts Brokering Responding Gateway for IHE Transaction ITI-39 Cross Gateway Retrieve.<br/><i>Default: https://brokeringrespondinggateway- /iti39/&lt;CQ Participant OID&gt;/outbound</i>', max_length=400, verbose_name=b'Retrieve Document Endpoint:', blank=True)),
            ],
            options={
                'history_meta_label': 'Set Carequality Integration Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarequalityIntegrationSettingsPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Set Carequality Integration Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CCDADisplay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_mode', models.IntegerField(default=0, help_text=b'Determines in which Mode the CCDA is displayed when it is opened in the CV, CVA and PV.<br>PDF: Displayed as a PDF using the Allscripts PDF Converter Web API<br>CVE: CCDA is opened with the Interactive CVE (CVE is Allscripts Clinical View Engine)<br/><i>Default: PDF</i>', verbose_name=b'CCDA Display Mode', choices=[(0, b'PDF'), (1, b'CVE')])),
                ('cve_renew_certificate', models.CharField(help_text=b'Defines the Certificate Thumbprint for the Retrieval Key. The Certificate must be downloaded from the Allscripts Community Configuration Manager (CCM) and installed on the Application server.', max_length=500, verbose_name=b'Certificate', blank=True)),
                ('environment', models.IntegerField(default=1, help_text=b'Defines the community library environments.<br/><i>Default: Testing</i>', verbose_name=b'Environment', choices=[(0, b'Testing'), (1, b'Production')])),
                ('source_system', models.CharField(default=b'', help_text=b'Defines the dbMotion project OID.', max_length=500, verbose_name=b'Source System', blank=True)),
                ('service_location', models.IntegerField(default=0, help_text=b'Determines the type of service that will be used.<br>Cloud: Allscripts remote cloud service<br>On premise: Customer local service<br/><i>Default: Cloud</i>', verbose_name=b'Service location', choices=[(0, b'Cloud'), (1, b'On premise')])),
                ('retrieval_key_cloud_service', models.CharField(default=b'', help_text=b'URL for retrieval key for Cloud service', max_length=500, verbose_name=b'Retrieval key for Cloud service')),
                ('CCDA_export_continuity_of_care_document', models.CharField(default=b'https://taas1000-prod-us.csg.az.allscriptscloud.com/transform/CCDA_R21_ContinuityOfCareDocument/', help_text=b'URL for CCDA export Continuity of Care Document', max_length=500, verbose_name=b'CCDA export Continuity of Care Document')),
                ('CCDA_export_discharge_summary', models.CharField(default=b'https://taas1000-prod-us.csg.az.allscriptscloud.com/transform/CCDA_R21_DischargeSummary/', help_text=b'URL for CCDA export Discharge Summary', max_length=500, verbose_name=b'CCDA export Discharge Summary')),
                ('CCDA_export_referral_notes', models.CharField(default=b'https://taas1000-prod-us.csg.az.allscriptscloud.com/transform/CCDA_R21_ReferralNote/', help_text=b'URL for CCDA export Referral Notes', max_length=500, verbose_name=b'CCDA export Referral Notes')),
                ('CCDA_export_unstructured_document', models.CharField(default=b'https://taas1000-prod-us.csg.az.allscriptscloud.com/transform/CCDA_R21_UnstructuredDocument/', help_text=b'URL for CCDA export Unstructured Document', max_length=500, verbose_name=b'CCDA export Unstructured Document')),
                ('Cve_document_conversion', models.CharField(default=b'https://viewer-prod-us.csg.az.allscriptscloud.com', help_text=b'URL for CVE document conversion', max_length=500, verbose_name=b'CVE document conversion')),
                ('Pdf_document_conversion', models.CharField(default=b'https://cdatopdf-prod-us.csg.az.allscriptscloud.com/api/convert', help_text=b'URL for PDF document conversion', max_length=500, verbose_name=b'PDF document conversion')),
                ('vaas_document_conversion', models.CharField(default=b'', help_text=b'URL for VAAS document conversion. This service is only supported for the Cloud and will work via Cloud regardless if On premise option is selected.', max_length=500, verbose_name=b'VAAS document conversion')),
                ('transformation_cloud_service', models.CharField(default=b'', help_text=b'URL for dbMotion transformation cloud service', max_length=500, verbose_name=b'Transformation cloud service', blank=True)),
                ('transformation_service_subscription', models.CharField(default=b'', help_text=b'Subscription key for dbMotion transformation cloud service', max_length=500, verbose_name=b'Transformation service subscription', blank=True)),
                ('customer_name', models.CharField(default=b'dbMotion', help_text=b'Defines the dbMotion customer name.', max_length=500, verbose_name=b'Customer Name')),
            ],
            options={
                'history_meta_label': 'CCDA Display and Report',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChangesHistory',
            fields=[
                ('logentry_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='admin.LogEntry')),
            ],
            options={
                'help_text': 'The search is available for the following fields: Screen, Page Model Name and Action.',
                'verbose_name': 'Change Action',
            },
            bases=('admin.logentry',),
        ),
        migrations.CreateModel(
            name='ClinicalCodeDisplay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business_aspect', models.CharField(max_length=40)),
                ('business_table', models.CharField(help_text=b'The business table within the business aspect.', max_length=40)),
                ('code_name', models.CharField(help_text=b'The business codes.', max_length=40)),
                ('vocabulary_domain', models.CharField(help_text=b'The relevant Vocabulary domain of the codes.', max_length=40)),
                ('display_as', models.CharField(default=b'Preferred|Baseline|Local|Text', max_length=50, null=True, help_text=b'Change the priority order by dragging and dropping the text in the required field.', blank=True)),
            ],
            options={
                'history_meta_label': 'Clinical Code Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClinicalCodeDisplayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Clinical Code Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClinicalDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('help_text_1', models.TextField(default=b'This is a help text section No. 1', blank=True)),
                ('help_text_2', models.TextField(default=b'This is a help text section No. 2', blank=True)),
                ('help_text_3', models.TextField(default=b'This is a help text section No. 3', blank=True)),
                ('clinical_view_name', models.CharField(max_length=100, blank=True)),
                ('report_name', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClinicalDomainAllergies',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainDemographics',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainDiagnoses',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainDocuments',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainEncounterDetails',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainEncounters',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainImaging',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainImmunizations',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainLaboratory',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainLabResults',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainLabResultsHistory',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainMedications',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainPathologies',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainPlv',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainProblems',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainProcedures',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ClinicalDocument_DD_ResetPasskey', models.CharField(help_text=b'Defines the text displayed in the Patient View that explains how the patient can reset the Disclosure Directive password (maximum length of 300 Characters).<br>(For example: To reset keyword, the patient should call XXX-XXX-XXXX.)<br/><i>Default: empty</i>', max_length=300, null=True, verbose_name=b'Reset Keyword')),
                ('ClinicalDocument_DD_ProviderPolicy_URL', models.CharField(help_text=b'Defines the URL (or network drive) of the providers policies help page.<br/><i>Default: empty</i>', max_length=500, null=True, verbose_name=b'Providers Policies Help Page')),
                ('ClinicalDocument_DD_PatientPolicy_URL', models.CharField(help_text=b'Defines the URL (or network drive) of the patients policies help page.<br/><i>Default: empty</i>', max_length=500, null=True, verbose_name=b'Patients Policies Help Page')),
                ('ClinicalDocument_DD_OverrdieWithoutConsentOrgPolicy_URL', models.CharField(help_text=b"Defines the URL (or network drive) of the Organization's Override Without Consent Policy Page.<br/><i>Default: empty</i>", max_length=500, null=True, verbose_name=b'Override Without Consent Policy')),
                ('help_1', models.TextField(null=True, verbose_name=b'help', blank=True)),
                ('help_2', models.TextField(null=True, verbose_name=b'help', blank=True)),
                ('show_cancelled_display', models.BooleanField(default=True, verbose_name=b'"Show Cancelled" is displayed')),
                ('show_cancelled_selected', models.BooleanField(default=True, verbose_name=b'"Show Cancelled" is selected')),
                ('help_3', models.TextField(null=True, verbose_name=b'help', blank=True)),
                ('grouped_by_display', models.BooleanField(default=True, verbose_name=b'"Grouped By" option is displayed')),
                ('grouped_by_selected', models.BooleanField(default=True, verbose_name=b'"Grouped By" option is selected')),
                ('code_system_name_display', models.IntegerField(default=0, verbose_name=b'CodeSystem name display within the Code column', choices=[(0, b'Display the CodeSystem Name only as a tooltip when the user hovers the cursor over the Code column'), (1, b'Display the CodeSystem Name in parentheses attached to the Code within the Code column')])),
                ('display_not_inactive', models.BooleanField(default=False, verbose_name=b'Display only medications whose status is active')),
                ('display_grid', models.BooleanField(default=True, verbose_name=b'Display Location History Grid')),
                ('show_record_count', models.BooleanField(default=True, verbose_name=b'The domain grid title bars display messages')),
                ('Imaging_DisplayImagingMetaData', models.BooleanField(default=False, verbose_name=b'The Imaging Details are displayed on the top of the imaging report')),
                ('Imaging_ShowEmptyFolders', models.BooleanField(default=False, verbose_name=b'Show Imaging folder even if it is empty')),
                ('Documents_CompletionStatusAdded', models.BooleanField(default=False, verbose_name=b'The presentation of the Document Completion Status is added to both the Preview and the Report (with title Report Status).')),
                ('LabEvents_DefaultGrouping', models.IntegerField(default=0, help_text=b'Determines the default grouping of Lab events.<br><i>Default: By order of events</i>', verbose_name=b'Default grouping of Lab events', choices=[(0, b'By order of events'), (1, b'By collection date'), (2, b'By the latest results')])),
                ('ClinicalDocument_ShowEmptyFolders', models.BooleanField(default=False, help_text=b'Determines whether to show a Clinical Document folder even if it is empty.<br/>If True, the empty folder is displayed.<br/>If False, the empty folder is not displayed.<br/><i>Default: False</i>', verbose_name=b'Show a Clinical Document folder even if it is empty')),
                ('Laboratory_UseWrappedText', models.BooleanField(default=True, help_text=b'Determines whether the full results and comments are displayed as wrapped.<br/>If True, the full result/comment is presented wrapped.<br/>If False, the results and comments are displayed in a single line with 3 dots.<br/><i>Default: True</i>', verbose_name=b'Use wrapped text')),
                ('Laboratory_OpenMicroReportForMicroEvent', models.BooleanField(default=False, help_text=b'Determines whether to display the Microbiology lab report instead of the Lab Results Clinical View if the lab result is a microbiology lab (A microbiology lab is identified by the code 2.16.840.1.113883.6.1|MICRO). In that case, the report is available from all the places that the Lab Results clinical view is accessed for regular results (meaning, from Labs, from Labs in Summary Page, etc.) and by clicking on the report icon in the Labs clinical view.<br/><i>Default: False</i>', verbose_name=b'Open Microbiology Report   ')),
                ('LabResults_FormatText', models.BooleanField(default=False, help_text=b'Determines whether the Lab Results/Remarks font is changed to be formatted text (Courier New). If so, the text has the same alignment regardless of the letters that are used.<br/><em>Default: False</em>', verbose_name=b'Change Lab Results/Remarks to be formatted text')),
                ('demography_details_type', models.IntegerField(default=7, help_text=b"Determines the mode that the patient's contact details are displayed in the Demographics clinical view.<br/>If the value is 'Leading record contacts', only the leading record contacts information is displayed. Additional information can be accessed only by clicking the More icon.<br/>If the value is 'All contacts', the leading record contacts information is displayed and also all additional contacts are displayed.<br/><i>Default: All contacts</i>", choices=[(0, b'Leading record contacts'), (7, b'All contacts')])),
                ('ClinicalDocument_ShowExternalDocumentsLabel', models.CharField(default=b'Show External Documents', max_length=50, blank=True, help_text=b"Determines the text to show for all External Documents on Disclaimer after the fixed text<br/><i>Default: 'Show External Documents' and Fixed text: 'You are about to access patient documents from external system(s) for the following reasons:'</i>", null=True, verbose_name=b'Show External Documents Checkbox Label')),
                ('ClinicalDocument_BringExtDocsOnShowAll', models.BooleanField(default=True, help_text=b'Determines whether external documents are retrieved and shown with other documents - when the user selects to Show All. <br/><b>True: </b>The External Documents checkbox will be selected automatically, so external documents will be retrieved and displayed with other documents. <br/><b>False: </b>The External Documents checkbox will not be selected automatically, so external documents will be not retrieved and displayed.<br/><i>Default: True</i>', verbose_name=b'Retrieve External Documents on Show All')),
                ('ClinicalDocument_ShowExternalDocumentsLabelForAgent', models.BooleanField(default=False, help_text=b'Determines whether an External Document disclaimer will be displayed in EHR Agent when the user wants to access External Documents.<br><br><b>True:</b><br>In the EHR Agent a disclaimer message will be displayed before displaying the list of External Documents to the user. The user is expected to approve the disclaimer.  The disclaimer will concatenate a fixed text with a configurable text.<br>Fixed Disclaimer Text:"You are about to access patient documents from external systems for the following reason(s):"<br>Configured Disclaimer Text: This will be the same text configured for the label of the Show External Documents checkbox in the Clinical Viewer. (The label is configured in the Show External Documents Checkbox Label configuration.) The text will be the same for both applications.<br>This configured text will also be displayed above the list of External Documents in the EHR Agent.<br><br><b>False:</b><br>The EHR Agent will not display the disclaimer text and will not display the configured text above the External Documents list. However, this text, if configured for Clinical Viewer External Documents checkbox, will be displayed in the Clinical Viewer.<br/><i>Default: False</i>', verbose_name=b'External Documents Display')),
                ('ConditionTypeToDisplay', models.IntegerField(default=1, help_text=b'Determines whether the Diagnosis grid or Problems grid is displayed in the Summary clinical view.<br/><i>Default: Display Problems grid</i>', verbose_name=b'Displaying Diagnosis and Problems grid', choices=[(0, b'Display Diagnosis grid'), (1, b'Display Problems grid'), (2, b'Do not display either')])),
                ('demography_display_insurances_grid', models.BooleanField(default=True, help_text=b'Determines whether the Insurance grid is visible in the Demographics clinical view.<br/><i>Default: True</i>', verbose_name=b'Insurance grid is displayed')),
                ('ClinicalDocument_DocPreviewFontFamily', models.CharField(default=b'Courier New', help_text=b'Defines the Font Type in the preview of Clinical Documents.<br/><i>Default: Courier New</i>', max_length=60, verbose_name=b'Clinical Document preview font type', choices=[(b'Arial', b'Arial'), (b'Courier New', b'Courier New')])),
                ('ClinicalDocument_SortTypeByDesignation', models.BooleanField(default=True, help_text=b'Determines whether to sort documents by designation or by domain code.<br/><i>Default: True</i>', verbose_name=b'Sort Clinical Documents by designation')),
                ('LabResultHistory_DisplaySearch', models.BooleanField(default=False, help_text=b'Define whether to display the Lab search option in the Lab results history page.<br/><i>Default: False</i>', verbose_name=b'Display Lab Search')),
                ('ClinicalDocument_DocsTreePaneWidth', models.IntegerField(default=33, help_text=b'Defines the width of the Documents pane (in percentage) in relation to the Preview pane. The value range is 33%-70%.<br/><i>Note: The horizontal width will be set after the user opens the Clinical Documents page. There is no need to click on External Documents.</i><br/><i>Default: 33%</i>', verbose_name=b'Documents Tree Pane Width', validators=[django.core.validators.MinValueValidator(33), django.core.validators.MaxValueValidator(70)])),
                ('ClinicalDocument_ExtDocsTreePaneHeight', models.IntegerField(default=35, help_text=b'Defines the height of the External Documents area (in percentage) within the entire area of the Documents pane (including Internal and External Documents areas). The remainder of the Documents pane contains the internal Documents area (meaning, 100% minus this value). The value range is 0%-100%.<br/><i>Note: This configuration takes effect only after External Documents is selected.</i><br/><i>Default: 35%</i>', verbose_name=b'External Documents Tree Pane Height', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('ExteranlDocument_Default_Grouping', models.CharField(help_text=b'Defines the default grouping method for the External Documents domain in Clinical Viewer.<br>Note that this does not affect the "Internal Documents" grouping in this domain.<br/><i>Default: By Date</i>', max_length=60, null=True, verbose_name=b'External Documents Default Grouping', choices=[(b'Type', b'By Type'), (b'Author', b'By Author'), (b'Date', b'By Date'), (b'Facility', b'By Facility')])),
                ('disclaimer', models.BooleanField(default=False, help_text=b'Determines whether a disclaimer will be displayed in Patient view when the user wants to access any External Documents category.<br/><b>True: </b><br/>In the external documents category a disclaimer message will be displayed before displaying the list of External Documents to the user. The user is expected to approve the disclaimer. The disclaimer will concatenate a fixed text with a configurable text.<br/><b>False:</b><br/>The application will not display the disclaimer in any external documents category.<br/>Default: False.', verbose_name=b'Disclaimer Required')),
            ],
            options={
                'history_meta_label': 'Display Options',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClinicalDomainSummary',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalDomainVitals',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='ClinicalViewerGeneral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DefaultDomain', models.CharField(default='', help_text=b'Defines the domain that opens by default after login.<br/><i>Default: N/A</i>', max_length=100, verbose_name=b'Domain name', blank=True)),
                ('IsOtherGroupExpanded', models.BooleanField(default=True, help_text=b'Determines whether, in grouping scenarios, the Others group of unspecified medical information/results is always expanded.<br/>If True, this data is always expanded.<br/>If False, the  data is always collapsed.<br/>*Note: this configuration applies to Medications, Allergies, Problems, Diagnosis, and Procedures.<br/><i>Default: True</i>', verbose_name=b'Others group is always expanded')),
                ('IsTextWrappingUsedInCD', models.BooleanField(default=True, help_text=b'Defines whether text wrapping is used in a Clinical Document, in Clinical Documents and Imaging clinical domains.<br/><i>Default: True</i>', verbose_name=b'Text wrapping is used in a Clinical Document')),
                ('IsShowMessageSectionDisclaimer', models.BooleanField(default=False, help_text=b'Determines whether to show the message section of the disclaimer in the clinical view status bar.<br/><i>Default: False</i>', verbose_name=b'Show the message section of the disclaimer in the clinical view status bar.')),
                ('IsShowLinkSectionDisclaimer', models.BooleanField(default=False, help_text=b'Determines whether to show the link section of the disclaimer in the clinical view status bar<br/><i>Default: False</i>', verbose_name=b'Show the link section of the disclaimer in the clinical view status bar')),
                ('UrlOnLinkSectionDisclaimer', models.CharField(default=b'/dbMotionInformationServices/dbMotionInformationPage.aspx', help_text=b'Defines the URL used when clicking on the link section of the disclaimer.<br/>The default URL: The System Info Page.<br/><i>Default: /dbMotionInformationServices/dbMotionInformationPage.aspx</i>', max_length=500, verbose_name=b'Disclaimer link address', blank=True)),
                ('UserNameDisplayOptions', models.CharField(default=b'{0}, |{1}, |{2}|{3}, |{4}, |{5}', help_text=b'Defines the format for the parts of the user&apos;s name displayed in the Clinical Viewer User Header.<br/>0 = Title<br/>1 = First Name<br/>2 = Last Name<br/>3 = TitleUnmanaged<br/>4 = FirstNameUnmanaged<br/>5 = LastNameUnmanaged<br/><i>Default: {0}, |{1}, |{2}|{3}, |{4}, |{5}</i>', max_length=100, verbose_name=b'User name format', validators=[dbmconfigapp.models.clinical_viewer_general.validate_name_format])),
                ('CustomerLogoFileName', models.CharField(default=b'', help_text=b'Defines the file name of the customer&#39;s logo displayed in the Clinical Viewer login screen. The logo file should manually be saved to:<br/>C:\\Program Files\\dbMotion\\Web\\Sites\\WebApp35\\SiteImages\\logos<br/>This configuration applies only in the case that the "Logos display" selection above includes the customer logo.<br/>The following are the logo image type and size requirements:<br/>Type: gif<br/>Height: 60px<br/>Width: 365px<br/><br/>Note: The logo file name should include the extension<br/><i>Example: customer.gif</i><br/><i>Default: No default value</i>', max_length=100, verbose_name=b'Customer Logo file name', blank=True)),
                ('WebApplicationName', models.CharField(default=b'dbMotionClinicalViewer', help_text=b'Defines the name of Clinical View Web Application.<br/><i>Default: dbMotionClinicalViewer</i>', max_length=100, verbose_name=b'Web Application Name')),
                ('DefaultLogoFile', models.ImageField(default=b'', storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), upload_to=b'ClinicalViewer/Logo', blank=True, help_text=b'Defines the default logo presented in the Clinical Viewer.<br/>The following are the logo image type and size requirements:<br/>Type: gif<br/>Height: 28px<br/>Width: 84px<br/><i>Default: No default value</i>', null=True, verbose_name=b'Logo File')),
                ('LoginScreenLogosOptions', models.IntegerField(default=0, help_text=b'<i>Default: In the upper area of the login screen, the dbMotion logo is displayed and the lower area is empty.</i>', verbose_name=b'Logos display', choices=[(0, b'In the upper area of the login screen, the dbMotion logo is displayed and the lower area is empty.'), (1, b'In the upper area of the login screen, the customer logo is displayed and the lower area displays the dbMotion logo. Please upload the customer logo file below.'), (2, b'In the upper area of the login screen, the customer logo is displayed and the sentence "Powered by dbMotion" is displayed beneath the customer logo. The lower area of the login screen is empty. Please upload the customer logo file below and define the position of the sentence.')])),
                ('CreditTitlePosition', models.IntegerField(default=120, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(250)], max_length=3, blank=True, help_text=b'Defines the horizontal position of the "Powered by dbMotion" sentence relative to the left corner of the login logo container<br/>The default horizontal position is in the center of the logo container, 120.<br/>0 will position the sentence on the far left side of the login logo container.<br/>250 will position the sentence on the far right side of the login logo container.<br/>Possible values: 0-250<br/><i>Default: 120</i>', null=True, verbose_name=b'Position of "Powered by dbMotion" sentence')),
            ],
            options={
                'verbose_name': 'Clinical Viewer General',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClinicalViewerGeneralPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Clinical Viewer General',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollaboratePatientSearchProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('MrnSystemSelectorMaxDropItems', models.IntegerField(default=6, help_text=b'Defines the maximum number of items that can be displayed in the standard MRN System Selector dropdown list. If the maximum value is exceeded, the enhanced MRN System Selector dropdown list is provided to display all the items on the list.<br/>The possible values are 2-100<br/><em>Default: 6</em>', verbose_name=b'Max items displayed in the standard MRN System Selector dropdown list', validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(100)])),
                ('MrnSystemSelectorMaxColumnCount', models.IntegerField(default=2, help_text=b'Defines the maximum number of columns that can be displayed in the MRN System Selector dropdown list.<br/>The possible values are 1-5<br/><em>Default: 2</em>', verbose_name=b'Max columns displayed in the MRN System Selector dropdown list', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('MrnSystemSelectorIsSortingEnabled', models.BooleanField(default=True, help_text=b'Supported by Clinical Viewer only.<br/>Determines whether the MRN System Selector dropdown list is sorted.<br/>If true, the list is sorted in ascending order.<br/>If false, the list is not sorted and the displayed order is taken from the configuration of the systems.<br/><em>Default: True</em>', verbose_name=b'MRN System Selector is sorted in ascending order')),
                ('MrnSystemSelectorIsEmptyItemEnabled', models.BooleanField(default=True, help_text=b'Supported by Clinical Viewer only.<br/>Determines whether the MRN System Selector dropdown list is enabled if it is empty.<br/>If true, the application adds an item titled Empty and if a user selects this item, the selected system is null.<br/>If false, the list is disabled when empty.<br/><em>Default: True</em>', verbose_name=b'MRN System Selector is enabled if it is empty')),
                ('PatientSearch_IsDirectEnterPatientFile', models.BooleanField(default=True, help_text=b'Determines whether when the search results via MRN return a cluster, the system automatically enters the patient&#39;s file.<br/>If False, the system displays the cluster and the user can then choose to enter the patient&#39;s file.<br/>In External Mode access, this value is always True<br/>Note : Affects only Clinical Viewer and Patient View<br/><em>Default: True</em>', verbose_name=b"Enter the patient's file automatically when the search results via MRN return a cluster")),
                ('PatientSearch_IsDirectEnterPatientFile_Demographics', models.BooleanField(default=True, help_text=b'Determines whether when the search results via demographics return a cluster, the system automatically enters the patient&#39;s file.<br/>If False, the system displays the cluster and the user can then choose to enter the patient&#39;s file.<br/>In External Mode access, this value is always True<br/>Note : Affects only Clinical Viewer<br/><em>Default: True</em>', verbose_name=b"Enter the patient's file automatically when the search results via Demographics return a cluster")),
                ('PatientSearch_IsDirectEnterPatientFile_Demographics_MinScore', models.IntegerField(default=140, help_text=b"Determines the minimum score, to enter the patient file automatically following a demographic search, when a single cluster is returned. If the score is lower, the system displays the cluster, and the user can then choose to enter the patient's file.<br/>Note: Affects only Clinical Viewer, including External Mode access.<br/><em>Default: 140</em>", verbose_name=b'Minimum score', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)])),
                ('LeadingPatientRecordPolicy', models.CharField(default=b'', help_text=b'Supported by Clinical Viewer only.<br/>Determines the Leading Patient Record (including which MRN is displayed in the Patient Details header and in the Demographics clinical view) in response to a Patient Search by MRN.<br/>This includes the Leading Patient Record that opens in the following cases:<br/>&nbsp;&nbsp;&nbsp;&nbsp;- When launching the Clinical Viewer from an EHR.<br/>&nbsp;&nbsp;&nbsp;&nbsp;- When launching the Clinical Viewer from EHR Agent or Collaborate.<br/>&nbsp;&nbsp;&nbsp;&nbsp;- When searching for the patient by MRN.<br/><b>By default,</b> the leading record chosen will be the record with the same MRN that the user entered in the Patient Search.<br/>The following configurable options enable the customer to determine cases in which the Leading Patient Record will be the first index returned by the MPI.<br/>In these cases, the MPI might determine a Leading Patient Record with a different MRN than the MRN used in the Patient Search.<br/>The following configurable options are available. In all of the following cases, the CV will choose the first record returned by the MPI regardless of the MRN used in the Patient Search or in the launching application.<br/><b>EMR1|EMR2 =</b> In the case of Clinical Viewer launch from <b>only these defined client applications.</b> If the CV is launched from any undefined application, the behavior is the default behavior.<br/><b>All =</b> In the case of Clinical Viewer launch from any (all) existing client applications.<br/><b>Empty =</b> In the case of an MRN search when the clientApplicationId was not sent by the EHR or launching application (as configured in the Launch API). This includes also a case where the CV is launched by an undefined application (for example if a user opened a browser and accessed the CV login page).<br/><em>Default: No default value</em>', max_length=500, verbose_name=b'Leading patient record policy', blank=True)),
                ('System_label', models.CharField(default=b'System', max_length=120, verbose_name=b'Enter the label for System', blank=True)),
                ('MRN_label', models.CharField(default=b'MRN', max_length=120, verbose_name=b'Enter the label for MRN', blank=True)),
                ('MinSQQ', models.IntegerField(default=50, help_text=b'Defines the minimum MPI SQQ score (quality of a search query) from which VIA will return records.<br/>Before submitting the patient search query, it must undergo a quality check to minimize the possibility of a large number of search results.<br/>The SQQ score is determined by calculating the sum of weights of the various search attributes that participate in the query.<br/>Only if the SQQ score is equal to or greater than the MinSQQ value, the search query passes the quality check.<br/><em>Default: 50</em>', verbose_name=b'Minimum SQQ score', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('ContinueSearchAfterSQQCheckFailure', models.BooleanField(default=False, help_text=b'Determines whether if the configured MinSQQ score is too low, the user is given an option to continue the search.<br/>If True, a message is displayed enabling the user to continue the search or cancel it.<br/>If false, a message informs the user that the score is too low and the search is discontinued.<br/><em>Default: False</em>', verbose_name=b'Continue search although SQQ score is too low')),
                ('DemographicSearch_AutoEnter', models.IntegerField(blank=True, help_text=b"This configuration determines when the system will auto enter into a patient's file using demographic search.<br/>Auto enter, using demographic search, happens only when the search result's return one cluster and the OOB strength of the search fields is more than the strength defined in this configuration.<br/>If Empty, the system displays the cluster and the user can then select to enter the patient's file. This configuration only allows numeric values.<br/><b>Note :</b> Affects only Patient View, stand alone and Launch API modes.<br/><em>Default: Empty</em>", null=True, verbose_name=b"Enter the patient's file automatically using Demographic search", validators=[django.core.validators.MinValueValidator(1)])),
                ('PatientSearch_LeadingPatientRecordPolicy', models.BooleanField(default=False, help_text=b'Determines leading index if VIA response does not have searched MRN and source. The leading index is selected based on configuration:<br/>False - Use the same MRN from a different source, else first index from the VIA response is selected.<br/>True - Use the first index from VIA response.<br/><em>Default: False</em>', verbose_name=b'Leading patient record policy (When the searched MRN and source is not found)')),
            ],
            options={
                'history_meta_label': 'Patient Search',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('verbose_name', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Culture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Define a new language for the user interface.', max_length=30, verbose_name=b'Additional Languages')),
                ('readonly', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Language',
                'history_meta_label': 'Language list',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CurrentCulture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Language',
                'history_meta_label': 'Language list',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CVCCDADisplayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'CCDA Display, Report and Data Export',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvPatientDisplayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Patient Display',
                'history_meta_label': 'Clinical Viewer Patient Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CVReportingPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Reporting',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataAccessAuditing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auditing_type', models.IntegerField(default=0, help_text=b'\n        Suspicious activity is any access to the database by non-dbMotion service accounts.<br/>\n        Application authorized users are dbMotion application service accounts.<br/><i>Default: Enable suspicious activity auditing</i>', verbose_name=b'', choices=[(0, b'Enable suspicious activity auditing'), (1, b'Enable suspicious activity and application authorized user auditing'), (999, b'No auditing')])),
                ('suspected_max_storage_size', models.IntegerField(default=500, verbose_name=b'Suspicious activity auditing files maximum storage(in MB)', validators=[django.core.validators.MinValueValidator(50)])),
                ('authorized_max_storage_size', models.IntegerField(default=dbmconfigapp.models.operational_manager.GetCDRAuthorizedUsersSize, help_text=b'<br/>\n        SQL Server audit files are kept in the file system.<br/> \n        Specify the maximum storage limit to keep disk space use under control.<br/> \n        After the limit reached, SQL Server overwrites the current files.<br/>\n        Default calculated according to expected amount of activity.', verbose_name=b'Authorized activity auditing files maximum storage(in MB)', validators=[django.core.validators.MinValueValidator(50)])),
                ('server_principals', models.TextField(default=b'', help_text=b'\n    Users listed are not monitored for suspicious activites.<br/>\n    Use comma seperated list of users in a format domain\\user name, domain\\user name, ...', max_length=500, verbose_name=b'Authorized User Name')),
            ],
            options={
                'history_meta_label': 'CDR Data Access Auditing',
                'verbose_name_plural': 'CDR Data Access Auditing',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataAccessAuditingPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('help_text_1', models.TextField(default=b'Use this configuration to audit database access.', blank=True)),
            ],
            options={
                'verbose_name': 'CDR Instance Data Access Auditing',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'Elements (Vocabulary Domain Code)', blank=True)),
                ('enable', models.BooleanField(default=True, help_text=b'Determines whether or not the column is displayed.', verbose_name=b'Enable')),
                ('page_width', models.FloatField(help_text=b"Defines the column width, as a percentage of the screen's width. The sum of weight of all visible columns should be equal to 100% or higher.", null=True, verbose_name=b'Column Width')),
                ('default_width', models.FloatField(null=True, verbose_name=b'Default Column Width')),
                ('report_width', models.FloatField(help_text=b"Defines the report column width, as a percentage of the screen's width. The sum of weight of all visible columns should be strongly equal to 100%.", null=True, verbose_name=b'Report Column Width')),
                ('default_report_width', models.FloatField(null=True, verbose_name=b'Default Report Column Width')),
                ('order', models.IntegerField(help_text=b'Determines the order of the column in the grid', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('clinical_view_name', models.CharField(max_length=100, blank=True)),
                ('report_field_name', models.CharField(max_length=100, blank=True)),
                ('grid_name', models.CharField(max_length=100, blank=True)),
                ('report_name', models.CharField(max_length=100, blank=True)),
                ('hide_uom', models.BooleanField(default=False, help_text=b'Defines the Vital Signs measurement in which the UOM (Unit of Measurement) is hidden (not displayed), by default.\nDefault: BloodPressure, HeartRate\nThis configuration applies to Clinical Viewer and EHR Agent.', verbose_name=b'Hide the UOM')),
                ('concatenate_values', models.BooleanField(default=False, help_text=b'Defines which Vitals Measurements will be displayed as concatenated. For example: 65 kg 50 g or 65.5 kg\nDefault: BodyWeight, BodyHeight.\nThe Blood Pressure (BP) concatenation business rule is as follows:\nIf a BP Measurement event includes a combined BP Measurement value, display the combined value and do not display separate systolic and diastolic measurements.\nIf a BP Measurement event does not include a combined BP Measurement value and includes both systolic and diastolic measurements, display the concatenated value as systolic/diastolic.\nThis configuration applies to Clinical Viewer and EHR Agent.', verbose_name=b'Concatenate Values')),
                ('_info', models.CharField(max_length=60, null=True, blank=True)),
            ],
            options={
                'history_meta_label': 'Grid Display Options',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AllergiesDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Allergies grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='DataExportCCDADisplayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'CCDA Display and Data Export',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DbFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('data', dbmconfigapp.models.db_files.BlobField()),
                ('size', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DemographicsDetailsDEGrid',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Demographics Details Grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='DemographySearchFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('demo_search_field_label', models.CharField(max_length=120, verbose_name=b'Label')),
                ('max_chars', models.IntegerField(max_length=120, verbose_name=b'Maximum Characters', validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'Demographic Search Field',
                'history_meta_label': 'Demographic Search Fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiagnosesDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Diagnoses grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='DiagnosisDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Diagnosis grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='DirectMessagingAcdm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enableSendingViaAcdm', models.BooleanField(default=True, help_text=b'Determines whether sending TOC via ACDM is enabled.<br/>If True, the following parameters are mandatory.<br/>If False, Sending TOC assumes direct MedAllies connectivity.<br/>Note: For a detailed description of TOC implementation see "IHE Integration Implementation Guide".<br/><i>Default: False</i>', verbose_name=b'Enable sending TOC via ACDM')),
                ('gatewayUrl', models.CharField(default=b'', help_text=b'Defines the ACDM Gateway URL.<br/><i>Default: URL for Testing (https://directuat.allscriptsclient.com:443/gateway/xdr.svc)</i>', max_length=100, verbose_name=b'ACDM Gateway Url', choices=[(b'https://directuat.allscriptsclient.com:443/gateway/xdr.svc', b'URL for Testing (https://directuat.allscriptsclient.com:443/gateway/xdr.svc)'), (b'https://gateway.acdm.allscriptscloud.com/gateway/xdr.svc', b'URL for Production (https://gateway.acdm.allscriptscloud.com/gateway/xdr.svc)')])),
                ('clientOid', models.CharField(default=b'', help_text=b'Defines the Client OID that was configured in the Allscripts Community Manager.', max_length=500, verbose_name=b'ACDM Client OID', blank=True)),
                ('clientCertificateThumbprint', models.CharField(default=b'', help_text=b'Defines the thumbprint of the ACDM Client Certificate that was previously obtained.<br/>For more details see "IHE Integration Implementation Guide".', max_length=500, verbose_name=b'ACDM Client Certificate Thumbprint', blank=True)),
                ('acdmCommunityName', models.CharField(default=b'', help_text=b'Defines whether to work with a production HISP (e.g. Allscripts Community Direct Messaging) or a staging/testing HISP (e.g. Test Allscripts Community Direct Messaging).', max_length=500, verbose_name=b'ACDM Community Name', blank=True)),
            ],
            options={
                'verbose_name': 'Direct Messaging ACDM',
                'history_meta_label': 'ACDM',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectMessagingAcdmPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'ACDM',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DisclaimerText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=120, verbose_name=b'text')),
                ('culture', models.CharField(max_length=12)),
                ('message_link_text', models.CharField(max_length=60, verbose_name=b'link text')),
            ],
            options={
                'verbose_name': 'Disclaimer text',
                'history_meta_label': 'Disclaimer Texts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Related Documents grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='DocumentSearchBootstrap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Document Search Bootstarp',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentSearchBootstrapProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency_mode', models.IntegerField(default=1, help_text=b'Each insert, update, and delete of a clinical document in the CDR triggers queuing the document in an operational table for Elasticsearch indexing. Specify how often the indexing occurs.<br/>* <b>Continuous</b><br/>* <b> Time frame:</b><br/><i>Default: Continuous.</i>', verbose_name=b'Bootstrap frequency mode:', choices=[(1, b'Continuous'), (2, b'Time Frame')])),
                ('start_scheduled_time', models.TimeField(default=None, help_text=b'Enter a time in format HH:MM:SS, click Now, or click the clock icon to select from a list of start times.<br/><i>Default: Empty</i>', null=True, verbose_name=b'Bootstrap start time:', blank=True)),
                ('end_scheduled_time', models.TimeField(default=None, help_text=b'Enter a time in format HH:MM:SS, click Now, or click the clock icon to select from a list of start times.<br/><i>Default: Empty</i>', null=True, verbose_name=b'Bootstrap end time:', blank=True)),
                ('protected_systems1', models.TextField(default=b'', help_text=b'\n        Specify a list of systems not affected by content requests by the group. Use the pipe symbol [|] as a delimiter between systems.\n    <br/><i>Default: Empty</i>', verbose_name=b'Group #1 protected systems', blank=True)),
                ('protected_systems_rate1', models.IntegerField(blank=True, help_text=b'\n        Define the aggregated rate of content requests to systems from group.\n    <br/><i>Default: Empty</i>', null=True, verbose_name=b'Group #1 aggregated rate (req/min)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('protected_systems2', models.TextField(default=b'', help_text=b'\n        Specify a list of systems not affected by content requests by the group. Use the pipe symbol [|] as a delimiter between systems.\n    <br/><i>Default: Empty</i>', verbose_name=b'Group #2 protected systems', blank=True)),
                ('protected_systems_rate2', models.IntegerField(blank=True, help_text=b'\n        Define the aggregated rate of content requests to systems from group.\n    <br/><i>Default: Empty</i>', null=True, verbose_name=b'Group #2 aggregated rate (req/min)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('unprotected_systems_rate', models.IntegerField(default=8000, help_text=b'\n        Define the maximum standard rate of content requests for unprotected sources. Changing this setting might affect the system.\n    <br/><i>Default: 8000</i>', verbose_name=b'Standard aggregated rate (req/min)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
            ],
            options={
                'verbose_name': 'Document Search Bootstarp',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentSearchGeneral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Document Search General',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentSearchGeneralProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_free_systems_mode', models.IntegerField(default=1, help_text=b'Systems are configured to search content and metadata, or search metadata only. Systems configured for metadata search only do not index content into Elasticsearch, meaning content is not available for searching. This setting specifies which systems to search using metadata only.<br/><b>Note:</b> The setting affects the indexing process, but not the search process, and does not affect documents already indexed in Elasticsearch.<br/>* <b>None:</b> None of the systems are defined to support metadata search only. All systems support both metadata and content search for supported document types.<br/>* <b>Custom:</b>  Systems are defined by the organization to support metadata search only, using the document ID_Root of the clinical document. Use the pipe symbol [|] as a delimiter between systems.<br/>* <b>All:</b>  All systems are defined to support metadata search only.<br/><i>Default: None.</i>', verbose_name=b'Search metadata only mode:', choices=[(1, b'None'), (2, b'Custom'), (3, b'All')])),
                ('content_free_systems', models.TextField(default=b'', help_text=b'\n        Define source systems to metadata search only. Use the pipe symbol [|] as a delimiter between systems. Use the document Id_Root from clinicalDocument table.<br/><b>Note:</b> Changes to this setting does not affect past indexing.\n    <br/><i>Default: Empty</i>', verbose_name=b'Systems to CDR metadata search systems:', blank=True)),
                ('index_free_systems', models.TextField(default=b'', help_text=b'\n        Define source systems to omit during indexing. Use the pipe symbol [|] as a delimiter between systems. Use the document Id_Root from clinicalDocument table.<br/><b>Note:</b> Changes to this setting does not affect past indexing.<br/><i>Default: Empty</i>', verbose_name=b'Systems to omit from index process:', blank=True)),
                ('is_ds_of_cdr_enabled', models.BooleanField(default=False, help_text=b'To conduct a document search, the Elasticsearch engine must index the documents that are loaded in the CDR. In Patient View, this setting enables a document search field in the Documents category.<br/><b>Note:</b> Users must be assigned a security task to conduct a search.<br/><i>Default: False.<br/><br/><br/><br/></i>', verbose_name=b'Enable indexing and searching for CDR clinical documents')),
                ('is_ds_of_external_enabled', models.BooleanField(default=False, help_text=b'To conduct a document search, the Elasticsearch engine must index the documents that are loaded in the External documents repositories. In Patient View, this setting enables a document search field in the External Documents category.<br/><b>Note 1:</b> The search for external documents is supported only on metadata fields.<br/><b>Note 2:</b> Users must be assigned a security task to conduct a search.<br/><i>Default: False.<br/><br/><br/><br/></i>', verbose_name=b'Enable indexing and searching for External clinical documents')),
            ],
            options={
                'verbose_name': 'Document Search General',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentSearchLiveFeeds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Document Search Live-Feeds',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentSearchLiveFeedsProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency_mode', models.IntegerField(default=1, help_text=b'Each insert, update, and delete of a clinical document in the CDR triggers queuing the document in an operational table for Elasticsearch indexing. Specify how often the indexing occurs.<br/>* <b>Continuous</b><br/>* <b> Time frame:</b><br/><i>Default: Continuous.</i>', verbose_name=b'Live-feed frequency mode:', choices=[(1, b'Continuous'), (2, b'Time Frame')])),
                ('start_scheduled_time', models.TimeField(default=None, help_text=b'Enter a time in format HH:MM:SS, click Now, or click the clock icon to select from a list of start times.<br/><i>Default: Empty</i>', null=True, verbose_name=b'Live-feed start time', blank=True)),
                ('end_scheduled_time', models.TimeField(default=None, help_text=b'Enter a time in format HH:MM:SS, click Now, or click the clock icon to select from a list of start times.<br/><i>Default: Empty</i>', null=True, verbose_name=b'Live-feed end time', blank=True)),
                ('protected_systems1', models.TextField(default=b'', help_text=b'\n        Specify a list of systems not affected by content requests by the group. Use the pipe symbol [|] as a delimiter between systems.\n    <br/><i>Default: Empty</i>', verbose_name=b'Group #1 protected systems', blank=True)),
                ('protected_systems_rate1', models.IntegerField(blank=True, help_text=b'\n        Define the aggregated rate of content requests to systems from group. If the rate is over 2000, the group becomes an unprotected source and is threaded together with other sources (that is, not a special group or thread for those systems).\t\t\n    <br/><i>Default: Empty</i>', null=True, verbose_name=b'Group #1 aggregated rate (req/min)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('protected_systems2', models.TextField(default=b'', help_text=b'\n        Specify a list of systems not affected by content requests by the group. Use the pipe symbol [|] as a delimiter between systems.\n    <br/><i>Default: Empty</i>', verbose_name=b'Group #2 protected systems', blank=True)),
                ('protected_systems_rate2', models.IntegerField(blank=True, help_text=b'\n        Define the aggregated rate of content requests to systems from group. If the rate is over 2000, the group becomes an unprotected source and is threaded together with other sources (that is, not a special group or thread for those systems).\t\t\n    <br/><i>Default: Empty</i>', null=True, verbose_name=b'Group #2 aggregated rate (req/min)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('unprotected_systems_rate', models.IntegerField(default=2000, help_text=b'\n        Define the maximum standard rate of content requests for unprotected sources. Changing this setting might affect the system.\n    <br/><i>Default: 2000</i>', verbose_name=b'Standard aggregated rate (req/min)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
            ],
            options={
                'verbose_name': 'Document Search Live-Feeds',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EhrAgentBaseUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_url', models.CharField(default=dbmconfigapp.models.ehragent.fill_agent_hub_base_url, help_text=b"This is the full qualified domain name for dbMotion's web server. This will be used to build URLs for Collaborate, CV and Agent Service endpoint.<br/>For the default value the following URLs will be used:<br/>https://$_NODE_WEB_SERVER_STATEFUL$.$_NODE_ACCESS_ABSOLUTE_DOMAIN$/SmartAgent/SmartAgentWebService.svc<br/>https://$_NODE_WEB_SERVER_STATEFUL$.$_NODE_ACCESS_ABSOLUTE_DOMAIN$/dbMotionClinicalViewer/ApplicativeDomains/Host/PublicPages/Dispatcher.aspx<br/>https://$_NODE_WEB_SERVER_STATEFUL$.$_NODE_ACCESS_ABSOLUTE_DOMAIN$/collaborate/dbmotion/frontend/security/authentication/dbmPrincipal.v2.api<br/><i>Default: $_NODE_WEB_SERVER_STATEFUL$.$_NODE_ACCESS_ABSOLUTE_DOMAIN$</i>", max_length=200, verbose_name=b'Agent Hub base URL configuration')),
            ],
            options={
                'verbose_name': 'EHR Agent General',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentBlinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admission_interval', dbmconfigapp.models.fields.TimeSpanField(default=b'1|3', help_text=b'Defines the time span from the start of an inpatient admission for which the Badging functionality is enabled.<br/><i>Default: 1 Day</i>', max_length=50, verbose_name=b'First Day Of Admission Interval')),
                ('admission_inpatient_domains', models.TextField(default=b'e757b766e61d08f435d3e9e6280f355c', help_text=b'Defines the Encounter Type domains (in a comma-separated list) used to define the inpatient encounter for which the Badging functionality is enabled.<br/><i>Default: e757b766e61d08f435d3e9e6280f355c (Inpatient encounter)</i>', max_length=400, verbose_name=b'First Day Of Admission Encounter Type Domains')),
            ],
            options={
                'history_meta_label': 'First Day Of Admission Behavior (For Badging)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentCategoriesProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('category_name', models.CharField(unique=True, max_length=60, verbose_name=b'Category')),
                ('enable_category', models.BooleanField(default=True, verbose_name=b'Category Enabled')),
                ('category_opened', models.BooleanField(default=False, help_text=b'Display a category as opened by default', verbose_name=b'Opened By Default ')),
                ('grouping_option', models.IntegerField(default=1, verbose_name=b'Grouping', choices=[(0, b'Disabled'), (1, b'Collapsed'), (2, b'Expanded')])),
                ('category_order', models.IntegerField(help_text=b'Determines the order of the category in the application. The category order configuration is relevant for the CVA main page only.', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('has_tooltips', models.BooleanField(default=False)),
                ('show_in_encounter_details', models.BooleanField(default=False, help_text=b'Select the categories to be displayed in the Encounter Details page. The Encounter-related acts of these categories will be displayed in the Encounter Details page.', verbose_name=b'Categories Displayed in Encounter Details Page')),
            ],
            options={
                'verbose_name': 'Categories Definition',
                'history_meta_label': 'Categories Definition',
                'verbose_name_plural': 'Categories Definition',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentCategoriesTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_name', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentClinicalDomainsProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='AllDomains', max_length=60)),
                ('display_name', models.CharField(default='All Clinical Domains', unique=True, max_length=60, verbose_name=b'Clinical Domain')),
                ('attention_searching_time', models.IntegerField(default=7, null=True, verbose_name=b'Attention Time Range')),
                ('attention_searching_option', models.IntegerField(default=3, verbose_name=b'Attention Time Unit', choices=[(0, b'Year'), (1, b'Month'), (3, b'Day'), (6, b'Off')])),
                ('default_attention_time', models.CharField(default='7 Days', max_length=60, verbose_name=b'Default Attention Time')),
            ],
            options={
                'verbose_name': 'Attention Rule Time Filter',
                'history_meta_label': 'Attention Rule Time Filter',
                'verbose_name_plural': 'Attention Rule Time Filters (For Badging)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentCVCommonClinicalDomainsProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('display_name', models.CharField(unique=True, max_length=60, verbose_name=b'Clinical Domain')),
                ('default_searching_time', models.IntegerField(default=0, null=True, verbose_name=b'Time Range', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2147483647)])),
                ('default_searching_option', models.IntegerField(default=4, verbose_name=b'Time Unit', choices=[(0, b'Year'), (1, b'Month'), (3, b'Day'), (4, b'All')])),
                ('default_time_range', models.CharField(max_length=60, verbose_name=b'Default Time Range')),
            ],
            options={
                'verbose_name': 'Time Range Filter',
                'history_meta_label': 'Time Range Filter',
                'verbose_name_plural': 'Time Range Filters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EhrAgentGeneral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('my_ehr_data_default_view', models.CharField(default=b'False', help_text=b'Determines whether the Delta view or Show All view is displayed by default when first opening the Patient View or EHR Agent.<br/><i>Default: Delta view</i>', max_length=5, verbose_name=b'Initial data view', choices=[(b'False', b'Delta view'), (b'True', b'Show All view')])),
                ('default_bulk_action', models.CharField(default=b'Print', help_text=b'Defines the default action displayed in the Bulk action button.<br/><i>Default: Print</i>', max_length=20, verbose_name=b'Default bulk action', choices=[(b'Print', b'Print'), (b'SendToMyEhr', b'Send')])),
                ('reset_bulk_action', models.BooleanField(default=True, help_text=b'Determines whether to reset the bulk action to the default action after the performing the action (after clicking the Go button).<br/><i>Default: True</i>', verbose_name=b'Reset bulk action to default after bulk action')),
                ('clean_checkboxes_after_bulk_action', models.BooleanField(default=True, help_text=b'Determines whether to clear the bulk action checkboxes after performing the action.<br/><i>Default: True</i>', verbose_name=b'Clear checkboxes after bulk action')),
                ('get_all_data_button_available', models.BooleanField(default=True, help_text=b'Determines whether to display the Get All Data button in the Time Filter Settings window.<br/><i>Default: True</i>', verbose_name=b'Display Get All Data button')),
                ('show_launch_collaborate', models.BooleanField(default=False, help_text=b'Determines whether to display the Launch Collaborate menu option.<br/><i>Default: False</i>', verbose_name=b'Display Launch Collaborate menu option')),
                ('show_send_feedback', models.BooleanField(default=True, help_text=b'Determines whether to display the Send Feedback option in the EHR Agent More Options menu.<br/><i>Default: True</i>', verbose_name=b'Display Send Feedback Menu Option')),
                ('enable_patient_mapping', models.BooleanField(default=False, help_text=b'Determines whether the Patient Mapping Agent is enabled. dbMotion Context Receiver supports a Patient Mapping Agent that is able to receive different patient IDs from each participant that belongs to the same patient. The Patient Mapping Agent, as part of the common context system, maps the identifiers for patients. Whenever an application sets the patient context, the context manager instructs the patient mapping agent (if present) to provide any additional identifiers it knows for the patient.<br/><i>Default: False</i>', verbose_name=b'Patient Mapping Agent')),
                ('footer_logo', models.ImageField(default=b'', storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), upload_to=b'EhrAgent/FooterLogo', blank=True, help_text=b'Defines the logo displayed in the Clinical View Agent Footer.<br/>The following are the logo image type and size requirements:<br/>Type: png<br/>Height max size: 38px<br/>Width max size: 115px<br/>If one of the image dimensions (Height or Width) is larger than the maximum size, the image will be reduced with the lock aspect ratio.<br/><i>Default: No default value</i>', null=True, verbose_name=b'Footer Logo File')),
                ('enable_cv_from_patient_name', models.BooleanField(default=True, help_text=b'Determines whether Clinical Viewer can be launch from the patient name <br/><i>Default: True</i>', verbose_name=b'Launch CV from Patient Name in Agent Hub')),
            ],
            options={
                'verbose_name': 'EHR Agent General',
                'history_meta_label': 'EHR Agent General',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EhrAgentHelp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_name', models.CharField(unique=True, max_length=200, verbose_name=b'Link name')),
                ('link_url', models.CharField(max_length=200, verbose_name=b'URL')),
                ('agentpp_hosted_app_page', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.AgentppHostedAppPage', null=True)),
            ],
            options={
                'verbose_name': 'Help Link',
                'history_meta_label': 'Help Links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentLabratory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_lab_events', dbmconfigapp.models.fields.IntegerFieldEx(default=200, validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(2147483647)], blank=True, help_text=b'Defines the maximum number of latest Lab Events to display in the EHR Agent.<br>The minimum value is 20 Lab Events. To display all labs, leave the field empty.<br/><i>Default: 200</i>', null=True, verbose_name=b'Limit Number Of Lab Events')),
                ('max_clinical_document', dbmconfigapp.models.fields.IntegerFieldEx(default=200, validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(2147483647)], blank=True, help_text=b'Defines the maximum number of latest Clinical Documents to display in the EHR Agent.<br>The minimum value is 20 Documents. To display all documents, leave the field empty.<br/><i>Default: 200</i>', null=True, verbose_name=b'Limit Number Of Clinical Documents')),
            ],
            options={
                'history_meta_label': 'Limit Number Of Clinical Acts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentMeasurementProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain_id', models.CharField(unique=True, max_length=60, verbose_name=b'Vocabulary Domain')),
                ('order', models.IntegerField(verbose_name=b'Order')),
                ('hide_uom', models.BooleanField(default=False, help_text=b'Defines the vital sign measurement in which the UOM (Unit Of Measurement) is hidden. Default: BloodPressure, HeartRate. This configuration applies to Patient View', verbose_name=b'Hide the UOM')),
            ],
            options={
                'verbose_name': 'Measurement Definition',
                'history_meta_label': 'Measurement Definition',
                'verbose_name_plural': 'Measurement Definition',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentMedication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('medication_is_show_calculated_sig', models.BooleanField(default=True, help_text=b'Defines the format of the Medication prescription instructions (SIG) that is displayed in the Clinical View Agent when the calc_sig field is not available. <br>Note: This configuration is applied only in the case that the calc_sig field is NOT populated. <br>- If the calc_sig field is populated, the SIG is displayed as a single line of text. <br>- If the calc_sig field is Null, the display of the SIG depends on this configuration. <br>The SIG includes the Dose, Route, and Frequency of the medication.<br>True (default): The SIG is displayed as calculated from the Dose, Route and the Frequency fields.<br>False: The SIG is displayed in a table format (Structured SIG).<br/><i>Default: True</i>', verbose_name=b'Medication SIG Display')),
            ],
            options={
                'history_meta_label': 'Medication',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentSemanticDelta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('display_name', models.CharField(max_length=60, verbose_name=b'Clinical Domain')),
                ('enable_semantic_delta', models.BooleanField(default=True, help_text=b'Determines whether EHR Agent or Patient View filters out data from the selected domains according to semantic similarity.\nFor more details about the semantic delta behavior please refer to the functional specs.', verbose_name=b'Enable Semantic Delta')),
            ],
            options={
                'verbose_name': 'Enable Semantic Delta',
                'history_meta_label': 'Enable Semantic Delta',
                'verbose_name_plural': 'Semantic Delta Configuration',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentSemanticGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=200, verbose_name=b'Group Display Name')),
                ('order', models.IntegerField(verbose_name=b'Group Order')),
            ],
            options={
                'help_text': 'For the following Measurements configurations, see the <a href="/admin/dbmconfigapp/clinicaldomainvitals/13/">Vitals</a> page under Clinical Viewer Clinical Domains: <ul><li>Displaying/hiding the UOM</li><li>Concatenating Measurement Values</li><li>Defining UOM priority order to display concatenated Body Weight</li><li>Defining UOM priority order to display concatenated Body Height</li></ul>',
                'verbose_name': 'Measurements Domain Grouping',
                'history_meta_label': 'Semantic Group',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentTooltips',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tooltip', models.CharField(max_length=40)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Tooltips Definition',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmergencyDeclarationReasons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=120, verbose_name=b'text')),
                ('culture', models.CharField(max_length=12)),
            ],
            options={
                'verbose_name': 'Emergency Declaration Reason',
                'history_meta_label': 'Emergency Declaration Reasons',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmergencyDeclarationText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(help_text=b'Define the Emergency Declaration Text which will be displayed in the Declare Emergency windows.<br/><i>Default: Organizational policy prevents some patient information from being displayed. Restrictions about patient data can be overridden. To view the data in emergency mode, select a reason to remove the restriction and click Break Glass. To continue without viewing the restricted data, click Cancel. All override actions are audited.<br/><i>Note: there is a permanent text always displayed on Emergency Declaration dialog: "To view the patient record in Emergency mode, select a Reason for Declaration and Click Break Glass. To Exit without viewing the patient record, click Cancel".</i></i>', verbose_name=b'Text', blank=True)),
            ],
            options={
                'history_meta_label': 'Emergency Declaration Text',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EncounterDiagnosisRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primary_diagnosis', models.CharField(default=b'1', help_text=b'Determines the value(s) used for the main (primary) diagnosis of the patient during an encounter, such as a hospitalization.<br/>Possible values: Any value can be configured. For example:  American market: 1   Israeli market: 1, 6, or 1,6<br/>Default Value: 1 (American market)<br/>', max_length=50, verbose_name=b'Primary Diagnosis', validators=[dbmconfigapp.models.pl_general.validate_diagnosis_format])),
                ('admitted_diagnosis', models.CharField(default=b'0', blank=True, help_text=b'Determines the value(s) used for the admitting diagnosis given when the patient was first admitted to the hospital.<br/>Possible Values: Any value can be configured. For example:  American market: 0   Israeli market: Null (empty)<br/>Default Value: 0 (American market)<br/>', max_length=50, verbose_name=b'Admitting Diagnosis', validators=[dbmconfigapp.models.pl_general.validate_string_is_a_num])),
            ],
            options={
                'help_text': 'This configuration determines the code used for the display of the Encounter Diagnosis (or Encounter reason) in the clinical applications (for example, the data displayed in Discharge Diagnosis or the Visit Reason field). The business logic for the displayed data differs depending on the customer location and on the specific field in the application.  For a detailed description of the business logic, see the Functional Specification documentation.<br/>',
                'verbose_name': 'Configure the Encounter Diagnosis',
                'history_meta_label': 'Configure the Encounter Diagnosis',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Defines the Name of the icon and link displayed in the Clinical Viewer navigation toolbar.', max_length=40)),
                ('culture', models.CharField(help_text=b'Defines the culture, For example: en-US.', max_length=10)),
                ('is_active', models.BooleanField(default=True, help_text=b'Determines whether the External Application icon is displayed (Default: true)', verbose_name=b'Active')),
                ('uri', models.CharField(help_text=b'The URI of the External Application.', max_length=200, verbose_name=b'URI')),
                ('method', models.CharField(default=b'GET', help_text=b'Defines the method of access to the external application (Default: GET)', max_length=4, choices=[(b'GET', b'GET'), (b'POST', b'POST')])),
            ],
            options={
                'history_meta_label': 'External Application Links',
                'verbose_name_plural': 'External Application Links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalApplicationParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of parameter used by other application.', max_length=40, verbose_name=b'parameter name')),
                ('dbm_param', models.CharField(default=None, choices=[(b'USER_UserName', b'User name'), (b'USER_FirstName', b'User first name'), (b'USER_LastName', b'User last name'), (b'PAT_Calc_MRN', b'Leading MRN'), (b'Calc_MRN_System', b'MRN source system'), (b'PAT_Calc_Given', b'Patient first name'), (b'PAT_Calc_Family', b'Patient last name'), (b'PAT_BirthDate', b'Patient birth date'), (b'NAV_CVNAME', b'Current Clinical View')], max_length=20, blank=True, help_text=b'In case the parameter is static, enter the value to pass. In case it is a dbMotion parameter, choose the parameter to pass from the drop down list.', null=True, verbose_name=b'parameter value')),
                ('static_value', models.CharField(default=None, max_length=20, null=True, verbose_name=b'static value', blank=True)),
                ('is_static', models.BooleanField(default=False, help_text=b'Indication if the parameter value is static or dbMotion parameter.<br/><i>Default: False</i>')),
            ],
            options={
                'verbose_name_plural': 'External Application Parameters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FindingDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Related Findings grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='GridDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Grid Display Options',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='ImagingPacs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_id', models.CharField(help_text=b'The Imaging study deviceId based on the Federation Node Id.<br/>For Any value define ALL.', max_length=40, null=True, verbose_name=b'deviceId', blank=True)),
                ('use_code', models.CharField(help_text=b'The Imaging study useCode based on the UMS ImageValue.use.<br/>For Any value define ALL.', max_length=40, null=True, verbose_name=b'useCode', blank=True)),
                ('schema_code', models.CharField(help_text=b'The Imaging study SchemeCode based on the UMS ImageValue.Scheme.<br/>For Any value define ALL.', max_length=40, null=True, verbose_name=b'schemeCode', blank=True)),
                ('facility', models.CharField(default=b'ALL', max_length=200, blank=True, help_text=b'In some organizations the PACS URL depends on the user location. In order to configure the correct URL, according to the user location, the User Facility Identification should  be enabled and configured.<br/>If configured, the system will use the PACS URL with the facility that matches the user facility (it detects the facility mapped to the EHR instance intercepted by the Agent Hub).<br/>User Facility Identification should be configured in the following location: CCenter > Agent Hub -> EHR Integration -> EHR Instances -> User Facility Identification.<br/>Format: ID Root|ID Extension.<br/>For Any value define ALL.', null=True, verbose_name=b'facility')),
                ('uri', models.CharField(help_text=b'The URI for the PACS.', max_length=200, verbose_name=b'URI')),
                ('method', models.CharField(default=b'GET', help_text=b'For a Web Application, use one of the following:<br/><b>POST:</b> All the specified parameters are passed as hidden values.<br/><b>GET:</b> All the specified parameters are passed as a connection string, in the order they appear in the configuration.<br/><i>Default: GET</i>', max_length=4, choices=[(b'GET', b'GET'), (b'POST', b'POST')])),
            ],
            options={
                'verbose_name': 'Imaging PACS',
                'history_meta_label': 'Imaging PACS',
                'verbose_name_plural': 'Imaging PACS',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImagingPacsDisclaimer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Pacs_Disclaimer_Text', models.CharField(help_text=b'This configuration determines the text to display as disclaimer on PACS images. When it has some text we display a disclaimer, when it is empty the disclaimer wont be showed. <br/><i>Default: empty</i>', max_length=500, null=True, verbose_name=b'PACS Disclaimer Text', blank=True)),
                ('Grouping_by_Modality', models.BooleanField(default=False, help_text=b'This configuration enables grouping of (UMS: Image study.typecode) designations received with imaging study type. All studies that are received with the same type code designations are grouped together. If the configuration is set to false, grouping of imaging results is by sub domain designation of imaging study  (UMS: Imaging Study code). <br><i> Default: False.</i>', verbose_name=b'Imaging Grouping by Modality')),
            ],
            options={
                'history_meta_label': 'Imaging',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImagingPacsParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of the parameter that should be sent in the request. In projects where the Agent Hub user retrieves images from PACS systems that require validation of the request with a SAML token, enter a new PACS Parameter with the following name: SAMLResponse. For the Parameter Value, enter the certificate thumbprint. In projects where the Agent Hub user retrieves images from PACS systems that use IE different than IE 11, enter a new PACS Parameter with the following name: "X-UA-Compatible". For the Parameter Value, enter the X-UA-Compatible string for example "IE=7" for IE 7 emulation.', max_length=40, verbose_name=b'parameter name')),
                ('is_static', models.BooleanField(default=True, help_text=b'If True (static), the value is taken as is.\nIf False (dynamic), the value is taken from the Image Value Reference field.\n<i>Default: True</i>')),
                ('parameter_value', models.CharField(help_text=b'In cases where the URI requires URL or HTML encoding (GET)/HTML(POST), add either the <b>UrlEncode_ or HtmlEncode_</b> prefix to non-static parameter values, as follows:\n- UrlEncode: Used for the GET method or if the parameter is part of the URL.\n- HtmlEncode: Used for the POST method.', max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Imaging PACS Parameters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InsuranceDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Insurance Grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='LabChartDisplayOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chart_format', models.IntegerField(default=0, help_text=b'Determines whether the Lab Chart display is in line or column format<br><i>Default: Line</i>', verbose_name=b'Chart type', choices=[(0, b'Chart in Line format'), (1, b'Chart in Column format')])),
                ('range_values', models.IntegerField(default=1, help_text=b'Determines whether the range values high/low are retrieved from the business functionality or calculated by the Front End<br><i>Default: Retrieved from the business functionality</i>', verbose_name=b'Range values high/low calculation', choices=[(0, b'Calculated by the Front End'), (1, b'Retrieved from the business functionality')])),
                ('abnormal_values', models.IntegerField(default=1, help_text=b'Determines how the Abnormal values displayed in the chart are calculated.<br><i>Default: Based on the value of the range calculation parameter (above)</i>', verbose_name=b'Abnormal values calculation', choices=[(0, b'Calculated using the business logic'), (1, b'Calculated based on the value of the range calculation parameter (above)')])),
                ('date_format', models.IntegerField(default=0, help_text=b'Determines whether the date is displayed in the DateTime format or as a string.<br><i>Default: DateTime</i>', verbose_name=b'Date display', choices=[(0, b'The date is displayed in the DateTime format'), (1, b'The date is displayed as a string')])),
                ('display_range_values', models.BooleanField(default=False, help_text=b'Determines whether the chart displays the range of values.<br><i>Default: False</i>', verbose_name=b'The chart displays the range of values.')),
                ('display_abnormal_in_color', models.BooleanField(default=False, help_text=b'Determines whether the chart displays Abnormal values in color (red).<br><i>Default: False</i>', verbose_name=b'The chart displays Abnormal values in color (red).')),
                ('report_max_rows_in_regular_col', models.IntegerField(default=20, help_text=b'Defines the maximum number of rows in the regular grid column.<Br>This parameter is used to determine if the text can be displayed in the regular grid column.<Br><i>Default: 20</i>', verbose_name=b'The maximum number of rows in the regular grid column', validators=[django.core.validators.MinValueValidator(1)])),
                ('report_max_chars_in_remark_col', models.IntegerField(default=600, help_text=b'Defines the total maximum number of characters in the Remarks column of the Lab Results Report.<br>This parameter is used to determine if the text can be displayed in the regular grid Remarks column.<br><i>Default: 600</i>', verbose_name=b'The total maximum number of characters in the Remarks column', validators=[django.core.validators.MinValueValidator(1)])),
                ('report_max_rows_in_long_row_cell', models.IntegerField(default=33, help_text=b'Defines the maximum number of rows in a Long Row cell.<br>This parameter is used to determine if the text can be displayed in the Long Row.<br><i>Default: 33</i>', verbose_name=b'The maximum number of rows in a Long Row cell', validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'Lab Chart Display Options',
                'history_meta_label': 'Lab Chart Display Options',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LabsDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Labs grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='LauncherGeneralProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Default Application',
                'history_meta_label': 'Default Application',
                'verbose_name_plural': 'Default Application',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationHistoryDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Location History grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='LoginsHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_name', models.CharField(max_length=100, null=True, blank=True)),
                ('action_time', models.DateTimeField(auto_now_add=True, verbose_name=b'Date/Time')),
                ('action', models.TextField(verbose_name=b'Action')),
            ],
            options={
                'verbose_name': 'Login/Logout Action',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MedicationsDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Medications grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='MigrationManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255, null=True, blank=True)),
                ('ga_migration', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModelDescriptor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=200)),
                ('export_in_api', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MyHRConnectivityEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable_my_hr_flow', models.BooleanField(default=False, help_text=b'Enables MyHR Connectivity for Australian projects.<br/><i>Default: Disable</i>', verbose_name=b'Enable MyHR Connectivity')),
                ('my_hr_oid', models.CharField(help_text=b'Defines the Australian virtual source system used to retrieve the patient IHI. This OID must be identical to the OID of this virtual source system as configured in EMPI -> Authority Systems.<br/><i>Default: Empty</i>', max_length=260, verbose_name=b'IHI source system OID', blank=True)),
                ('pcehr_exist_url', models.CharField(help_text=b'Defines doesPCEHRexists URI to MyHR<br/><i>Default: Empty</i>', max_length=260, null=True, verbose_name=b'Does PCEHR exists URI', blank=True)),
                ('my_hr_node_id', models.PositiveIntegerField(help_text=b'Defines MyHR Node id, node value should be between 101-120<br/><i>Default: Empty</i>', null=True, verbose_name=b'MyHR Node ID', blank=True)),
                ('gain_access_url', models.CharField(help_text=b'Defines gainPCEHRAccess URI to MyHR<br/><i>Default: Empty</i>', max_length=260, null=True, verbose_name=b'Gain PCEHR access URI', blank=True)),
                ('get_document_list_url', models.CharField(help_text=b'Defines getDocumentList URI MyHR<br/><i>Default: Empty</i>', max_length=260, null=True, verbose_name=b'Get Document List URI', blank=True)),
                ('get_document_url', models.CharField(help_text=b'Defines getDocument URI MyHR<br/><i>Default: Empty</i>', max_length=260, null=True, verbose_name=b'Get Document URI', blank=True)),
                ('stylesheet', models.FileField(help_text=b'Defines the stylesheet that will be used to display CDAs retrieved from the MyHR node. The file extension must be .xslt or .xsl for the system to function properly. The stylesheet should contain all styling as part of the xslt and should be XSLT 1.0.<br/><i>Default: DH_Generic_CDA_Stylesheet-1.3.0.xsl</i>', upload_to=b'MyHR/Stylesheet', storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), null=True, verbose_name=b'CDA Stylesheet')),
            ],
            options={
                'verbose_name': 'MyHR Connectivity',
                'history_meta_label': 'MyHR Connectivity',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MyHRConnectivityPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'MyHR Connectivity',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MyHROrganizationsEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iho_thumbprint', models.CharField(help_text=b'Defines the thumbprint of IHO<br/><i>Default: Empty</i>', max_length=260, verbose_name=b'IHO Thumbprint')),
                ('iho_name', models.CharField(help_text=b'Defines the IHO name<br/><i>Default: Empty</i>', unique=True, max_length=260, verbose_name=b'IHO Name')),
                ('org_name', models.CharField(help_text=b'Defines the Organization Name of the IHO<br/><i>Default: Empty</i>', max_length=260, verbose_name=b'Organization Name', blank=True)),
            ],
            options={
                'verbose_name': 'MyHR Organization',
                'history_meta_label': 'MyHR Organization',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OperationalManagerPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Usage Reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantBaselineListModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paticipant_name', models.CharField(default=b'', help_text=b'Carequality participant name.', max_length=400, verbose_name=b'Name')),
                ('paticipant_identifier', models.CharField(default=b'', help_text=b'Carequality participant OID.', max_length=400, verbose_name=b'Identifier')),
            ],
            options={
                'verbose_name': 'Shared Participant',
                'history_meta_label': 'Shared Participant List',
                'verbose_name_plural': 'Shared Participant List',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantListBasedPAAModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('healthcare_institude_name', models.CharField(default=b'', help_text=b'Name of institute. Enter to ease the future management of the table contents. For display only.', max_length=400, verbose_name=b'Healthcare Institute Name', blank=True)),
                ('patient_assigning_authority_name', models.CharField(default=b'', help_text=b'Patient Assigning Authority Name as displayed in CCenter under EMPI- Assigning Authority', max_length=400, verbose_name=b'Patient Assigning Authority Name', blank=True)),
                ('identifier', models.CharField(default=b'', help_text=b'Patient Assigning Authority OID as displayed in CCenter under EMPI- Assigning Authority.', unique=True, max_length=400, verbose_name=b'Identifier')),
                ('home_community_id_three_level', models.CharField(default=b'', help_text=b"Defines the facility's Home Community ID (OID) for outbound requests to Carequality.The OID format should be: urn:oid:n.n.n.n.n.n. For example: urn:oid:2.16.840.1.113883.3.57.1.3.0.2. If it is empty, the dbMotion Home Community ID  will be used by default.", max_length=400, verbose_name=b'Home Community ID', blank=True)),
            ],
            options={
                'verbose_name': 'Settings Per EHR',
                'history_meta_label': 'Settings Per EHR',
                'verbose_name_plural': 'Settings Per EHR',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantListModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paticipant_name', models.CharField(default=b'', help_text=b'Carequality participant name.', max_length=400, verbose_name=b'Name')),
                ('paticipant_identifier', models.CharField(default=b'', help_text=b'Carequality participant OID.', max_length=400, verbose_name=b'Identifier')),
            ],
            options={
                'verbose_name': 'Carequality Participant',
                'history_meta_label': 'Carequality Participants',
                'verbose_name_plural': 'Carequality Participants',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientDetailsSectionOrdering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=60, verbose_name=b'Patient details section', blank=True)),
                ('code', models.CharField(max_length=60, blank=True)),
                ('priority_order', models.IntegerField(help_text=b'', verbose_name=b'Section order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientSearchDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Patient Search Results Grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='PatientSearchDefaultSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_search', models.IntegerField(default=1, help_text=b'Supported by Clinical Viewer only.<br/>Defines the default type of the patient search method.<br><i>Default: Search by Demographics</i>', verbose_name=b'Default Search method', choices=[(0, b'Search by MRN'), (1, b'Search by Demographics')])),
            ],
            options={
                'history_meta_label': 'Default Patient Search',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientSearchDisplayOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_warning', models.BooleanField(default=False, help_text=b'Note: Only for Clinical Viewer<br>Determines whether the system displays a warning message when the selected leading record has no data. In this case the system displays the latest record (from those selected by the user) for the same patient that exists in the CDR.<br>If True, a message informs the user that the leading record has been changed.<br>If False, no message is displayed.<br><i>Default: True</i>', verbose_name=b'Display a warning message when the selected leading record has no data')),
                ('cluster_selection_behavior', models.IntegerField(default=0, help_text=b'Supported by Clinical Viewer only.<br/>This configuration enables or disables the option to clear the previously selected linkage set.<br><i>Default: Previous selected linkage set is not cleared</i>', verbose_name=b'Cluster selection behavior', choices=[(1, b'Previous selected linkage set is cleared'), (0, b'Previous selected linkage set is not cleared')])),
                ('display_user_attestation', models.BooleanField(default=False, help_text=b'Determines whether the system displays a confirmation message before the user enters the patient record.<br>True: A confirmation message is displayed.<br>False: No message is displayed.<br>Note: This configuration is supported by Agent hub.<br><i>Default: False</i>', verbose_name=b'Display Confirmation Message Before User Enters Patient Record')),
                ('attestation_text', models.TextField(help_text=b'Define the Attestation Message Text displayed to the user<br/><i>Default: Please note that you are about to enter the patient record. Please confirm you requested to view the patient clinical information explicitly for treatment reasons only, and not for other reasons (such as research, etc).</i>', null=True, verbose_name=b'Attestation Message Text', blank=True)),
                ('authority_text', models.CharField(help_text=b'Define the patient assigning authority used to retry fetch patient data that exists in the enterprise master patient index (EMPI), but not in the dbMotion Clinical Data Repository (CDR). If the patient assigning authority is defined, the system attempts to fetch patient data for 10 seconds. If the patient assigning authority is not defined, the feature is unavailable.', max_length=260, null=True, verbose_name=b'Specify patient assigning authority to enable retry', blank=True)),
                ('enable_death_indicator', models.BooleanField(default=True, help_text=b'Specifies if the Deceased indicator is displayed in the patient search results grid.<br><i>Default: True</i>', verbose_name=b'Display Deceased indicator on patient search results grid')),
            ],
            options={
                'history_meta_label': 'Display Options',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientSearchHistoryDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Patient Search History Grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='PatientSearchPage',
            fields=[
                ('clinicaldomain_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.ClinicalDomain')),
            ],
            options={
            },
            bases=('dbmconfigapp.clinicaldomain',),
        ),
        migrations.CreateModel(
            name='CvPatientSearch',
            fields=[
                ('patientsearchpage_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.PatientSearchPage')),
            ],
            options={
                'history_meta_label': 'Patient Search (from Clinical Viewer)',
            },
            bases=('dbmconfigapp.patientsearchpage',),
        ),
        migrations.CreateModel(
            name='PatientSearchTooltip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=120, verbose_name=b'text')),
                ('culture', models.CharField(max_length=12)),
            ],
            options={
                'history_meta_label': 'Patient Search Tooltips',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientsListViews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patients_list_type', models.CharField(max_length=75, verbose_name=b'Patients List Type')),
                ('patients_list_label', models.CharField(help_text=b'Defined label is displayed to all users with page access. Default is page name.', unique=True, max_length=75, verbose_name=b'Label')),
                ('patients_list_order', models.IntegerField(help_text=b'The order of pages are displayed.', verbose_name=b'Order', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('patients_list_roles', models.CharField(default=b'None', help_text=b"Defines the user roles which has access to view this Page. Possible Values: All, None, Role names separated by ','. When the values is 'All' all users will have access to view this page. When certain role(s) are filled, only users having that role(s) will be able to access this page. Default is None , which means no user can access this page", max_length=500, verbose_name=b'User Roles')),
                ('patients_relation_type', models.CharField(max_length=75, null=True, verbose_name=b'Relationship Type', blank=True)),
            ],
            options={
                'verbose_name': '"My Patient" List',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientViewDefaultLandingPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_page', models.IntegerField(default=0, help_text=b'Determines the default landing page when a user enters a patient file. This configuration applies to Patient View only. A user can override the configuration and select a different landing page in User Settings > Application Preferences.<br/><i>Default: Patient Summary</i>', verbose_name=b'Default landing page', choices=[(0, b'Patient Summary'), (1, b'View by Category'), (2, b'View by Date')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientViewGeneralDefinitions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_logofile', models.ImageField(default=b'', storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), upload_to=b'PatientView/Logo', blank=True, help_text=b'Defines the default logo presented in the Login Page.<br/>The following are the logo image type and size requirements:<br/>Type: PNG<br/>Height: 28px<br/>Width: 304px<br/><i>Default: Allscripts Logo</i>', null=True, verbose_name=b'Logo Image')),
                ('project_name', models.CharField(default=b'', help_text=b'This configuration is to define the default Project Name presented in the Login Page.<br/><i>Default: dbMotion&trade; Solution</i>', max_length=35, verbose_name=b'Project Name', blank=True)),
                ('background_image', models.ImageField(default=b'', storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), upload_to=b'PatientView/BackgroundImage', blank=True, help_text=b'Defines the background image displayed in the Login Page.<br/>The following are the background image type and size requirements:<br/>Type: JPEG, PNG, BMP, GIF<br/>Height: 1080px<br/>Width: 1920px<br/>Weight: Upto 2MB<br/><i>Default: Solid #f2f2f2 Background color</i>', null=True, verbose_name=b'Background Image')),
            ],
            options={
                'history_meta_label': 'Set Patient View Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientViewPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Set Patient View Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlClinicalCodeDisplayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Patient list Clinical Code Display',
                'history_meta_label': 'Patient list Clinical Code Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlGeneralPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Patient List General',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlPatientDisplayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Patient Display',
                'history_meta_label': 'Patient Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlReportingPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Reporting',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PpolGeneral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PatientDefaultCacheTolerance', models.IntegerField(default=-1, help_text=b"\n                Patient information is imported from the VIA service. To improve the Provider Registry service performance, the patient information is cached in the Provider Registry service.<br/>\n                Each cached patient stores its last refreshed Date and Time. Patient retrieval service calls may specify the maximum period of time that they accept cached patient information to be used.<br/>\n                For example, if a consumer accepts cached patient up to a week, and the actual patient was last refreshed 6 days ago, the Provider Registry will communicate to VIA to import updated data.<br/>\n                In addition, the Provider Registry service may eagerly import patient information from VIA when the cached information is close to expiration.<br/>\n                This configuration defines the default patient cache tolerance value in seconds.<br/>\n                If a service call does not specify a cache tolerance, the service does not refresh the patient information.<br/>\n                If you set a shorter period of time may lower the service response time.<br/>\n                The default is that service calls shouldn't trigger a patient refresh, due to the 'CDR Auto Discovery' mechanism of ProviderRegistry, where loaded messages to CDR triggers a patient refresh.<br/>\n                Possible Values: -1 (no refresh), 604800 (Week).\n                <br/><i>Default: -1 (no refresh)</i>", verbose_name=b'Patient Default Cache Tolerance (Seconds)', validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(2147483647)])),
                ('ParsedDateTimeFormat', models.CharField(default=b'yyyy-MM-dd HH:mm', help_text=b"Defines the DateTime format in the Provider Registry.<br/>In cases where Initiate will change to support the full date time (which might not be supported for all customers), the value should be changed to yyyy-MM-dd HH:mm.<br/>Relevant the following: <br/>- patient's birth date (and new-born age display)<br/>- patient's death time<br/>-  JoinHinMode (Consent) creation & update date<br/><i>Default: yyyy-MM-dd HH:mm</i>", max_length=20, verbose_name=b'Parsed Date Time Format', choices=[(b'yyyy-MM-dd', b'yyyy-MM-dd'), (b'yyyy-MM-dd HH:mm', b'yyyy-MM-dd HH:mm')])),
                ('PcpRelationStrategy', models.IntegerField(default=0, help_text=b'Defines the PCP relation strategy.<br/>CDR aligned - This strategy enables a single patient cluster to have more than one PCP relation<br/>Last Updated - This strategy enables a single patient cluster to have only one PCP relation<br/><i>Default: CDR aligned PCP relation strategy.</i>', verbose_name=b'PCP relation strategies', choices=[(0, b'CDR aligned PCP relation strategy'), (1, b'Last Updated PCP relation strategy')])),
                ('CdrDiscovery', models.BooleanField(default=True, help_text=b'Determines whether Provider Registry should sync both CDR patients and their PCP relations into Provider Registry DB. Used for CAG, Collaborate and PH.<br/><span style="font-style:italic">Default: True</span>', verbose_name=b'Enable CDR discovery')),
                ('MedicalStaffSync', models.BooleanField(default=True, help_text=b'Determines whether Provider Registry should sync CDR medical-staff into Provider Registry DB. Used for CAG, Collaborate.<br/><span style="font-style:italic">Default: True</span>', verbose_name=b'Enable medical-staff sync')),
                ('MaximumAttemptsNumber', models.IntegerField(default=3, help_text=b'Maximum number of attempts to try resolving either patients or relations in case of failure<br/><span style="font-style:italic">Default: 3.</span><br/>', verbose_name=b'Maximum attempts number', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2147483647)])),
                ('PatientResetWorker', models.IntegerField(default=20, help_text=b'The time duration between failed patient and process status reset.<br/><span style="font-style:italic">Default: 20.</span><br/><span style="font-style:italic">Units: Minutes.</span><br/>', verbose_name=b'Time duration until patient status reset', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2147483647)])),
                ('RelationSourceResetWorker', models.IntegerField(default=20, help_text=b'The time duration between failed relation source and process status reset.<br/><span style="font-style:italic">Default: 20.</span><br/><span style="font-style:italic">Units: Minutes.</span><br/>', verbose_name=b'Time duration until relation source status reset', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2147483647)])),
                ('RelationTargetResetWorker', models.IntegerField(default=20, help_text=b'The time duration between failed relation target and process status reset.<br/><span style="font-style:italic">Default: 20.</span><br/><span style="font-style:italic">Units: Minutes.</span><br/>', verbose_name=b'Time duration until relation target status reset', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2147483647)])),
                ('GeneralResetWorker', models.IntegerField(default=720, help_text=b'The time duration between unexpected failed item and process status reset.<br/><span style="font-style:italic">Default: 720.</span><br/><span style="font-style:italic">Units: Minutes.</span><br/>', verbose_name=b'Time duration until unexpected status reset', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2147483647)])),
                ('MedicalStaffSyncTracing', models.BooleanField(default=False, help_text=b'Determines whether Provider Registry should generate trace files during CDR medical-staff synchronization.<br/><span style="font-style:italic">Default: False</span>', verbose_name=b'Enable medical-staff sync tracing files generation')),
            ],
            options={
                'verbose_name': 'PPOL General',
                'history_meta_label': 'Provider Registry',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProblemsDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Problems grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='ProviderRelationshipDataElement',
            fields=[
                ('dataelement_ptr', models.OneToOneField(on_delete=models.SET_NULL, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dbmconfigapp.DataElement')),
            ],
            options={
                'history_meta_label': 'Provider Relationship grid',
            },
            bases=('dbmconfigapp.dataelement',),
        ),
        migrations.CreateModel(
            name='PVCategoriesProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(default=b'External Documents', max_length=60, verbose_name=b'Category Type')),
                ('display_name', models.CharField(help_text=b'Defines the name to display for the clinical category in the application. Display name configuration is applicable to Patient View only.', unique=True, max_length=75, verbose_name=b'Category Display Name', validators=[dbmconfigapp.utils.custom_validators.validate_not_empty_string])),
                ('hide_fields', models.CharField(help_text=b'For the Details pane, specify the metadata fields to hide. Use the format Label1, Label2 ; example, in Problems  enter: "Status, Source" to hide these fields on details page of Problems. <br/>For Encounters: Diagnosis, Chief Complaint, Location History and Providers sections can also be hidden, also hides Service, Location and Diagnosis on encounter cards and reports.', max_length=500, null=True, verbose_name=b'Hide Fields', blank=True)),
                ('category_order', models.IntegerField(help_text=b'Defines the order of clinical categories to display in the application. Category order configuration is applicable to Patient View only.', null=True, verbose_name=b'Category Order', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('expand_by_default', models.BooleanField(default=False, help_text=b'Defines if the category should be expanded by default on enter patient file, in view by category. Applicable only to Patient view application.', verbose_name=b'Expand by default')),
                ('nodes', models.CharField(help_text=b"Defines the list of XDS.b and XCA nodes for the dedicated External Documents page, in the following format: nodeID1,nodeID2.<br/>Possible values: Empty, nodeIDs seperated by ','.<br/>When the value is list of nodeID is then only that nodes which are configured in master config file will be queried for external documents list, when the value is Empty no nodes will be queried.<br/>User should not configure same nodes in more than one external document category.<br/>Default: Empty.", max_length=500, null=True, verbose_name=b'XDS.b Nodes', blank=True)),
                ('roles', models.CharField(default=b'All', max_length=500, null=True, verbose_name=b'Permitted Roles', help_text=b"Defines the user roles which has access to view this External Documents category.<br/>Possible values: All, None, Role names separated by ','. <br/>When the value is 'All' all users will have access to view this category. <br/> When certain role(s) are filled, only users having that role(s) will be able to access this category.<br/>When the value is 'None' no user can view/access this category.<br/>Default: All.")),
                ('time_frame', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], blank=True, help_text=b'Defines the timeframe in years to load data for this External Documents category. If no value or 0 is configured, then entire data is loaded for the category.<br/>Default: 1 Year.', null=True, verbose_name=b'Timeframe')),
                ('information_text', models.CharField(help_text=b'Defines the text to show on this External documents category as a tooltip and as information text to explain about the source of the data displayed under this category.', max_length=500, null=True, verbose_name=b'Information Text', blank=True)),
            ],
            options={
                'verbose_name': 'External Document Category',
                'history_meta_label': 'Patient View Categories',
                'verbose_name_plural': 'Patient View Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PVCCDADisplayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'CCDA Display and Data Export',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PVClinicalCodeDisplayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Clinical Code Display',
                'history_meta_label': 'Clinical Code Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PVClinicalDomainPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Set Clinical domains Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PVMeasurementPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Measurement',
                'history_meta_label': 'Measurement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PVPatientDisplayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Set the Patient Display Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PvPatientNameDisplay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pv_patient_name_display', models.CharField(default=b'{FNAME}, |{GNAME} |{MNAME}', help_text=b'Defines the display name and the order of the patient display name parts. Only the parts configured will be displayed in patient view. Example: {GNAME}, |{FNAME}. Default: {FNAME}, |{GNAME} |{MNAME}', max_length=200, verbose_name=b'Patient Name Display')),
            ],
            options={
                'verbose_name': 'Patient Name Display',
                'history_meta_label': 'Patient Name Display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PVPatientSearchPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Set Patient Search Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PVReportingPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
            ],
            options={
                'verbose_name': 'Reporting',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchResultGrid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(unique=True, max_length=260)),
                ('column_order', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('default_fields', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Search Result field',
                'history_meta_label': 'Search Result Field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('verbose_name', models.CharField(max_length=60)),
                ('code_name', models.CharField(max_length=60)),
                ('need_restart', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecializedViews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('view_name', models.CharField(help_text=b'Defines the name of specialized view and allows to type alpha numeric text. Mandatory field to fill to create a view, default: Empty', unique=True, max_length=50)),
                ('domain_codes_file_name', models.FileField(default=b'', help_text=b'The CSV file Defines the category type and codes (Code & Code system) to display under the specialized view. Category type should match with the defined category types in dbMotion. Mandatory field to fill, default: Empty', storage=dbmconfigapp.models.database_storage.DatabaseStorage({'table': 'dbmconfigapp_dbfiles', 'base_url': '/dbmconfigapp/files/'}), verbose_name=b'Domains and Codes file', upload_to=b'PatientView/SpecializedViews')),
                ('roles', models.CharField(default=b'None', help_text=b"Defines the user roles which has access to view this specialized view.<br/>Possible values: All, None, Role names separated by ','. <br/>When the value is 'All' all users will have access to view this category. <br/> When certain role(s) are filled, only users having that role(s) will be able to access this category.<br/>When the value is 'None' no user can view/access this category.<br/>Default: None.", max_length=500, verbose_name=b'Permitted Roles')),
                ('patient_view_page', models.ForeignKey(on_delete=models.CASCADE, default=1, to='dbmconfigapp.PatientViewPage')),
            ],
            options={
                'verbose_name': 'Specialized view',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SystemParameters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('param_name', models.CharField(unique=True, max_length=100, verbose_name=b'Parameter Name')),
                ('param_value', models.CharField(max_length=100, verbose_name=b'Parameter Value')),
            ],
            options={
                'verbose_name': 'System Parameters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsageReports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('smtp_url', models.CharField(default=b'db-cas', max_length=512, null=True, verbose_name=b'SMTP URL', blank=True)),
                ('smtp_port', models.IntegerField(default=25, blank=True, null=True, verbose_name=b'SMTP port', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65536)])),
                ('from_address', models.EmailField(default=b'ReportingServices@dbMotion.com', max_length=75, null=True, blank=True)),
                ('status', models.CharField(max_length=20, null=True, blank=True)),
                ('message', models.CharField(max_length=200, null=True, blank=True)),
                ('parent', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.OperationalManagerPage', null=True)),
            ],
            options={
                'history_meta_label': 'Usage Reports',
                'verbose_name_plural': 'Usage Reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=255)),
                ('install_date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VitalsInpatientMeasurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('include_inpatient_measurements', models.BooleanField(default=False, help_text=b'Determines whether Inpatient Measurements are displayed in the Vital Signs domain in CV and EHR Agent.<br>True: Inpatient Measurements will be displayed in Vital Signs.<br>False: Inpatient Measurements will be filtered out and not displayed in Vital Signs.<br>Inpatient Encounter baseline codes: 2.16.840.1.113883.5.4|IMP^2.16.840.1.113883.5.4|ACUTE^2.16.840.1.113883.5.4|NONAC<br><br>Note that all Inpatient Measurements will be displayed. In extreme cases, this can increase system load and reduce performance and product usability. Therefore, we recommend loading only the relevant measurements to the CDR.<br/><i>Default: False</i>', verbose_name=b'Include Inpatient Measurements')),
                ('include_emergency_measurements', models.BooleanField(default=False, help_text=b'Determines whether Emergency Measurements are displayed in the Vital Signs domain in CV and EHR Agent.<br>True: Emergency Measurements will be displayed in Vital Signs.<br>False: Emergency Measurements will be filtered out and not displayed in Vital Signs.<br>Emergency Encounter baseline codes: 2.16.840.1.113883.5.4|EMER<br><br>Note that all Emergency Measurements will be displayed. In extreme cases, this can increase system load and reduce performance and product usability. Therefore, we recommend loading only the relevant measurements to the CDR.<br/><i>Default: False</i>', verbose_name=b'Include Emergency Measurements')),
                ('cv_vital_parent', models.ForeignKey(on_delete=models.SET_NULL, default=13, editable=False, to='dbmconfigapp.ClinicalDomain', null=True)),
                ('pv_parent', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.PVMeasurementPage', null=True)),
            ],
            options={
                'history_meta_label': 'Inpatient Measurements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vpo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_id_type_display_priority', models.CharField(default=b'', max_length=20, blank=True, help_text=b"This configuration applies to Clinical Viewer only.<br/>Defines the priority for displaying the patient ID in the Patient Details header (can be used to display the patient's PHIN instead of displaying the MRN), using the &lt;code&gt;|&lt;code&gt; format.<br/><i>Default: MRN|SSN</i>", null=True, verbose_name=b'Patient ID display priority')),
                ('pv_patient_id_type_display_priority', models.CharField(default=b'', max_length=100, blank=True, help_text=b"This configuration applies to Patient View.<br/>Defines the priority for displaying the patient ID in the Patient Banner, this configuration can be used to display the patient's PHIN instead of displaying the MRN.<br/>Patient View - using the &lt;code&gt;^label|&lt;code&gt;^label format, user can define the code priority and label of it for displaying on Patient Banner.<br/>If label is not configured, by default code is displayed as label.<br/><i>Default: MRN|SSN</i>", null=True, verbose_name=b'Patient ID display priority')),
                ('patient_name_type_priority', models.CharField(default=b'', max_length=20, blank=True, help_text=b'Defines the sorting order of name parts to display in the Name grid , using the &lt;code&gt;|&lt;code&gt; format.<br/><i>Default: FAM|GIV|PFX</i>', null=True, verbose_name=b'Name parts sorting order')),
                ('medical_staff_types_priority', models.TextField(help_text=b'Defines the code (using the &lt;code system&gt;|&lt;code&gt;^&lt;code system&gt;|&lt;code&gt; format) used to determine the priority order for displaying the Medical Staff type in the Document label.<br/>For example, if the priority is Author, Authenticator, then the Author of the document is displayed. If there is no Author, the Authenticator is displayed.<br/>If both exist, the first is displayed.<br/><i>Default: 2.16.840.1.113883.5.90|AUT^2.16.840.1.113883.5.90|AUTHEN</i>', null=True, verbose_name=b'Priority of Medical staff types', blank=True)),
                ('filter_mood_codes', models.TextField(null=True, verbose_name=b'Mood Codes to filter out', blank=True)),
                ('encounter_types_to_display', models.TextField(help_text=b'Defines which Encounter Types to filter (to display) in the Encounter Summary grid. By default all Types are displayed.<br/>To display only one or multiple specific Encounter Types, the &lt;code system&gt;|&lt;code&gt;^&lt;code system&gt;|&lt;code&gt; format must be used.<br/><i>Default: ALL</i>', null=True, verbose_name=b'Encounter types to display', blank=True)),
                ('encounters_remove_duplicated', models.BooleanField(default=False, help_text=b'Determines whether to display all Locations in the Location History grid as retrieved (that is, including, if relevant, the same location consecutively more than once) or to filter the Locations by removing consecutive duplicate records.<br/>If True, the second and any subsequent consecutive duplicate location records are removed.<br/>If False, all locations records are displayed as retrieved.<br/><i>Default: False</i>', verbose_name=b'Remove duplicated Location records')),
                ('encounters_enable_episode_filter', models.BooleanField(default=False, help_text=b'Determines whether to Enable the Episode Filter<br/>When the value is True, only Encounters with End date = Null with Inpatient Code =2.16.840.1.113883.5.4|IMP are treated as open encounters (Episode). Emergency Code =2.16.840.1.113883.5.4|EMER will cause encounters to be treated as episodes based on the Duration of emergency encounter parameter (below) and other Encounter codes will be treated as closed encounters (Events).<br/>When the value is False, every encounter with End date = Null is treated as an open encounter (an Episode). Duration of emergency encounter parameter is ignored.<br/><i>Default: False</i>', verbose_name=b'Enable Episode filter')),
                ('encounters_emergency_threshold', models.PositiveSmallIntegerField(help_text=b'This configuration point is only relevant if the Enable Episode Filter parameter (above) is True.<br/>Defines the duration, in number of hours, of an Emergency Encounter when there is no Discharge Date (Discharge Date = NULL).<br/><i>Default: 24</i>', null=True, verbose_name=b'Duration of emergency encounter', blank=True)),
                ('lab_susceptibility_methods_code_type', models.CharField(help_text=b'Determines how the Lab Results and Lab Results History clinical views and reports (in the Clinical Viewer, Collaborate, Patient List and EHR Agent applications) display the types of Microbiology Test results.<br/><i>Default: MIC: Displays all types of test results in a MIC captioned column.</i>', max_length=20, null=True, verbose_name=b'Labs method type', choices=[(b'MIC', b'MIC: Displays all types of test results in a MIC captioned column.'), (b'KB', b'KB: Displays all types of test results in a KB captioned column.'), (b'Both', b'Both: Displays all types of results in a Zone\\MIC captioned column and also the following designation in the Remarks column: Vocabulary Domain designation or Method Unknown.')])),
                ('summary_top_encounters', models.IntegerField(default=-1, help_text=b"Defines the number of the patients' latest Encounter records to display in the Encounters Summary.<br><i>Default: 4</i>", verbose_name=b'Number of Encounter records to display', choices=[(-1, b'All'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10')])),
                ('summary_top_allergy_intolerance', models.IntegerField(default=-1, help_text=b"Defines the number of the patients' latest Allergy records to display in the Allergies Summary.<br><i>Default: 4</i>", verbose_name=b'Number of Allergy records to display', choices=[(-1, b'All'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10')])),
                ('summary_top_conditions', models.IntegerField(default=-1, help_text=b"Defines the number of the patients' latest Problem records to display in the Problems  Summary.<br><i>Default: 5</i>", verbose_name=b'Number of Problem records to display', choices=[(-1, b'All'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10')])),
                ('summary_top_laboratory_events', models.IntegerField(default=-1, help_text=b"Defines the number of the patients' latest Lab records to display in the Labs Summary.<br><i>Default: All</i>", verbose_name=b'Number of Lab records to display', choices=[(-1, b'All'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10')])),
                ('summary_top_substance_administration', models.IntegerField(default=-1, help_text=b"Defines the number of the patients' latest Medication records to display in the Medications Summary.<br><i>Default: All</i>", verbose_name=b'Number of Medication records to display', choices=[(-1, b'All'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10')])),
                ('summary_med_filter_undefined_status', models.BooleanField(default=False, help_text=b'Determines whether to filter (display) Medications whose status is Undefined.<br/>If True, the medication is displayed.<br/>If False, the medication is not displayed.<br/><i>Default: True</i>', verbose_name=b'Display Medications whose status is Undefined.')),
                ('summary_time_filter_amount_labs', models.PositiveSmallIntegerField(null=True)),
                ('summary_time_filter_unit_labs', models.IntegerField(default=0, verbose_name=b'', choices=[(0, b'Year'), (1, b'Month'), (4, b'All')])),
                ('summary_time_filter_amount_encounter', models.PositiveSmallIntegerField(null=True)),
                ('summary_time_filter_unit_encounter', models.IntegerField(default=0, verbose_name=b'', choices=[(0, b'Year'), (1, b'Month'), (4, b'All')])),
                ('summary_time_filter_amount_meds', models.PositiveSmallIntegerField(null=True)),
                ('summary_time_filter_unit_meds', models.IntegerField(default=0, verbose_name=b'', choices=[(0, b'Year'), (1, b'Month'), (4, b'All')])),
                ('domains_to_hide_uom', models.TextField(help_text=b'Defines the Vital Signs measurement in which the UOM (Unit of Measurement) is hidden (not displayed), by default.<br/>Note: Multiple measurements should be separated by commas (Example: BodyWeight,BodyHeight).<br/><i>BloodPressure</i>', null=True, verbose_name=b'Vitals Measurements in which to hide the UOM', blank=True)),
                ('domains_to_concatenate_values', models.TextField(help_text=b'Defines the Vitals Measurements to be displayed as concatenated. For example: 65 kg 50 g or 65.5 kg<br/>Note: Multiple measurements should be separated by commas (Example: BodyWeight,BodyHeight).<br/><i>BloodPressure</i>', null=True, verbose_name=b'Vitals Measurements to display with concatenated values', blank=True)),
                ('filter_cancelled_items', models.BooleanField(default=False, verbose_name=b'Filter cancelled items')),
                ('filter_status_code', models.TextField(help_text=b'Defines the code used to filter the %s list (using the &lt;code system&gt;|&lt;code&gt^&lt;code system&gt|&lt;code&gt; format).<br/><i>Default: %s</i>', null=True, verbose_name=b'%s filter status code', blank=True)),
                ('unit_priority_list_body_weight', models.TextField(null=True, blank=True)),
                ('unit_priority_list_body_height', models.TextField(null=True, blank=True)),
                ('patient_privacy_indicate_minority', models.NullBooleanField(help_text=b'This configuration applies to Clinical Viewer and Patient View.<br/>Determines whether the system indicates if a patient is a minor in the Patient Details area.<br/><i>Default: False</i>', verbose_name=b'Indicate if a patient is a minor')),
                ('patient_privacy_minor_min', models.PositiveSmallIntegerField(help_text=b'This configuration applies to Clinical Viewer and Patient View.<br/>Defines the minimum age in years (inclusive) that determines if the patient is a minor.<br/><i>Default: 11</i>', null=True, verbose_name=b'Minor minimum age')),
                ('patient_privacy_minor_max', models.PositiveSmallIntegerField(help_text=b'This configuration applies to Clinical Viewer and Patient View.<br/>Defines the maximum age in years (inclusive) that determines if the patient is a minor.<br/><i>Default: 18</i>', null=True, verbose_name=b'Minor maximum age')),
                ('lab_report_fixed_width_font', models.BooleanField(default=True, help_text=b'Determines whether to show the Lab Report Remark and Result text in fixed-width font.<br/>True: Displays text in fixed-width font.<br/>False: Does not display text in fixed-width font.<br/><i>Default: True</i>', verbose_name=b'Display report text in fixed-width font')),
                ('facility_filter_enable', models.BooleanField(default=False, help_text=b"Determines whether the User Facility filter is enabled.<br/>If false, the user will see the patient record regardless of the facility related to the patient's acts.<br/>If true, the user will only be authorized to enter the patient record if at least one patient index includes the user's facility or a child of the user's facility. If no patient index includes the user facility, the user will not be authorized to enter patient file (the system's behavior will be identical to the behavior that occurs with patient confidentiality).<br/><i>Default: false</i>")),
                ('user_facility_root_oid', models.CharField(help_text=b"Defines the root Identifier of the Facility for which the Facility filter is enabled. This identifier enables the system to identify all the relevant parent and child facilities. This OID must be identical to the root OID that was used to load the customer's organizational structure to dbMotion CDR.<br/><i>Default: empty</i>", max_length=40, null=True, verbose_name=b'User Facility Root OID', blank=True)),
                ('grouping_mode', models.IntegerField(default=1, help_text=b'Determines the priority order for grouping:<br>Baseline, Local: First, group by baseline subdomain; if local code is unmapped, group by local subdomain.<br>Local, Baseline: First, group by local subdomain; if local code is under the root domain, and is mapped to a baseline code, group by baseline subdomain.<br>If local code is unmapped and is under a root domain, display under "Others".<br>This configuration applies to Clinical Viewer, EHR Agent and Patient View .<br/><i>Default: Baseline, Local</i>', null=True, verbose_name=b'Grouping Priority Order', choices=[(1, b'Baseline, Local'), (0, b'Local, Baseline')])),
                ('clinical_domain', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.ClinicalDomain', null=True)),
                ('cv_general', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.ClinicalViewerGeneralPage', null=True)),
                ('cv_patient_display', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.CvPatientDisplayPage', null=True)),
                ('pl_parent', models.ForeignKey(on_delete=models.SET_NULL, default=None, editable=False, to='dbmconfigapp.PlGeneralPage', null=True)),
                ('pl_patient_display', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.PlPatientDisplayPage', null=True)),
                ('pv_grouping_mode', models.ForeignKey(on_delete=models.SET_NULL, default=None, editable=False, to='dbmconfigapp.PVClinicalDomainPage', null=True)),
                ('pv_parent', models.ForeignKey(on_delete=models.SET_NULL, default=None, editable=False, to='dbmconfigapp.PVMeasurementPage', null=True)),
                ('pv_parent_patient_display', models.ForeignKey(on_delete=models.SET_NULL, default=None, editable=False, to='dbmconfigapp.PVPatientDisplayPage', null=True)),
                ('reporting_cv', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.CVReportingPage', null=True)),
                ('reporting_pl', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.PlReportingPage', null=True)),
                ('reporting_pv', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.PVReportingPage', null=True)),
            ],
            options={
                'history_meta_label': 'Business Rules',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VpoCommon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clinical_data_display_options', models.IntegerField(default=0, help_text=b'Determines how clinical data is displayed in the Clinical Viewer.<br/>This configuration affects the Clinical Viewer page and all the reports.<br/>The behavior of this parameter depends on the Local/Baseline/Calculated property definitions and the value of the &lt;clinical view domain&gt;_LocalCodeDisplayPriorities parameter as configured for that page.<br/>If the displayName in the original message received from the customer, is different from the value that is returned after the calculation, the system behaves as follows:<br/>First option: Only the returned calculated value is displayed on the page.<br/>Second option: The displayName from the original message is added in brackets (concatenated) to the calculated value.<br/>This parameter is relevant for the following clinical data fields:<br/>- Summary page Allergy grid: Allergy To<br/>- Summary page Problems grid: Problem<br/>- Summary page Labs grid: Test<br/>- Daily Summary page Labs grid: Test<br/>- Problem List grid: Problem<br/>- Allergies page Allergies grid: Allergy To<br/>- Immunizations page Immunizations grid: Name<br/>- Labs page Labs grid: Test<br/>- Lab Results page Labs Results grid: Test<br/>- Diagnoses page Diagnoses grid: Diagnosis<br/>- Procedures page Procedures grid: Procedure<br/>- Daily Summary Procedures grid: Procedure<br/><i>Default: Only the returned calculated value is displayed on the page</i>', null=True, verbose_name=b'Concatenate Display Name', choices=[(0, b'Only the returned calculated value is displayed on the page'), (1, b'The displayName from the original message is added in brackets (concatenated) to the calculated value')])),
                ('code_system_name_display', models.IntegerField(default=0, help_text=b'Determines how to display the CodeSystem name.<br/>This configuration affects the Clinical Viewer page and the Clinical Summary Selected Items report.<br/><i>Default: Display the CodeSystem Name only as a tooltip when the user hovers the cursor over the Code column</i>', verbose_name=b'CodeSystem name display within the Code column', choices=[(0, b'Display the CodeSystem Name only as a tooltip when the user hovers the cursor over the Code column'), (1, b'Display the CodeSystem Name in parentheses attached to the Code within the Code column')])),
                ('clinical_domain', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.ClinicalDomain', null=True)),
                ('cv_general', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.ClinicalViewerGeneralPage', null=True)),
                ('pl_parent', models.ForeignKey(on_delete=models.SET_NULL, default=None, editable=False, to='dbmconfigapp.PlGeneralPage', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VpoCommunication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_encounter_conf_inheritance', models.BooleanField(default=True, help_text=b'Determines whether to enable the inheritance from an encounter to its related acts.<br/>It also supports the inheritance of the encounter type code confidentiality to its related acts.<br/>This configuration affects Clinical viewer, Clinical View Agent, Patient View, SDK. In addition, supported when dbMotion serves as an XDS.b repository.<br/>For more information, look for "Data type level confidentiality" in the "Data Integration Layer Implementation Guide" <br/><i>Default: True</i>', verbose_name=b'Enable encounter confidentiality inheritance flow')),
                ('parent_cv_general', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.ClinicalViewerGeneralPage', null=True)),
                ('pl_parent', models.ForeignKey(on_delete=models.SET_NULL, default=None, editable=False, to='dbmconfigapp.PlGeneralPage', null=True)),
                ('pvp_parent', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.PatientViewPage', null=True)),
            ],
            options={
                'verbose_name': 'Confidentiality',
                'history_meta_label': 'Confidentiality',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VpoEHRAgent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('return_act_organization_as_unit', models.NullBooleanField(verbose_name=b"Display of the organization related to patient's clinical data")),
                ('use_org_type_mode', models.NullBooleanField(verbose_name=b'Calculating the Facility field')),
                ('facility_source', models.IntegerField(help_text=b'Determines how to calculate the organization shown in the Facility field.<br/>This configuration affects both Clinical Viewer and EHR Agent.<br/><i>Default: Display the first participant or parent organization that is defined by the INS (institute) code</i>', null=True, verbose_name=b'Calculation of the Facility field', choices=[(0, b'Display the first participant organization'), (1, b'Display the first parent of the first participant organization'), (2, b'Display the first participant or parent organization that is defined by the INS (institute) code')])),
                ('parent_cv_general', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.ClinicalViewerGeneralPage', null=True)),
                ('pl_parent', models.ForeignKey(on_delete=models.SET_NULL, default=None, editable=False, to='dbmconfigapp.PlGeneralPage', null=True)),
            ],
            options={
                'history_meta_label': 'Business Rules',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VpoEHRAgentDomains',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filter_codes', models.TextField(null=True, blank=True)),
                ('filter_type', models.SmallIntegerField(default=0, choices=[(0, b'Filter Out'), (1, b'Filter In')])),
                ('clinical_domain', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.ClinicalDomain', null=True)),
                ('pv_parent', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.PVClinicalDomainPage', null=True)),
            ],
            options={
                'history_meta_label': 'Filtering Clinical Data',
                'verbose_name_plural': 'Filtering Clinical Data',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VpoFacilityDisplay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(unique=True, max_length=60, verbose_name=b'Clinical Domain')),
                ('return_act_organization_as_unit', models.NullBooleanField(default=True, verbose_name=b"Display of the organization related to patient's clinical data")),
                ('use_org_type_mode', models.NullBooleanField(default=True, verbose_name=b'Calculating the Facility field')),
                ('facility_source', models.IntegerField(default=2, help_text=b'Determines how to calculate the organization shown in the Facility field.<br/>This configuration affects Clinical Viewer, EHR Agent, Patient View and Patient List. <br/><i>Default: Display the first participant or parent organization that is defined by the INS (institute) code</i>', verbose_name=b'Calculation of the Facility field', choices=[(0, b'Display the first participant organization'), (1, b'Display the first parent of the first participant organization'), (2, b'Display the first participant or parent organization that is defined by the INS (institute) code')])),
                ('clinical_domain', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.ClinicalDomain', null=True)),
                ('parent_cv_general', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.ClinicalViewerGeneralPage', null=True)),
                ('patient_view', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.PatientViewPage', null=True)),
                ('pl_parent', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.PlGeneralPage', null=True)),
            ],
            options={
                'history_meta_label': 'Facility Display Prioritization',
                'verbose_name_plural': 'Facility Display Prioritization',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VpoPPOL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_privacy_mask_ssn', models.IntegerField(default=0, help_text=b'This configuration applies to Clinical Viewer and Collaborate.<br/>Defines the number of SSN digits to display (masking the rest).<br/>For example, if the number is 4, then only the last 4 digits of the SSN will be displayed.<br/>This configuration affects the Identifiers grid in Demographics page and the Search Results grid in Patient Search page.<br/><i>Default: 4</i>', verbose_name=b'number of SSN digits to display', choices=[(-1, b'All'), (0, b'Do not display'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9')])),
                ('patient_privacy_remove_excluded_clusters', models.NullBooleanField(default=False, help_text=b'Determines whether the system does NOT return a patient cluster which includes at least one confidential patient index that the user does not have permission to see.<br/>If True, clusters with at least one confidential index that the user does not have permission to see will NOT be returned.<br/>If False, the cluster will be returned; however, the indexes that the user does not have permission to see will be disabled.<br/>This configuration is supported by CV and Agent Hub.<br/><i>Default: False</i>', verbose_name=b'Filter patient cluster when patient is partially confidential')),
                ('clinical_domain', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.ClinicalDomain', null=True)),
                ('cv_patient_display', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.CvPatientDisplayPage', null=True)),
                ('pl_patient_display', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.PlPatientDisplayPage', null=True)),
                ('pv_parent_patient_display', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.PVPatientDisplayPage', null=True)),
                ('pv_patient_display', models.ForeignKey(on_delete=models.SET_NULL, editable=False, to='dbmconfigapp.PVPatientSearchPage', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WebCulture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('culture', models.CharField(help_text=b'The culture that will be relevant to the date/time definition. For projects with a single language this can be left as default.', unique=True, max_length=10)),
                ('short_date_pattern', models.CharField(help_text=b'The date fields format presented in the clinical view and Patient List.', max_length=20, verbose_name=b'date format')),
                ('short_time_pattern', models.CharField(help_text=b'The time fields format presented in all the clinical views and Patient List.', max_length=20, verbose_name=b'time format')),
                ('long_time_pattern', models.CharField(help_text=b'The time fields format presented in PLV clinical view.', max_length=20, verbose_name=b'PLV time format')),
                ('date_separator', models.CharField(help_text=b'The date separator presented in the clinical view and Patient List.', max_length=10)),
                ('time_separator', models.CharField(help_text=b'The time separator presented in the clinical view and Patient List.', max_length=10)),
                ('cv_general_page', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.ClinicalViewerGeneralPage', null=True)),
            ],
            options={
                'verbose_name': 'Culture',
                'history_meta_label': 'Culture',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrefetchSettingsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable_prefetch', models.BooleanField(default=False, help_text=b'Determines whether to enable or disable Prefetch functionality.<br/><i>Default: False</i>', verbose_name=b'Enable Prefetch')),
                ('api_url', models.CharField(default=b'', help_text=b'URL for prefetch API cloud service<br/><i>Default: None</i>', max_length=400, verbose_name=b'Prefetch API cloud service:', blank=True)),
                ('api_subscription_key', dbmconfigapp.utils.encryption.EncryptedCharField(default=b'', help_text=b'Subscription key for prefetch API. The key is issued by the prefetch API Azure manager.<br/><i>Default: None</i><br/><b>Note:</b> this field will not be transferred in the export/import process.', max_length=400, verbose_name=b'Prefetch API subscription:', blank=True)),
                ('page', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.CarequalityIntegrationSettingsPage', null=True)),
            ],
            options={
                'verbose_name': 'Prefetch Settings',
                'history_meta_label': 'Prefetch Settings',
                'verbose_name_plural': 'Prefetch Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EHRAgentPastMedicalHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problem_is_past_medical_history_by_end_date', models.BooleanField(default=False, help_text=b'True: Problems will be considered as Medical History (MH) if one of the following exist:<br>- Problem has ended (Effective Time End Date < Today).<br>- Problem Observation Type is the MH baseline code (or is mapped to MH baseline code).<br>False: Problems will be considered as Medical History if Problem Observation Type is MH baseline code (or is mapped to MH baseline code).<br>Medical History baseline code: 2.16.840.1.113883.6.96|417662000<br/><i>Default: False</i>', verbose_name=b'Determined by Effective Time End Date')),
                ('cv_problem_parent', models.ForeignKey(on_delete=models.SET_NULL, default=2, editable=False, to='dbmconfigapp.ClinicalDomain', null=True)),
                ('pv_parent', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dbmconfigapp.PVClinicalDomainPage', null=True)),
            ],
            options={
                'history_meta_label': 'Medical History',
            },
            bases=(models.Model,),
        ),
    ]
