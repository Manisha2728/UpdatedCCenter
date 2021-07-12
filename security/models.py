from django.db import models
from dbmconfigapp.models.base import *
from django.core import validators
from federation.models import *
#from django.contrib.contenttypes import generic
from dbmconfigapp.utils import custom_validators, encryption
from django.db import connections, DEFAULT_DB_ALIAS
from django.contrib.auth.hashers import check_password, make_password

PAS_CHOICES_LOCAL = (
    (0, 'Disabled'),
    (1, 'Opt In and Most updated consent'),
    (2, 'Opt Out and Most updated consent'),
    (3, 'Opt In and Most restricted consent'),
    (4, 'Opt Out and Most restricted consent'),
    )

# Managed Users
class ADProviders(ConfigurationEntityBaseModel):
    domain_id = models.IntegerField(verbose_name='Domain Id', help_text="Defines the Domain Id.<br>Note: If the project was upgraded from an earlier release where the security configurations were performed in the Project Pack (prior to release 7.0),<br>you must make sure that the Domain ID configured here for the domain is identical to the Storage ID configured in the Project Pack configuration for this domain.<br>The PP configuration is located in the AD Providers worksheet in the Northwind Configuration Nodes Excel file.", unique=True)
    domain_name = models.CharField(verbose_name='Domain Name', unique=True, max_length=100, validators=[custom_validators.validate_not_ipv4], help_text="Defines the qualified name of the Active Directory.", default="")
    domain_port = models.IntegerField(blank=True, null=True, verbose_name='Port', validators=[custom_validators.validate_integer_is_more_than_0], max_length=20, help_text="Defines the port of the Active Directory.<br/>This value can be empty for the default port.", default=None)
    container = models.CharField(blank=True, null=True, max_length=200, verbose_name='Container', default="", help_text="Defines the Containers of the Active Directory (required only for clients that use AD containers).<br/>Containers are used to segment and organize a network (for users, groups, and so on). There is no default value.<br/>For Helios AD, the container is mandatory. <br/>Keywords are used to define the AD Containers. Keywords are not case sensitive and have the following meanings:<br/>cn: Common Name<br/>ou: Organizational Unit<br/>dc: Domain Component<br/>The following format should be used to define the AD Container:<br/>&lt;keyword&gt;=&lt;object&gt;,&lt;keyword&gt;=&lt;object&gt;.")
    untrusted_ad = models.BooleanField(default=False, verbose_name='Untrusted Active Directory', help_text=get_help_text('Defines an Active Directory in which there is not full trust between this AD and the dbMotion enterprise domain.<br/>The dbMotion security service account has no access to this directory domain and therefore its users are unknown to dbMotion.<br/>If an Active Directory is untrusted, its users can be accessed in dbMotion only by configuring the username and password of one of its members (impersonation).', 'False'))
    untrusted_ad_user_name = models.CharField(blank=True, null=True, max_length=100, verbose_name='Untrusted AD User Name', default="", help_text=get_help_text("Defines the User Name for the untrusted Active Directory.", add_no_export_note=True))
    untrusted_ad_user_password = encryption.EncryptedCharField(blank=True, null=True, max_length=100, verbose_name='Untrusted AD User Password', default="", help_text=get_help_text("Defines the User Password for the untrusted Active Directory.", add_no_export_note=True))
    netbios_domain_name = models.CharField(blank=True, null=True, max_length=100, verbose_name='NetBios Domain Name', default="", help_text="Enables users (who normally log in to applications with their AD Domain name or NetBios name) to access dbMotion applications.")
    helios = models.BooleanField(default=False, verbose_name='Helios', help_text=get_help_text('Determines whether the Active Directory is the Helios type.', 'False'))
    allow_alternative_authentication = models.BooleanField(default=True, verbose_name='Use SSL Binding Authentication Method', help_text=get_help_text('Determines whether SSL Binding is used for authentication of AD users logging in to dbMotion', 'True'))
    ad_mapping_FirstName = models.CharField(blank=True, null=True, max_length=100, verbose_name='First Name', default="givenName", help_text=get_help_text('Defines the AD user attribute that is mapped to the First Name User Profile property in the dbMotion Security Service.', 'givenName'))
    ad_mapping_LastName = models.CharField(blank=True, null=True, max_length=100, verbose_name='Last Name', default="sn", help_text=get_help_text('Defines the AD user attribute that is mapped to the Last Name User Profile property in the dbMotion Security Service.', 'sn'))
    
    ad_mapping_NationalIdNumber = models.CharField(blank=True, null=True, max_length=100, verbose_name='National Id Number', default="", help_text='Defines the AD user attribute that is mapped to the National Id Number Profile property in the dbMotion Security Service.')
    
    ad_mapping_Title = models.CharField(blank=True, null=True, max_length=100, verbose_name='Title', default="title", help_text=get_help_text('Defines the AD user attribute that is mapped to the Title property in the dbMotion Security Service.', 'title'))
    ad_mapping_Description = models.CharField(blank=True, null=True, max_length=100, verbose_name='Description', default="Description", help_text=get_help_text('Defines the AD user attribute that is mapped to the Description property in the dbMotion Security Service.', 'Description'))
    ad_mapping_Facility = models.CharField(blank=True, null=True, max_length=100, verbose_name='Facility', default="physicalDeliveryOfficeName", help_text=get_help_text('Defines the AD user attribute that is mapped to the Facility property in the dbMotion Security Service. This is required and relevant only when the Facility Based Filter is enabled by configuration.', 'physicalDeliveryOfficeName'))    
    use_dnl_format = models.BooleanField(default=False, verbose_name='Use the Down-Level Logon Name format', help_text=get_help_text('Determines whether DLN format will be used instead of UPN format for user name. The option will be disabled if NetBios Domain Name is empty.<br/> - DLN (Down-Level Logon Name): NETBIOS_DOMAIN_NAME\\USER_NAME <br/> - UPN (User Principal Name): USER_NAME@DOMAIN_NAME','False'))    

    def __unicode__(self):
        return self.domain_name
    
    def has_constraints(self):
        connection = connections[DEFAULT_DB_ALIAS]
        con = connection
        cur = con.cursor()
        cur.cursor.callproc('security_CheckDomainConstraints', [self.domain_id])
        answer = cur.cursor.fetchall()
         
        return answer[0][1]
    
    def set_password(self, raw_password):
        self.untrusted_ad_user_password = make_password(raw_password)
              
    class Meta:
        app_label = "security"
        verbose_name = 'Active Directory Provider'
        verbose_name_plural = 'Active Directory Providers Settings for Managed Users'
        history_meta_label = verbose_name_plural
        help_text = """
        This configuration is used to define the properties  of the Active Directory Domains for all Active Directories whose users require access to dbMotion.
        """


class SAMLIssuers(ConfigurationEntityBaseModel):
    domain_name = models.ForeignKey(ADProviders, on_delete=models.CASCADE, default=1)
    saml_issuer_name = models.CharField(max_length=256, verbose_name='SAML Issuer Name', default="", help_text='Defines the name of the Issuer of the SAML response Token before sending it to dbMotion. This name must be unique in the domain.')
    saml_certificate_thumbprint = models.CharField(max_length=100, default="", verbose_name='SAML Certificate Thumbprint', help_text="Defines the Thumbprint as found in the Certificate. The Certificate must be installed on the Windows Certificate store on the Local Machine, Personal folder.")
    
    def __unicode__(self):
        return self.saml_issuer_name
           
    class Meta:
        app_label = "security"
        verbose_name = 'SAML Issuers'
        verbose_name_plural = 'SAML Issuers Settings'
        history_meta_label = verbose_name_plural
        unique_together = ('domain_name', 'saml_issuer_name',)
        

# Unmanaged Users
class InternalRoles(ConfigurationEntityBaseModel):  
    role_name = models.CharField(max_length=100, default="", verbose_name='dbMotion Role', help_text="Defines the name of the role in dbMotion.", unique=True)

    def __unicode__(self):
        return self.role_name
           
    class Meta:
        app_label = "security"
        verbose_name = 'dbMotion Role'
        verbose_name_plural = 'dbMotion Roles Settings'
        history_meta_label = verbose_name_plural
         
class ApplicationDomains(ConfigurationEntityBaseModel):
    application_domain_qualifier = models.CharField(verbose_name='Application Domain Qualifier', max_length=100, help_text="Defines the qualified name of the external application domain. In most cases this is the NameQualifier sent in the SAML Assertion.", default="")
    default_role = models.ForeignKey(InternalRoles, on_delete=models.CASCADE, default=1, verbose_name='Default dbMotion Role', help_text="Defines the default role to set if the SAML Token does not contain the Role attribute or there is no Role Mappings defined to the given application ID / name.")
    
    def __unicode__(self):
        return self.application_domain_qualifier
           
    class Meta:
        app_label = "security"
        verbose_name = 'Application Domain Qualifier'
        verbose_name_plural = 'Application Domain Qualifier Settings for Unmanaged Users'
        history_meta_label = verbose_name_plural
        help_text = 'This configuration is used to authenticate unmanaged users who use Single Sign On (SSO) to access dbMotion applications; for example when launching dbMotion applications from their EHR.'

class SAMLIssuersUnmanaged(ConfigurationEntityBaseModel):
    application_domain_qualifier = models.ForeignKey(ApplicationDomains, on_delete=models.CASCADE, default=1)
    saml_issuer_name = models.CharField(max_length=256, verbose_name='SAML Issuer Name', default="", help_text='Defines the name of the Issuer of the SAML response Token before sending it to dbMotion. This name must be unique in the domain.')
    saml_certificate_thumbprint = models.CharField(max_length=100, default="", verbose_name='SAML Certificate Thumbprint', help_text="Defines the Thumbprint as found in the Certificate. The Certificate must be installed on the Windows Certificate store on the Local Machine, Personal folder.")
    
    def __unicode__(self):
        return self.saml_issuer_name
           
    class Meta:
        app_label = "security"
        verbose_name = 'SAML Issuers'
        verbose_name_plural = 'SAML Issuers Settings'
        history_meta_label = verbose_name_plural
        unique_together = ('application_domain_qualifier', 'saml_issuer_name',)

# Role Mapping
class Applications(ConfigurationEntityBaseModel):
    application_id = models.CharField(verbose_name='Application ID', max_length=100, help_text="Defines the OID or application name of the sending system. This name is used to determine which Role Mappings to use for unmanaged users authorization requests.", default="", unique=True)
    
    def __unicode__(self):
        return self.application_id
           
    class Meta:
        app_label = "security"
        verbose_name = 'Application Role Mapping'
        verbose_name_plural = 'Application Role Mapping Settings'
        history_meta_label = 'Application'
        help_text = 'This configuration is used to map the security roles for users in the sending system to dbMotion security roles.'

class RoleMapping(ConfigurationEntityBaseModel):
    application_id = models.ForeignKey(Applications, on_delete=models.CASCADE, default=1)
    external_role_name = models.CharField(max_length=100, verbose_name='External Application Role', default="", help_text='Defines the name of the role in the external application.')
    internal_role_name = models.ForeignKey(InternalRoles, on_delete=models.CASCADE, default=1, verbose_name='dbMotion Role', help_text="Defines the name of the role in dbMotion to which the external role will be mapped.")
    
    def __unicode__(self):
        return self.external_role_name
           
    class Meta:
        app_label = "security"
        verbose_name = 'Role Mapping'
        verbose_name_plural = 'Role Mapping'
        history_meta_label = verbose_name_plural
        unique_together = ('external_role_name', 'application_id',)

# General Definitions
class SecurityGeneralPage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "security"
        verbose_name = "Security General"
        verbose_name_plural = 'Security General'
        history_meta_label = verbose_name_plural


class SecurityGeneral(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(SecurityGeneralPage, on_delete=models.CASCADE, default=1)
    activate_facility_identification = models.BooleanField(verbose_name='Confidentiality Filter - User Facility Identification', default=False, help_text="Determines whether the Confidentiality Filter using User Facility Identification is enabled. If true, if the user role has a confidentiality permission (for example, Restricted) and the act has the equivalent act confidentiality (in this case, Restricted), the confidential data is displayed only if the act is related to the user's local facility. If false, confidential data is displayed, depending on the user role, from all nodes and facilities, regardless of the user's facility.<br><br><b>Important!</b> To enable the functionality in this section it is mandatory to configure the 'User Facility Identification' in the following CCenter page: Agent Hub -> EHR Integration -> EHR Instances -> User Facility Identification" + 
                                                                "<br><br><b>Note:</b> If this is configured as True, and the 'User Facility Identification' in the EHR Integration section is not configured or if the user logs into CV directly (and not through the EHR Agent), the user will not see confidential data at all.<br><br><em>Default: False</em>")
    facility_identification_excluded_codes = models.TextField(verbose_name='Codes Excluded from User Facility Confidentiality Filter', help_text="This configuration is used in conjunction with the following CCenter configuration: Confidentiality Filter - User Facility Identification. It is used to specify confidentiality codes that are not  filtered out by the User Facility Identification Filter.<br><br>This configuration defines the confidentiality codes (in Code System | Code ^ format) that the customer wants to exclude from the Confidentiality Filter - User Facility Identification. The Confidentiality Filter allows users to see confidential data only from the user's (configured) local facility.  However, codes configured here (for example, 2.16.840.1.113883.5.25|PSY^) will NOT be filtered out by the User Facility Identification Filter. Confidential data with these codes can be viewed by users with relevant permissions from all facilities.<br>Codes configured here must be in allowConfidentialityLevels configuration in the Security Management role profile.<br>", default="", blank=True)    
    active_encounter_validation_rule = models.BooleanField(verbose_name='Restricting Access to Patient File Based on Active Encounter', default=False , help_text="Determines (if true) whether a user will only be allowed to access and view a patient record if the patient has an Active Encounter that originated from the User Facility.<br><br>The User Facility is defined in the User Facility Identification CCenter configuration.<br><u>An Active Encounter is defined as one of the following:</u><br>&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;Encounter Act that has no end date or future end date.<br>&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;Encounter Act that ends within the number of days configured in the Security Role Profile (configured per Security Role).<br>The facility of the Encounter is taken from the CDR from the MessageWrapper.Sender Organization.<br><br><em><u>Note:</u>&nbsp;This functionality is relevant only for Israel Implementation that uses the 'Federated CDR' EMPI Adapter (configured in: EMPI&#8594; General Definitions)</em><br><br><em>Default: False</em><br>")
        
    def __unicode__(self):
        return 'General Definitions'
 
    class Meta:
        app_label = "security"
        verbose_name = "Security General"
        verbose_name_plural = 'Security General'
        history_meta_label = verbose_name_plural
        
class PatientAuthorization(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(SecurityGeneralPage, on_delete=models.CASCADE, default=1)
    pas_option_local = models.IntegerField(verbose_name='Defining Patient Consent Policy', choices=PAS_CHOICES_LOCAL, default=0, help_text=get_help_text('This configuration defines the Patient Consent Policy and how to resolve a Patient Authorization Record (PAR) conflict. A PAR conflict exists when a patient has multiple indexes and at least two indexes have a different consent value. This configuration is applied to Clinical Viewer, Collaborate, EHR Agent, and CAG applications.<br>This configuration is not relevant if Defining Patient Consent Policy is set to Disabled.<br>- Disabled: Determines whether the Patient Authorization Service (PAS) is disabled. If true (Disabled), the system does not apply a Patient Consent calculation when entering the Patient File in dbMotion applications. Patient Consent Policy is ignored.<br>- OptIn: Determines whether the OptIn Patient Consent Policy is applied. OptIn policy allows users to view patient data and enter the patient file only of those patients that explicitly agreed to give consent.<br>- OptOut: Determines whether the OptOut Patient Consent Policy is applied. OptOut policy allows users to view patient data and enter the patient file of either those patients that agreed to give consent or of patients that did not yet specify their consent (null Par) and consent is undefined.<br>- Most Updated Consent: Determines whether the Most Updated Consent Policy is applied. If true, when a patient has multiple indexes, Patient Consent Policy is applied according to the consent value in the most updated index of the patient cluster.<br>- Most Restricted Consent: Determines whether the Most Restricted Consent Policy is applied. If true, when a patient has multiple indexes, Patient Consent Policy is applied according to the consent value in all the indexes of the cluster. If even one index does not give consent, the user cannot enter the patient file.', 'Disabled'))

    def __unicode__(self):
        return 'Patient Authorization Settings'
 
    class Meta:
        app_label = "security"
        verbose_name = "Patient Authorization"
        verbose_name_plural = 'Patient Authorization'
        history_meta_label = verbose_name_plural

class PatientProviderRelationship(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(SecurityGeneralPage, on_delete=models.CASCADE, default=1)
    patient_provider_relationship = models.BooleanField(verbose_name='Add Psychiatric permission based on Provider - Patient relationship', default=False, help_text=get_help_text("Determines whether to allow members of the patient's Care Team to access the patient's psychiatric data by adding Psychiatric permissions (Code: Psy, Code System: 2.16.840.1.113883.5.25) to the Provider's security permissions.<br> The Patient-Provider relationship exists when both the Patient and the Provider are related to the same Care Team. The Provider's Care Team is managed as an Organization, which is defined as a Care Team if the Code ID (of the Organization)  is under the CareTeam sub domain. The Patient's Care Team is managed as a PrimaryCareProvider, which is defined as a Care Team if the Code ID (of the PrimaryCareProvider) is under the CareTeamLink subdomain.<br> To define the Provider's Care Team, the Provider's National ID value (configured in the Active Directory) is used to associate the Provider to the relevant Medical Staff Identifier (ID extension) in the CDR that defines the Provider's Care Team.<br> The configuration of the Provider's National ID value is performed in the following CCenter location:  Security > Managed Users > National ID.<br> To define the Medical Staff ID root, the EHR User Assigning Authority value must be configured in the following CCenter location: Agent Hub > EHR Integration > Properties Packages.<br> If the Patient and Provider have overlapping Care Team values,  this indicates that the Patient-Provider relationship exists. In this case the Psychiatric permission will be added to the User.", 'False'))
    
    def __unicode__(self):
        return ''
  
    class Meta:
        app_label = "security"
        verbose_name = "Patient Provider Relationship"
        verbose_name_plural = 'Patient Provider Relationship'
        history_meta_label = verbose_name_plural
        
