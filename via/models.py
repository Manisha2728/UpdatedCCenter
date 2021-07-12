# -*- coding: utf-8 -*-
from django.db import models
from dbmconfigapp.models.base import *
from django.core import validators
from federation.models import *
# from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from dbmconfigapp.utils import encryption
from configcenter.settings import get_param
import sys

_EMPI_TYPE_CHOICES = (
    ('Initiate', 'Initiate'),
    ('PDQ', 'PDQ'),
    ('DEMO', 'DEMO'),
    ('CDR', 'CDR'),
    ('FEDCDR', 'Federated CDR'),
                     )
HMO_CHOICES = (
    ('1', 'כללית'),
    ('2', 'מכבי'),
    ('3', 'מאוחדת'),
    ('4', 'לאומית'),
    ('5', 'צהל'),
                   )

_INITIATE_VERSION_CHOICES = (
    ('PatientAdapter92', '9.5, 9.7'),
#     ('PatientAdapter92', '9.7'),
    ('PatientAdapter100', '10.1, 11.4'),
                     )

_INITIATE_FILTER_CHOICES = (
    ('NONE', 'Exclude'),
    ('IN', 'VIA Input'),
    ('INOUT', 'VIA Input and Output'),
                     )

_SEGMENT_NAME_CHOICES = (
    ('memIdent', 'memIdent'),
    ('memName', 'memName'),
    ('memAddr', 'memAddr'),
    ('memAttr', 'memAttr'),
    ('memPhone', 'memPhone'),
    ('memDate', 'memDate'),
                     )

_SYSTEM_TYPE_CHOICES = (
    ('Real', 'Real'),
    ('Virtual', 'Virtual'),
    ('Virtual Replace Real', 'Virtual Replace Real'),
    ('Search Only', 'Search Only'),
    ('Virtual MPIID', 'Virtual MPIID'),
    ('Search Only MPIID', 'Search Only MPIID'),
                     )

PARSED_DATE_TIME_FORMAT_CHOICES = (
    ('yyyy-MM-dd', 'yyyy-MM-dd'),
    ('yyyy-MM-dd HH:mm', 'yyyy-MM-dd HH:mm')
    )

PCP_RELATION_OPTIONS_CHOICES = (
    (0, 'CDR aligned PCP relation strategy'),
    (1, 'Last Updated PCP relation strategy')
    )

class ViaPageModel:
    def page_title(self):
        return 'Set the %s Settings' % self._meta.verbose_name
    
class ViaPage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "via"
        verbose_name = 'VIA General'
        verbose_name_plural = 'VIA Settings'
        history_meta_label = verbose_name_plural
        
class AuthoritySystemsPage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "via"
        verbose_name = 'Authority Systems'
        verbose_name_plural = 'Authority Systems Settings'
        history_meta_label = verbose_name_plural

class Via(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(ViaPage, on_delete=models.CASCADE, default=1)
    systems_parent = models.ForeignKey('AuthoritySystemsPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    empi_type = models.CharField(verbose_name='EMPI Type', max_length=20, choices=_EMPI_TYPE_CHOICES, default=_EMPI_TYPE_CHOICES[0][0], help_text=get_help_text('Defines the EMPI connection type <br> *Federated CDR Relevant only in Israel.', _EMPI_TYPE_CHOICES[0][1]))
    hmo_id = models.CharField(verbose_name='HMO', max_length=20, choices=HMO_CHOICES, default=HMO_CHOICES[0][0], help_text=get_help_text("""
        In a Federated CDR, this configuration defines the HMO (Health Management Organization) in the local node.<br/>
        This configuration is used in conjunction with the Patient Consent Policy configuration (in the Security configurations) to determine how patient privacy is implemented in the local node.<br/>
        The following Patient Consent Policy options are available in a Federated CDR:<br/>
        - Disabled: Patient Consent Policy is ignored and all data can be accessed.<br/>
        - Opt Out: Patient data cannot be accessed of patients who belong to a different HMO and did not give consent. However, access to patient data from the same HMO is allowed even if the patient did not give consent.<br/>
        &nbsp;&nbsp;<b>Note</b>: If the HMO is configured as Null, entry to patient data is blocked for Opted Out patients (regardless of the patient HMO).<br/>
        - Opt In: In a Federated CDR this option SHOULD NOT BE SELECTED.<br/>
        <b>Note</b>: In order to for the change to take affect in the Patient Consent Admin Tool, please restart the DbmPatientConsentAdminPool Application Pool after changing this value.
        """), blank=True, null=True)
    hmo_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __unicode__(self):
        return self.empi_type
           
    class Meta:
        app_label = "via"
        verbose_name = 'EMPI General'
        verbose_name_plural = 'EMPI Type'
        history_meta_label = 'EMPI Type'
        
class ViaVpo(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(ViaPage, on_delete=models.CASCADE, default=1)
    vpo_personindex_dynamic_field_list_for_response = models.TextField(verbose_name='Person Index structure in VPO response', default='GNAME,FNAME,STATE,CITY,ADDR,GEN,BTHDAY,HOSP,PHONE,SSN,INSRNC,SRCINSRNC,ZIP,SENDFAC,SENDAPP,JHINMD,PAR_MDATE,PAR_CDATE,NONMASKSSN,LAST_MODIFIED_DATE', help_text=get_help_text('Defines the structure of the person index (demographic data as defined in the VPO request) returned to the VPO from VIA, as a comma-separated list.<br/>This list must be aligned with the VIA Attributes field in the EMPI Mapping (Patient) PP configuration.', 'GNAME,FNAME,STATE,CITY,ADDR,GEN,BTHDAY,HOSP,PHONE,SSN,INSRNC,SRCINSRNC,ZIP,SENDFAC,SENDAPP,JHINMD,PAR_MDATE,PAR_CDATE,NONMASKSSN,LAST_MODIFIED_DATE'))
    vpo_patient_entrance_apply_cluster_filter = models.BooleanField(default=True, verbose_name='VPO Federation Cluster Filter', help_text=get_help_text('In a dbMotion federated system, enables filtering out an MPI cluster that does not include at least one patient index from the local node.' , 'True'))

    def __unicode__(self):
        return 'Via VPO'
           
    class Meta:
        app_label = "via"
        verbose_name = 'EMPI VPO Settings'
        verbose_name_plural = 'EMPI VPO Settings'
        history_meta_label = 'EMPI VPO Settings'
        
        
class InitiatePage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "via"
        verbose_name = 'Initiate General'
        verbose_name_plural = 'Initiate Settings'
        history_meta_label = verbose_name_plural

class Initiate(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(InitiatePage, on_delete=models.CASCADE, default=1)
    patient_member_type = models.CharField(max_length=100, default='PERSON', help_text=get_help_text('The Initiate input parameter to define the member type in the MPI instance.<br/>A Member is a set of demographic information that represents one individual (for example, a Person).<br/>The value configured here (for example, Person) must be aligned with the Member value in the project\'s MPI.', 'PERSON')) 
    patient_entity_type = models.CharField(max_length=100, default='PATIENT', help_text=get_help_text('Defines the entity type in the MPI instance.<br/>An Entity is an attribute used for managing identities. It can have a value representing the relationship between two or more records or two members in a healthcare organization.<br/>For example, it can represent multiple patient records sharing one Enterprise ID.', 'PATIENT'))
    filter_active = models.CharField(verbose_name='Active Filter', max_length=20, choices=_INITIATE_FILTER_CHOICES, default=_INITIATE_FILTER_CHOICES[2][0], help_text=get_help_text('Defines the Active filter.<br/>Active status refers to the most current patient index in Initiate.', _INITIATE_FILTER_CHOICES[2][1]))
    filter_overlay = models.CharField(verbose_name='Overlay Filter', max_length=20, choices=_INITIATE_FILTER_CHOICES, default=_INITIATE_FILTER_CHOICES[0][0], help_text=get_help_text('Defines the Overlay filter.<br/>Overlay status refers to a patient index in Initiate that was overridden by another patient index.', _INITIATE_FILTER_CHOICES[0][1]))
    filter_merged = models.CharField(verbose_name='Merged Filter', max_length=20, choices=_INITIATE_FILTER_CHOICES, default=_INITIATE_FILTER_CHOICES[1][0], help_text=get_help_text('Defines the Merged filter.<br/>Merged status refers to a patient index that was merged to another patient index in Initiate.', _INITIATE_FILTER_CHOICES[1][1]))
    filter_deleted = models.CharField(verbose_name='Deleted Filter', max_length=20, choices=_INITIATE_FILTER_CHOICES, default=_INITIATE_FILTER_CHOICES[0][0], help_text=get_help_text('Defines the Deleted state filter.<br/>Deleted status refers to a patient index that is logically deleted in Initiate.', _INITIATE_FILTER_CHOICES[0][1]))
    filter_MinimumScoreThreshold = models.PositiveIntegerField(verbose_name='Minimum Score Threshold', default=5, help_text=get_help_text('Defines the minimum score assigned by Initiate to the Patient Search results below which the search results will be filtered out and not returned. The Score is calculated internally by Initiate on each index returned in Patient Search.  It represents the quality (reliability) of the response. The purpose of the configuration is to filter out indexes that have a low quality score.', 5))    
    
    patient_results_sort_order = models.CharField(max_length=100, default='-getRecMtime', help_text=get_help_text('Defines the sort order of the patient  indexes that are returned from the MPI to VIA (and to the clinical applications).<br/> for example, "-getRecMtime" ("-" indicates descending order, and "getRecMtime" refers to the patient index modification time).', '-getRecMtime'))
    empi_url_address_for_patient_identity_feed_v3 = models.CharField(verbose_name='EMPI URL for Patient Identity Feed V3', max_length=100, default='', null=True, blank=True, help_text=get_help_text('Defines the EMPI URL Address for Patient Identity Feed V3.', 'Empty'))
    set_isrealleading = models.BooleanField(default=False, verbose_name='Is Real Leading', help_text=get_help_text('Determines whether the Demographics search returns the Real (true) or Virtual index (false) as the leading patient index:<br/>- Virtual Index: An index that is generated from a source system (root and extension) in an additional identifier field (memIdent) of the patient\'s record in Initiate. A record can hold multiple identifier fields.<br/>- Real Index: An index that is generated from a full Initiate record.', 'False'))
    filter_mode = models.BooleanField(default=True, verbose_name='Filter Mode', help_text=get_help_text('Determines whether filter mode is enabled for the Search/Match operation.<br/>If enabled only known sources are searched (for better performance).<br>*In some cases of Initiate federation filter mode needs to be disabled in order to avoid searching for unknown sources.', 'True'))
    
    def __unicode__(self):
        return 'Initiate'
           
    class Meta:
        app_label = "via"
        verbose_name = 'Initiate'
        verbose_name_plural = 'Patient Hub Settings'
        history_meta_label = verbose_name_plural
        
class InitiateConnection(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(InitiatePage, on_delete=models.CASCADE, default=1)
    initiate_version = models.CharField(verbose_name='Initiate version', max_length=20, choices=_INITIATE_VERSION_CHOICES, default=_INITIATE_VERSION_CHOICES[1][0], help_text=get_help_text('Defines the Initiate version', _INITIATE_VERSION_CHOICES[1][1]))
    initiate_url = models.CharField(max_length=100, default='', help_text=get_help_text('Defines Initiate URL.', 'Empty'))
    patient_credential_username = models.CharField(verbose_name='VIA User Credentials: Username', max_length=100, default='system', help_text=get_help_text('VIA connections/operations with the MPI (for example, Patient Search, Match, Insert, Remove) require Username credentials, which must be provided by the MPI service to replace the default value.', 'system'))
    patient_credential_password = encryption.EncryptedCharField(verbose_name='VIA User Credentials: Password', max_length=100, default='system', help_text=get_help_text('VIA connections/operations with the MPI (for example, Patient Search, Match, Insert, Remove) require User credentials with a Password, which must be provided by the MPI service to replace the default value.', 'system'))
    
    def __unicode__(self):
        return 'Initiate'
           
    class Meta:
        app_label = "via"
        verbose_name = 'Initiate'
        verbose_name_plural = 'Initiate connection Settings'
        history_meta_label = verbose_name_plural
        

class InitiateVpo(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(InitiatePage, on_delete=models.CASCADE, default=1)
    enable_federated_search = models.BooleanField(default=False, help_text=get_help_text('Determines if the Federated Search functionality is enabled (through PHRED) in a federated Initiate environment.<br/>Note that the Minimum Score Threshold value must be configured with a high score as it is used both for filtering out indexes and also for linking all returned indexes to a single cluster.', 'False'))
    enable_federated_match = models.BooleanField(default=False, help_text=get_help_text('Determines if the Federated Match functionality is enabled (through PHRED) for matching Patient Records in a federated Initiate environment.', 'False'))
    
    def __unicode__(self):
        return 'Initiate'
           
    class Meta:
        app_label = "via"
        verbose_name = 'Initiate'
        verbose_name_plural = 'Federated Patient Hub Settings'
        history_meta_label = verbose_name_plural
        
        


class AuthoritySystems(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(AuthoritySystemsPage, on_delete=models.CASCADE, default=1)
    source_system_dbMotion_oid = models.CharField(verbose_name='Source System dbMotion OID', unique=True, max_length=200, help_text="Defines the Source System OID as represented in the CDR and that is used to retrieve the patient data from the CDR. This OID is not stored in the EMPI, but is mapped here to the EMPI Source System Name.")
    source_system_name = models.CharField(max_length=100, verbose_name='Source System Name', help_text="Defines the Source System Name as it is represented in the EMPI. It is a different value from the Source System dbMotion OID.")
    source_system_display_name = models.CharField(max_length=100, verbose_name='Source System Display Name', help_text="Defines Source System Name as it is displayed in the Patient Search Clinical View (PSCV) dropdown list and in the Search Results grid. This might be the same or different from the EMPI Source System Name.")
    display_for_search = models.BooleanField(default=True, verbose_name='Display For Search', help_text=get_help_text('Determines whether to display the Source System Display Name in the PSCV dropdown list. If not displayed, the user will not be able to search for a patient (with MRN Match operation) from this Source System.', 'True', 'True'))
    is_system_mandatory = models.BooleanField(default=False, verbose_name='Is System Mandatory', help_text=get_help_text('Describes whether this is a mandatory system index in Patient Search Results. Multiple Systems can be selected.', 'False', True))
    segment_name = models.CharField(max_length=100, verbose_name='Segment Name', blank=True, null=False , choices=_SEGMENT_NAME_CHOICES, help_text="If this Source System Type is Virtual, defines the Segment Name in the EMPI response that contains the Source System Name. This attribute is only relevant for Initiate EMPI. If the Source System Type is Real, this attribute is Not Applicable.")
    attribute_code = models.CharField(max_length=100, verbose_name='Attribute Code', blank=True, null=True, help_text="If this Source System Type is Virtual, defines the Attribute Code that contains the field that contains the Source System Name. This attribute is only relevant for Initiate EMPI. If the Source System Type is Real, this attribute is Not Applicable.")
    system_type = models.CharField(max_length=100, verbose_name='System Type', blank=False, null=False , choices=_SYSTEM_TYPE_CHOICES, default=_SYSTEM_TYPE_CHOICES[0][0], help_text="Defines the source system type in the VIA configuration.")
    dbmotion_node_id = models.ForeignKey(Node, on_delete=models.SET_NULL, default=1, blank=True, null=True, verbose_name='dbMotion Node Name', help_text="Defines the name of the dbMotion node in a federated system that is associated with this Source System. If a Source System is installed on multiple nodes, it must have a unique OID and a unique Source System Name for each node.")
    node_uid = models.CharField(max_length=100, blank=True, null=True)  # for federation import purpose only
    cluster_filter_indication = models.BooleanField(default=False, verbose_name='Cluster Filter Indication', help_text=get_help_text('Determines whether a cluster of patient indexes is filtered out and not returned when performing patient search. If all source systems are configured here as False (unchecked), the feature is disabled and all indexes are returned in the response to patient search. If the cluster contains at least one index from a source system configured here as True (checked), the entire cluster will be returned in the response. If the cluster contains only indexes from source systems configured here as False (unchecked), the entire cluster will be filtered out and will not be returned.', 'False', 'True'))
    application_name = models.CharField(max_length=100, verbose_name='Application Name', blank=True, null=True, help_text="Defines the sending Application name in a PDQ request. This is used so that the PDQ response will return patient indexes only from the defined Application.")
    facility_name = models.CharField(max_length=100, verbose_name='Facility Name', blank=True, null=True, help_text="Defines the sending Facility name in a PDQ request. This is used so that the PDQ response will return patient indexes only from the defined Facility.")
    organization_code = models.CharField(max_length=100, verbose_name='Organization Code', blank=True, null=True, help_text="Defines an Organization Code provided by the customer that is mapped to each Source System. This is used to support the Provider Facility Filter functionality.")
    is_default = models.BooleanField(default=False, verbose_name='Is Default System', help_text=get_help_text('Determines whether this is the default Source System displayed in the PSCV dropdown list. Only one Source System can be selected.', 'False', 'True'))

    def __unicode__(self):
        return self.source_system_name
    
    def clean(self):
        if self.system_type.find('Virtual', 0) != -1 and self.system_type.find('MPIID', 0) == -1 and (self.segment_name == '' or self.attribute_code == ''):
            raise ValidationError("Segment Name and Attribute Code are required when System Type is Virtual!") 
           
    class Meta:
        app_label = "via"
        verbose_name = 'Authority Systems'
        verbose_name_plural = 'Authority Systems Settings'
        history_meta_label = verbose_name_plural
        
class CCDAwithoutADTSystems (ConfigurationEntityBaseModel):
    parent = models.ForeignKey(AuthoritySystemsPage, on_delete=models.CASCADE, default=1)
    load_ccda_without_adt_sources = models.BooleanField(default=False, verbose_name='Load CCDA Without ADT Sources', help_text="Load CCDA without ADT virtual source systems for Untrusted System<br/>Determines whether 50 virtual Source Systems are defined in VIA to support CCDA without ADT from Untrusted Systems.<br/><i>Default: False</i>")
    
    def __unicode__(self):
        return 'CCDA Without ADT Settings'
           
    class Meta:
        app_label = "via"
        verbose_name = 'CCDA Without ADT Settings'
        verbose_name_plural = 'CCDA Without ADT Settings'
        history_meta_label = verbose_name_plural
        
class dbMotionSystem(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(AuthoritySystemsPage, on_delete=models.CASCADE, default=1)
    dbmotion_system = models.CharField(max_length=100, verbose_name='dbMotion Internal System', help_text="Defines dbMotion's internal system name, this system is for CCDA without ADT support.")
    dbmotion_system_node_id = models.ForeignKey(Node, on_delete=models.SET_NULL, default=1, blank=True, null=True, verbose_name='dbMotion Node Name', help_text="Defines the dbMotion node that is associated with this source.")
    node_uid = models.CharField(max_length=100, blank=True, null=True)  # for federation import purpose only

    def __unicode__(self):
        return self.dbmotion_system
           
    class Meta:
        app_label = "via"
        verbose_name = 'CCDA without ADT Real Source System'
        verbose_name_plural = 'CCDA without ADT Real Source System'
        history_meta_label = verbose_name_plural

class InitiateMappingsPage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "via"
        verbose_name = 'Initiate Mappings'
        verbose_name_plural = 'Initiate Mappings Settings'
        history_meta_label = verbose_name_plural

class InitiateMappings(ConfigurationEntityBaseModel):
    parent = models.ForeignKey(InitiateMappingsPage, on_delete=models.CASCADE, default=1)
    dbmotion_attribute_name = models.CharField(max_length=100, verbose_name='dbMotion Patient Attribute Name', help_text="Patient attribute name in dbMotion. These names are nonconfigurable, But new attributes can be added.")
    dbmotion_attribute_description = models.CharField(max_length=100, blank=True, null=True, verbose_name='dbMotion Patient Attribute Description', help_text="Description of the dbMotion patient attribute.")
    initiate_hub_segment_name = models.CharField(max_length=100, verbose_name='Initiate Segment Name', choices=_SEGMENT_NAME_CHOICES, default=_SEGMENT_NAME_CHOICES[0][0], help_text="The Segment in Initiate that contains this attribute value.")
    initiate_hub_attribute_code = models.CharField(max_length=100, verbose_name='Initiate Attribute Code', help_text="The Attribute Code in Initiate that contains this attribute value.")
    initiate_hub_field_name = models.CharField(max_length=100, verbose_name='Initiate Field Name', help_text="The Field in Initiate that contains this attribute value.")
    initiate_hub_id_issuer = models.CharField(max_length=100, blank=True, null=True, verbose_name='Initiate Id Issuer', help_text="Defines the issuer of the patient identifier.<br/>Relevant only for Initiate memIdent attributes.<br/>For example, Social Security Authority (SSA) is issuer of the SSN.")
    mapping_values = models.CharField(max_length=100, blank=True, null=True, verbose_name='dbMotion Initiate Mapping Values', help_text='Determines whether you can map values to the MPI and from the MPI, as follows: Yes=Y;No=N;')
    dbmotion_attribute_input = models.BooleanField(default=True, verbose_name='VIA Request', help_text='Determines whether this attribute will be used when VIA sends a Patient Search query to Initiate. If this attribute is true (checked), the Attribute Weight field MUST be configured.')
    dbmotion_attribute_output = models.BooleanField(default=True, verbose_name='VIA Response', help_text='Determines whether this attribute will be used in the output from VIA in response to a Patient Search query. For example, an attribute might be required for a Patient Search query but is not required in the response.')
    dbmotion_attribute_weight = models.FloatField(blank=True, null=True, validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)], verbose_name='Attribute Weight', help_text='Defines the weight of each attribute sent in a Patient Search query to Initiate. The sum of the attributes sent in a Patient Search query must be equal to or greater than the Minimum SQQ Score (configured on the Patient Search page). If the sum of attributes sent in the query is less than the configured SQQ Score, the query will not be sent to Initiate.')
    
    def __unicode__(self):
        return self.dbmotion_attribute_name
           
    class Meta:
        app_label = "via"
        verbose_name = 'Initiate Mappings'
        verbose_name_plural = 'Initiate Mappings Settings'
        history_meta_label = verbose_name_plural        

class EmpiPpolGeneralPage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "via"
        verbose_name= "Provider Registry"
        verbose_name_plural = 'Provider Registry Settings'
        history_meta_label = verbose_name_plural
