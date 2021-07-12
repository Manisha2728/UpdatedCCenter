# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import dbmconfigapp.utils.custom_validators
import dbmconfigapp.utils.encryption


class Migration(migrations.Migration):

    dependencies = [
        ('dbmconfigapp', '2120001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ADProviders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain_id', models.IntegerField(help_text=b'Defines the Domain Id.<br>Note: If the project was upgraded from an earlier release where the security configurations were performed in the Project Pack (prior to release 7.0),<br>you must make sure that the Domain ID configured here for the domain is identical to the Storage ID configured in the Project Pack configuration for this domain.<br>The PP configuration is located in the AD Providers worksheet in the Northwind Configuration Nodes Excel file.', unique=True, verbose_name=b'Domain Id')),
                ('domain_name', models.CharField(default=b'', max_length=100, validators=[dbmconfigapp.utils.custom_validators.validate_not_ipv4], help_text=b'Defines the qualified name of the Active Directory.', unique=True, verbose_name=b'Domain Name')),
                ('domain_port', models.IntegerField(default=None, validators=[dbmconfigapp.utils.custom_validators.validate_integer_is_more_than_0], max_length=20, blank=True, help_text=b'Defines the port of the Active Directory.<br/>This value can be empty for the default port.', null=True, verbose_name=b'Port')),
                ('container', models.CharField(default=b'', max_length=200, blank=True, help_text=b'Defines the Containers of the Active Directory (required only for clients that use AD containers).<br/>Containers are used to segment and organize a network (for users, groups, and so on). There is no default value.<br/>For Helios AD, the container is mandatory. <br/>Keywords are used to define the AD Containers. Keywords are not case sensitive and have the following meanings:<br/>cn: Common Name<br/>ou: Organizational Unit<br/>dc: Domain Component<br/>The following format should be used to define the AD Container:<br/>&lt;keyword&gt;=&lt;object&gt;,&lt;keyword&gt;=&lt;object&gt;.', null=True, verbose_name=b'Container')),
                ('untrusted_ad', models.BooleanField(default=False, help_text=b'Defines an Active Directory in which there is not full trust between this AD and the dbMotion enterprise domain.<br/>The dbMotion security service account has no access to this directory domain and therefore its users are unknown to dbMotion.<br/>If an Active Directory is untrusted, its users can be accessed in dbMotion only by configuring the username and password of one of its members (impersonation).<br/><i>Default: False</i>', verbose_name=b'Untrusted Active Directory')),
                ('untrusted_ad_user_name', models.CharField(default=b'', max_length=100, blank=True, help_text=b'Defines the User Name for the untrusted Active Directory.<br/><b>Note:</b> this field will not be transferred in the export/import process.', null=True, verbose_name=b'Untrusted AD User Name')),
                ('untrusted_ad_user_password', dbmconfigapp.utils.encryption.EncryptedCharField(default=b'', max_length=100, blank=True, help_text=b'Defines the User Password for the untrusted Active Directory.<br/><b>Note:</b> this field will not be transferred in the export/import process.', null=True, verbose_name=b'Untrusted AD User Password')),
                ('netbios_domain_name', models.CharField(default=b'', max_length=100, blank=True, help_text=b'Enables users (who normally log in to applications with their AD Domain name or NetBios name) to access dbMotion applications.', null=True, verbose_name=b'NetBios Domain Name')),
                ('helios', models.BooleanField(default=False, help_text=b'Determines whether the Active Directory is the Helios type.<br/><i>Default: False</i>', verbose_name=b'Helios')),
                ('allow_alternative_authentication', models.BooleanField(default=True, help_text=b'Determines whether SSL Binding is used for authentication of AD users logging in to dbMotion<br/><i>Default: True</i>', verbose_name=b'Use SSL Binding Authentication Method')),
                ('ad_mapping_FirstName', models.CharField(default=b'givenName', max_length=100, blank=True, help_text=b'Defines the AD user attribute that is mapped to the First Name User Profile property in the dbMotion Security Service.<br/><i>Default: givenName</i>', null=True, verbose_name=b'First Name')),
                ('ad_mapping_LastName', models.CharField(default=b'sn', max_length=100, blank=True, help_text=b'Defines the AD user attribute that is mapped to the Last Name User Profile property in the dbMotion Security Service.<br/><i>Default: sn</i>', null=True, verbose_name=b'Last Name')),
                ('ad_mapping_NationalIdNumber', models.CharField(default=b'', max_length=100, blank=True, help_text=b'Defines the AD user attribute that is mapped to the National Id Number Profile property in the dbMotion Security Service.', null=True, verbose_name=b'National Id Number')),
                ('ad_mapping_Title', models.CharField(default=b'title', max_length=100, blank=True, help_text=b'Defines the AD user attribute that is mapped to the Title property in the dbMotion Security Service.<br/><i>Default: title</i>', null=True, verbose_name=b'Title')),
                ('ad_mapping_Description', models.CharField(default=b'Description', max_length=100, blank=True, help_text=b'Defines the AD user attribute that is mapped to the Description property in the dbMotion Security Service.<br/><i>Default: Description</i>', null=True, verbose_name=b'Description')),
                ('ad_mapping_Facility', models.CharField(default=b'physicalDeliveryOfficeName', max_length=100, blank=True, help_text=b'Defines the AD user attribute that is mapped to the Facility property in the dbMotion Security Service. This is required and relevant only when the Facility Based Filter is enabled by configuration.<br/><i>Default: physicalDeliveryOfficeName</i>', null=True, verbose_name=b'Facility')),
                ('use_dnl_format', models.BooleanField(default=False, help_text=b'Determines whether DLN format will be used instead of UPN format for user name. The option will be disabled if NetBios Domain Name is empty.<br/> - DLN (Down-Level Logon Name): NETBIOS_DOMAIN_NAME\\USER_NAME <br/> - UPN (User Principal Name): USER_NAME@DOMAIN_NAME<br/><i>Default: False</i>', verbose_name=b'Use the Down-Level Logon Name format')),
            ],
            options={
                'help_text': '\n        This configuration is used to define the properties  of the Active Directory Domains for all Active Directories whose users require access to dbMotion.\n        ',
                'verbose_name': 'Active Directory Provider',
                'history_meta_label': 'Active Directory Providers Settings for Managed Users',
                'verbose_name_plural': 'Active Directory Providers Settings for Managed Users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationDomains',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application_domain_qualifier', models.CharField(default=b'', help_text=b'Defines the qualified name of the external application domain. In most cases this is the NameQualifier sent in the SAML Assertion.', max_length=100, verbose_name=b'Application Domain Qualifier')),
            ],
            options={
                'help_text': 'This configuration is used to authenticate unmanaged users who use Single Sign On (SSO) to access dbMotion applications; for example when launching dbMotion applications from their EHR.',
                'verbose_name': 'Application Domain Qualifier',
                'history_meta_label': 'Application Domain Qualifier Settings for Unmanaged Users',
                'verbose_name_plural': 'Application Domain Qualifier Settings for Unmanaged Users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application_id', models.CharField(default=b'', help_text=b'Defines the OID or application name of the sending system. This name is used to determine which Role Mappings to use for unmanaged users authorization requests.', unique=True, max_length=100, verbose_name=b'Application ID')),
            ],
            options={
                'help_text': 'This configuration is used to map the security roles for users in the sending system to dbMotion security roles.',
                'verbose_name': 'Application Role Mapping',
                'history_meta_label': 'Application',
                'verbose_name_plural': 'Application Role Mapping Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InternalRoles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_name', models.CharField(default=b'', help_text=b'Defines the name of the role in dbMotion.', unique=True, max_length=100, verbose_name=b'dbMotion Role')),
            ],
            options={
                'verbose_name': 'dbMotion Role',
                'history_meta_label': 'dbMotion Roles Settings',
                'verbose_name_plural': 'dbMotion Roles Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientAuthorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pas_option_local', models.IntegerField(default=0, help_text=b'This configuration defines the Patient Consent Policy and how to resolve a Patient Authorization Record (PAR) conflict. A PAR conflict exists when a patient has multiple indexes and at least two indexes have a different consent value. This configuration is applied to Clinical Viewer, Collaborate, EHR Agent, and CAG applications.<br>This configuration is not relevant if Defining Patient Consent Policy is set to Disabled.<br>- Disabled: Determines whether the Patient Authorization Service (PAS) is disabled. If true (Disabled), the system does not apply a Patient Consent calculation when entering the Patient File in dbMotion applications. Patient Consent Policy is ignored.<br>- OptIn: Determines whether the OptIn Patient Consent Policy is applied. OptIn policy allows users to view patient data and enter the patient file only of those patients that explicitly agreed to give consent.<br>- OptOut: Determines whether the OptOut Patient Consent Policy is applied. OptOut policy allows users to view patient data and enter the patient file of either those patients that agreed to give consent or of patients that did not yet specify their consent (null Par) and consent is undefined.<br>- Most Updated Consent: Determines whether the Most Updated Consent Policy is applied. If true, when a patient has multiple indexes, Patient Consent Policy is applied according to the consent value in the most updated index of the patient cluster.<br>- Most Restricted Consent: Determines whether the Most Restricted Consent Policy is applied. If true, when a patient has multiple indexes, Patient Consent Policy is applied according to the consent value in all the indexes of the cluster. If even one index does not give consent, the user cannot enter the patient file.<br/><i>Default: Disabled</i>', verbose_name=b'Defining Patient Consent Policy', choices=[(0, b'Disabled'), (1, b'Opt In and Most updated consent'), (2, b'Opt Out and Most updated consent'), (3, b'Opt In and Most restricted consent'), (4, b'Opt Out and Most restricted consent')])),
            ],
            options={
                'verbose_name': 'Patient Authorization',
                'history_meta_label': 'Patient Authorization',
                'verbose_name_plural': 'Patient Authorization',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PatientProviderRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_provider_relationship', models.BooleanField(default=False, help_text=b"Determines whether to allow members of the patient's Care Team to access the patient's psychiatric data by adding Psychiatric permissions (Code: Psy, Code System: 2.16.840.1.113883.5.25) to the Provider's security permissions.<br> The Patient-Provider relationship exists when both the Patient and the Provider are related to the same Care Team. The Provider's Care Team is managed as an Organization, which is defined as a Care Team if the Code ID (of the Organization)  is under the CareTeam sub domain. The Patient's Care Team is managed as a PrimaryCareProvider, which is defined as a Care Team if the Code ID (of the PrimaryCareProvider) is under the CareTeamLink subdomain.<br> To define the Provider's Care Team, the Provider's National ID value (configured in the Active Directory) is used to associate the Provider to the relevant Medical Staff Identifier (ID extension) in the CDR that defines the Provider's Care Team.<br> The configuration of the Provider's National ID value is performed in the following CCenter location:  Security > Managed Users > National ID.<br> To define the Medical Staff ID root, the EHR User Assigning Authority value must be configured in the following CCenter location: Agent Hub > EHR Integration > Properties Packages.<br> If the Patient and Provider have overlapping Care Team values,  this indicates that the Patient-Provider relationship exists. In this case the Psychiatric permission will be added to the User.<br/><i>Default: False</i>", verbose_name=b'Add Psychiatric permission based on Provider - Patient relationship')),
            ],
            options={
                'verbose_name': 'Patient Provider Relationship',
                'history_meta_label': 'Patient Provider Relationship',
                'verbose_name_plural': 'Patient Provider Relationship',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoleMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_role_name', models.CharField(default=b'', help_text=b'Defines the name of the role in the external application.', max_length=100, verbose_name=b'External Application Role')),
                ('application_id', models.ForeignKey(on_delete=models.CASCADE, default=1, to='security.Applications')),
                ('internal_role_name', models.ForeignKey(on_delete=models.CASCADE, default=1, verbose_name=b'dbMotion Role', to='security.InternalRoles', help_text=b'Defines the name of the role in dbMotion to which the external role will be mapped.')),
            ],
            options={
                'verbose_name': 'Role Mapping',
                'history_meta_label': 'Role Mapping',
                'verbose_name_plural': 'Role Mapping',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SAMLIssuers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('saml_issuer_name', models.CharField(default=b'', help_text=b'Defines the name of the Issuer of the SAML response Token before sending it to dbMotion. This name must be unique in the domain.', max_length=256, verbose_name=b'SAML Issuer Name')),
                ('saml_certificate_thumbprint', models.CharField(default=b'', help_text=b'Defines the Thumbprint as found in the Certificate. The Certificate must be installed on the Windows Certificate store on the Local Machine, Personal folder.', max_length=100, verbose_name=b'SAML Certificate Thumbprint')),
                ('domain_name', models.ForeignKey(on_delete=models.CASCADE, default=1, to='security.ADProviders')),
            ],
            options={
                'verbose_name': 'SAML Issuers',
                'history_meta_label': 'SAML Issuers Settings',
                'verbose_name_plural': 'SAML Issuers Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SAMLIssuersUnmanaged',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('saml_issuer_name', models.CharField(default=b'', help_text=b'Defines the name of the Issuer of the SAML response Token before sending it to dbMotion. This name must be unique in the domain.', max_length=256, verbose_name=b'SAML Issuer Name')),
                ('saml_certificate_thumbprint', models.CharField(default=b'', help_text=b'Defines the Thumbprint as found in the Certificate. The Certificate must be installed on the Windows Certificate store on the Local Machine, Personal folder.', max_length=100, verbose_name=b'SAML Certificate Thumbprint')),
                ('application_domain_qualifier', models.ForeignKey(on_delete=models.CASCADE, default=1, to='security.ApplicationDomains')),
            ],
            options={
                'verbose_name': 'SAML Issuers',
                'history_meta_label': 'SAML Issuers Settings',
                'verbose_name_plural': 'SAML Issuers Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecurityGeneral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activate_facility_identification', models.BooleanField(default=False, help_text=b"Determines whether the Confidentiality Filter using User Facility Identification is enabled. If true, if the user role has a confidentiality permission (for example, Restricted) and the act has the equivalent act confidentiality (in this case, Restricted), the confidential data is displayed only if the act is related to the user's local facility. If false, confidential data is displayed, depending on the user role, from all nodes and facilities, regardless of the user's facility.<br><br><b>Important!</b> To enable the functionality in this section it is mandatory to configure the 'User Facility Identification' in the following CCenter page: Agent Hub -> EHR Integration -> EHR Instances -> User Facility Identification<br><br><b>Note:</b> If this is configured as True, and the 'User Facility Identification' in the EHR Integration section is not configured or if the user logs into CV directly (and not through the EHR Agent), the user will not see confidential data at all.<br><br><em>Default: False</em>", verbose_name=b'Confidentiality Filter - User Facility Identification')),
                ('facility_identification_excluded_codes', models.TextField(default=b'', help_text=b"This configuration is used in conjunction with the following CCenter configuration: Confidentiality Filter - User Facility Identification. It is used to specify confidentiality codes that are not  filtered out by the User Facility Identification Filter.<br><br>This configuration defines the confidentiality codes (in Code System | Code ^ format) that the customer wants to exclude from the Confidentiality Filter - User Facility Identification. The Confidentiality Filter allows users to see confidential data only from the user's (configured) local facility.  However, codes configured here (for example, 2.16.840.1.113883.5.25|PSY^) will NOT be filtered out by the User Facility Identification Filter. Confidential data with these codes can be viewed by users with relevant permissions from all facilities.<br>Codes configured here must be in allowConfidentialityLevels configuration in the Security Management role profile.<br>", verbose_name=b'Codes Excluded from User Facility Confidentiality Filter', blank=True)),
                ('active_encounter_validation_rule', models.BooleanField(default=False, help_text=b"Determines (if true) whether a user will only be allowed to access and view a patient record if the patient has an Active Encounter that originated from the User Facility.<br><br>The User Facility is defined in the User Facility Identification CCenter configuration.<br><u>An Active Encounter is defined as one of the following:</u><br>&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;Encounter Act that has no end date or future end date.<br>&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;Encounter Act that ends within the number of days configured in the Security Role Profile (configured per Security Role).<br>The facility of the Encounter is taken from the CDR from the MessageWrapper.Sender Organization.<br><br><em><u>Note:</u>&nbsp;This functionality is relevant only for Israel Implementation that uses the 'Federated CDR' EMPI Adapter (configured in: EMPI&#8594; General Definitions)</em><br><br><em>Default: False</em><br>", verbose_name=b'Restricting Access to Patient File Based on Active Encounter')),
            ],
            options={
                'verbose_name': 'Security General',
                'history_meta_label': 'Security General',
                'verbose_name_plural': 'Security General',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecurityGeneralPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('components', models.ManyToManyField(to='dbmconfigapp.Component', null=True)),
                ('services', models.ManyToManyField(to='dbmconfigapp.Service', null=True)),
            ],
            options={
                'verbose_name': 'Security General',
                'history_meta_label': 'Security General',
                'verbose_name_plural': 'Security General',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='securitygeneral',
            name='parent',
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to='security.SecurityGeneralPage'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='samlissuersunmanaged',
            unique_together=set([('application_domain_qualifier', 'saml_issuer_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='samlissuers',
            unique_together=set([('domain_name', 'saml_issuer_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='rolemapping',
            unique_together=set([('external_role_name', 'application_id')]),
        ),
        migrations.AddField(
            model_name='patientproviderrelationship',
            name='parent',
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to='security.SecurityGeneralPage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patientauthorization',
            name='parent',
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to='security.SecurityGeneralPage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='applicationdomains',
            name='default_role',
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, verbose_name=b'Default dbMotion Role', to='security.InternalRoles', help_text=b'Defines the default role to set if the SAML Token does not contain the Role attribute or there is no Role Mappings defined to the given application ID / name.'),
            preserve_default=True,
        ),
    ]
