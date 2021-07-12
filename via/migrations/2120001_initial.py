# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import dbmconfigapp.utils.encryption


class Migration(migrations.Migration):

    dependencies = [
        ('dbmconfigapp', '2120001_initial'),
        ('federation', '2120001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthoritySystems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_system_dbMotion_oid', models.CharField(help_text=b'Defines the Source System OID as represented in the CDR and that is used to retrieve the patient data from the CDR. This OID is not stored in the EMPI, but is mapped here to the EMPI Source System Name.', unique=True, max_length=200, verbose_name=b'Source System dbMotion OID')),
                ('source_system_name', models.CharField(help_text=b'Defines the Source System Name as it is represented in the EMPI. It is a different value from the Source System dbMotion OID.', max_length=100, verbose_name=b'Source System Name')),
                ('source_system_display_name', models.CharField(help_text=b'Defines Source System Name as it is displayed in the Patient Search Clinical View (PSCV) dropdown list and in the Search Results grid. This might be the same or different from the EMPI Source System Name.', max_length=100, verbose_name=b'Source System Display Name')),
                ('display_for_search', models.BooleanField(default=True, help_text=b'Determines whether to display the Source System Display Name in the PSCV dropdown list. If not displayed, the user will not be able to search for a patient (with MRN Match operation) from this Source System.\n<i>Default: True</i>', verbose_name=b'Display For Search')),
                ('is_system_mandatory', models.BooleanField(default=False, help_text=b'Describes whether this is a mandatory system index in Patient Search Results. Multiple Systems can be selected.\n<i>Default: False</i>', verbose_name=b'Is System Mandatory')),
                ('segment_name', models.CharField(blank=True, help_text=b'If this Source System Type is Virtual, defines the Segment Name in the EMPI response that contains the Source System Name. This attribute is only relevant for Initiate EMPI. If the Source System Type is Real, this attribute is Not Applicable.', max_length=100, verbose_name=b'Segment Name', choices=[(b'memIdent', b'memIdent'), (b'memName', b'memName'), (b'memAddr', b'memAddr'), (b'memAttr', b'memAttr'), (b'memPhone', b'memPhone'), (b'memDate', b'memDate')])),
                ('attribute_code', models.CharField(help_text=b'If this Source System Type is Virtual, defines the Attribute Code that contains the field that contains the Source System Name. This attribute is only relevant for Initiate EMPI. If the Source System Type is Real, this attribute is Not Applicable.', max_length=100, null=True, verbose_name=b'Attribute Code', blank=True)),
                ('system_type', models.CharField(default=b'Real', help_text=b'Defines the source system type in the VIA configuration.', max_length=100, verbose_name=b'System Type', choices=[(b'Real', b'Real'), (b'Virtual', b'Virtual'), (b'Virtual Replace Real', b'Virtual Replace Real'), (b'Search Only', b'Search Only'), (b'Virtual MPIID', b'Virtual MPIID'), (b'Search Only MPIID', b'Search Only MPIID')])),
                ('node_uid', models.CharField(max_length=100, null=True, blank=True)),
                ('cluster_filter_indication', models.BooleanField(default=False, help_text=b'Determines whether a cluster of patient indexes is filtered out and not returned when performing patient search. If all source systems are configured here as False (unchecked), the feature is disabled and all indexes are returned in the response to patient search. If the cluster contains at least one index from a source system configured here as True (checked), the entire cluster will be returned in the response. If the cluster contains only indexes from source systems configured here as False (unchecked), the entire cluster will be filtered out and will not be returned.\n<i>Default: False</i>', verbose_name=b'Cluster Filter Indication')),
                ('application_name', models.CharField(help_text=b'Defines the sending Application name in a PDQ request. This is used so that the PDQ response will return patient indexes only from the defined Application.', max_length=100, null=True, verbose_name=b'Application Name', blank=True)),
                ('facility_name', models.CharField(help_text=b'Defines the sending Facility name in a PDQ request. This is used so that the PDQ response will return patient indexes only from the defined Facility.', max_length=100, null=True, verbose_name=b'Facility Name', blank=True)),
                ('organization_code', models.CharField(help_text=b'Defines an Organization Code provided by the customer that is mapped to each Source System. This is used to support the Provider Facility Filter functionality.', max_length=100, null=True, verbose_name=b'Organization Code', blank=True)),
                ('is_default', models.BooleanField(default=False, help_text=b'Determines whether this is the default Source System displayed in the PSCV dropdown list. Only one Source System can be selected.\n<i>Default: False</i>', verbose_name=b'Is Default System')),
                ('dbmotion_node_id', models.ForeignKey(on_delete=models.SET_NULL, default=1, to='federation.Node', blank=True, help_text=b'Defines the name of the dbMotion node in a federated system that is associated with this Source System. If a Source System is installed on multiple nodes, it must have a unique OID and a unique Source System Name for each node.', null=True, verbose_name=b'dbMotion Node Name')),
            ],
            options={
                'verbose_name': 'Authority Systems',
                'history_meta_label': 'Authority Systems Settings',
                'verbose_name_plural': 'Authority Systems Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthoritySystemsPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('components', models.ManyToManyField(to='dbmconfigapp.Component', null=True)),
                ('services', models.ManyToManyField(to='dbmconfigapp.Service', null=True)),
            ],
            options={
                'verbose_name': 'Authority Systems',
                'history_meta_label': 'Authority Systems Settings',
                'verbose_name_plural': 'Authority Systems Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CCDAwithoutADTSystems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('load_ccda_without_adt_sources', models.BooleanField(default=False, help_text=b'Load CCDA without ADT virtual source systems for Untrusted System<br/>Determines whether 50 virtual Source Systems are defined in VIA to support CCDA without ADT from Untrusted Systems.<br/><i>Default: False</i>', verbose_name=b'Load CCDA Without ADT Sources')),
                ('parent', models.ForeignKey(on_delete=models.CASCADE, default=1, to='via.AuthoritySystemsPage')),
            ],
            options={
                'verbose_name': 'CCDA Without ADT Settings',
                'history_meta_label': 'CCDA Without ADT Settings',
                'verbose_name_plural': 'CCDA Without ADT Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='dbMotionSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dbmotion_system', models.CharField(help_text=b"Defines dbMotion's internal system name, this system is for CCDA without ADT support.", max_length=100, verbose_name=b'dbMotion Internal System')),
                ('node_uid', models.CharField(max_length=100, null=True, blank=True)),
                ('dbmotion_system_node_id', models.ForeignKey(on_delete=models.SET_NULL, default=1, to='federation.Node', blank=True, help_text=b'Defines the dbMotion node that is associated with this source.', null=True, verbose_name=b'dbMotion Node Name')),
                ('parent', models.ForeignKey(on_delete=models.CASCADE, default=1, to='via.AuthoritySystemsPage')),
            ],
            options={
                'verbose_name': 'CCDA without ADT Real Source System',
                'history_meta_label': 'CCDA without ADT Real Source System',
                'verbose_name_plural': 'CCDA without ADT Real Source System',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmpiPpolGeneralPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('components', models.ManyToManyField(to='dbmconfigapp.Component', null=True)),
                ('services', models.ManyToManyField(to='dbmconfigapp.Service', null=True)),
            ],
            options={
                'verbose_name': 'Provider Registry',
                'history_meta_label': 'Provider Registry Settings',
                'verbose_name_plural': 'Provider Registry Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Initiate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_member_type', models.CharField(default=b'PERSON', help_text=b"The Initiate input parameter to define the member type in the MPI instance.<br/>A Member is a set of demographic information that represents one individual (for example, a Person).<br/>The value configured here (for example, Person) must be aligned with the Member value in the project's MPI.<br/><i>Default: PERSON</i>", max_length=100)),
                ('patient_entity_type', models.CharField(default=b'PATIENT', help_text=b'Defines the entity type in the MPI instance.<br/>An Entity is an attribute used for managing identities. It can have a value representing the relationship between two or more records or two members in a healthcare organization.<br/>For example, it can represent multiple patient records sharing one Enterprise ID.<br/><i>Default: PATIENT</i>', max_length=100)),
                ('filter_active', models.CharField(default=b'INOUT', help_text=b'Defines the Active filter.<br/>Active status refers to the most current patient index in Initiate.<br/><i>Default: VIA Input and Output</i>', max_length=20, verbose_name=b'Active Filter', choices=[(b'NONE', b'Exclude'), (b'IN', b'VIA Input'), (b'INOUT', b'VIA Input and Output')])),
                ('filter_overlay', models.CharField(default=b'NONE', help_text=b'Defines the Overlay filter.<br/>Overlay status refers to a patient index in Initiate that was overridden by another patient index.<br/><i>Default: Exclude</i>', max_length=20, verbose_name=b'Overlay Filter', choices=[(b'NONE', b'Exclude'), (b'IN', b'VIA Input'), (b'INOUT', b'VIA Input and Output')])),
                ('filter_merged', models.CharField(default=b'IN', help_text=b'Defines the Merged filter.<br/>Merged status refers to a patient index that was merged to another patient index in Initiate.<br/><i>Default: VIA Input</i>', max_length=20, verbose_name=b'Merged Filter', choices=[(b'NONE', b'Exclude'), (b'IN', b'VIA Input'), (b'INOUT', b'VIA Input and Output')])),
                ('filter_deleted', models.CharField(default=b'NONE', help_text=b'Defines the Deleted state filter.<br/>Deleted status refers to a patient index that is logically deleted in Initiate.<br/><i>Default: Exclude</i>', max_length=20, verbose_name=b'Deleted Filter', choices=[(b'NONE', b'Exclude'), (b'IN', b'VIA Input'), (b'INOUT', b'VIA Input and Output')])),
                ('filter_MinimumScoreThreshold', models.PositiveIntegerField(default=5, help_text=b'Defines the minimum score assigned by Initiate to the Patient Search results below which the search results will be filtered out and not returned. The Score is calculated internally by Initiate on each index returned in Patient Search.  It represents the quality (reliability) of the response. The purpose of the configuration is to filter out indexes that have a low quality score.<br/><i>Default: 5</i>', verbose_name=b'Minimum Score Threshold')),
                ('patient_results_sort_order', models.CharField(default=b'-getRecMtime', help_text=b'Defines the sort order of the patient  indexes that are returned from the MPI to VIA (and to the clinical applications).<br/> for example, "-getRecMtime" ("-" indicates descending order, and "getRecMtime" refers to the patient index modification time).<br/><i>Default: -getRecMtime</i>', max_length=100)),
                ('empi_url_address_for_patient_identity_feed_v3', models.CharField(default=b'', max_length=100, blank=True, help_text=b'Defines the EMPI URL Address for Patient Identity Feed V3.<br/><i>Default: Empty</i>', null=True, verbose_name=b'EMPI URL for Patient Identity Feed V3')),
                ('set_isrealleading', models.BooleanField(default=False, help_text=b"Determines whether the Demographics search returns the Real (true) or Virtual index (false) as the leading patient index:<br/>- Virtual Index: An index that is generated from a source system (root and extension) in an additional identifier field (memIdent) of the patient's record in Initiate. A record can hold multiple identifier fields.<br/>- Real Index: An index that is generated from a full Initiate record.<br/><i>Default: False</i>", verbose_name=b'Is Real Leading')),
                ('filter_mode', models.BooleanField(default=True, help_text=b'Determines whether filter mode is enabled for the Search/Match operation.<br/>If enabled only known sources are searched (for better performance).<br>*In some cases of Initiate federation filter mode needs to be disabled in order to avoid searching for unknown sources.<br/><i>Default: True</i>', verbose_name=b'Filter Mode')),
            ],
            options={
                'verbose_name': 'Initiate',
                'history_meta_label': 'Patient Hub Settings',
                'verbose_name_plural': 'Patient Hub Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InitiateConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('initiate_version', models.CharField(default=b'PatientAdapter100', help_text=b'Defines the Initiate version<br/><i>Default: 10.1, 11.4</i>', max_length=20, verbose_name=b'Initiate version', choices=[(b'PatientAdapter92', b'9.5, 9.7'), (b'PatientAdapter100', b'10.1, 11.4')])),
                ('initiate_url', models.CharField(default=b'', help_text=b'Defines Initiate URL.<br/><i>Default: Empty</i>', max_length=100)),
                ('patient_credential_username', models.CharField(default=b'system', help_text=b'VIA connections/operations with the MPI (for example, Patient Search, Match, Insert, Remove) require Username credentials, which must be provided by the MPI service to replace the default value.<br/><i>Default: system</i>', max_length=100, verbose_name=b'VIA User Credentials: Username')),
                ('patient_credential_password', dbmconfigapp.utils.encryption.EncryptedCharField(default=b'system', help_text=b'VIA connections/operations with the MPI (for example, Patient Search, Match, Insert, Remove) require User credentials with a Password, which must be provided by the MPI service to replace the default value.<br/><i>Default: system</i>', max_length=100, verbose_name=b'VIA User Credentials: Password')),
            ],
            options={
                'verbose_name': 'Initiate',
                'history_meta_label': 'Initiate connection Settings',
                'verbose_name_plural': 'Initiate connection Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InitiateMappings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dbmotion_attribute_name', models.CharField(help_text=b'Patient attribute name in dbMotion. These names are nonconfigurable, But new attributes can be added.', max_length=100, verbose_name=b'dbMotion Patient Attribute Name')),
                ('dbmotion_attribute_description', models.CharField(help_text=b'Description of the dbMotion patient attribute.', max_length=100, null=True, verbose_name=b'dbMotion Patient Attribute Description', blank=True)),
                ('initiate_hub_segment_name', models.CharField(default=b'memIdent', help_text=b'The Segment in Initiate that contains this attribute value.', max_length=100, verbose_name=b'Initiate Segment Name', choices=[(b'memIdent', b'memIdent'), (b'memName', b'memName'), (b'memAddr', b'memAddr'), (b'memAttr', b'memAttr'), (b'memPhone', b'memPhone'), (b'memDate', b'memDate')])),
                ('initiate_hub_attribute_code', models.CharField(help_text=b'The Attribute Code in Initiate that contains this attribute value.', max_length=100, verbose_name=b'Initiate Attribute Code')),
                ('initiate_hub_field_name', models.CharField(help_text=b'The Field in Initiate that contains this attribute value.', max_length=100, verbose_name=b'Initiate Field Name')),
                ('initiate_hub_id_issuer', models.CharField(help_text=b'Defines the issuer of the patient identifier.<br/>Relevant only for Initiate memIdent attributes.<br/>For example, Social Security Authority (SSA) is issuer of the SSN.', max_length=100, null=True, verbose_name=b'Initiate Id Issuer', blank=True)),
                ('mapping_values', models.CharField(help_text=b'Determines whether you can map values to the MPI and from the MPI, as follows: Yes=Y;No=N;', max_length=100, null=True, verbose_name=b'dbMotion Initiate Mapping Values', blank=True)),
                ('dbmotion_attribute_input', models.BooleanField(default=True, help_text=b'Determines whether this attribute will be used when VIA sends a Patient Search query to Initiate. If this attribute is true (checked), the Attribute Weight field MUST be configured.', verbose_name=b'VIA Request')),
                ('dbmotion_attribute_output', models.BooleanField(default=True, help_text=b'Determines whether this attribute will be used in the output from VIA in response to a Patient Search query. For example, an attribute might be required for a Patient Search query but is not required in the response.', verbose_name=b'VIA Response')),
                ('dbmotion_attribute_weight', models.FloatField(blank=True, help_text=b'Defines the weight of each attribute sent in a Patient Search query to Initiate. The sum of the attributes sent in a Patient Search query must be equal to or greater than the Minimum SQQ Score (configured on the Patient Search page). If the sum of attributes sent in the query is less than the configured SQQ Score, the query will not be sent to Initiate.', null=True, verbose_name=b'Attribute Weight', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
            options={
                'verbose_name': 'Initiate Mappings',
                'history_meta_label': 'Initiate Mappings Settings',
                'verbose_name_plural': 'Initiate Mappings Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InitiateMappingsPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('components', models.ManyToManyField(to='dbmconfigapp.Component', null=True)),
                ('services', models.ManyToManyField(to='dbmconfigapp.Service', null=True)),
            ],
            options={
                'verbose_name': 'Initiate Mappings',
                'history_meta_label': 'Initiate Mappings Settings',
                'verbose_name_plural': 'Initiate Mappings Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InitiatePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('components', models.ManyToManyField(to='dbmconfigapp.Component', null=True)),
                ('services', models.ManyToManyField(to='dbmconfigapp.Service', null=True)),
            ],
            options={
                'verbose_name': 'Initiate General',
                'history_meta_label': 'Initiate Settings',
                'verbose_name_plural': 'Initiate Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InitiateVpo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable_federated_search', models.BooleanField(default=False, help_text=b'Determines if the Federated Search functionality is enabled (through PHRED) in a federated Initiate environment.<br/>Note that the Minimum Score Threshold value must be configured with a high score as it is used both for filtering out indexes and also for linking all returned indexes to a single cluster.<br/><i>Default: False</i>')),
                ('enable_federated_match', models.BooleanField(default=False, help_text=b'Determines if the Federated Match functionality is enabled (through PHRED) for matching Patient Records in a federated Initiate environment.<br/><i>Default: False</i>')),
                ('parent', models.ForeignKey(on_delete=models.CASCADE, default=1, to='via.InitiatePage')),
            ],
            options={
                'verbose_name': 'Initiate',
                'history_meta_label': 'Federated Patient Hub Settings',
                'verbose_name_plural': 'Federated Patient Hub Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Via',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('empi_type', models.CharField(default=b'Initiate', help_text=b'Defines the EMPI connection type <br> *Federated CDR Relevant only in Israel.<br/><i>Default: Initiate</i>', max_length=20, verbose_name=b'EMPI Type', choices=[(b'Initiate', b'Initiate'), (b'PDQ', b'PDQ'), (b'DEMO', b'DEMO'), (b'CDR', b'CDR'), (b'FEDCDR', b'Federated CDR')])),
                ('hmo_id', models.CharField(default=b'1', choices=[(b'1', b'\xd7\x9b\xd7\x9c\xd7\x9c\xd7\x99\xd7\xaa'), (b'2', b'\xd7\x9e\xd7\x9b\xd7\x91\xd7\x99'), (b'3', b'\xd7\x9e\xd7\x90\xd7\x95\xd7\x97\xd7\x93\xd7\xaa'), (b'4', b'\xd7\x9c\xd7\x90\xd7\x95\xd7\x9e\xd7\x99\xd7\xaa'), (b'5', b'\xd7\xa6\xd7\x94\xd7\x9c')], max_length=20, blank=True, help_text=b'\n        In a Federated CDR, this configuration defines the HMO (Health Management Organization) in the local node.<br/>\n        This configuration is used in conjunction with the Patient Consent Policy configuration (in the Security configurations) to determine how patient privacy is implemented in the local node.<br/>\n        The following Patient Consent Policy options are available in a Federated CDR:<br/>\n        - Disabled: Patient Consent Policy is ignored and all data can be accessed.<br/>\n        - Opt Out: Patient data cannot be accessed of patients who belong to a different HMO and did not give consent. However, access to patient data from the same HMO is allowed even if the patient did not give consent.<br/>\n        &nbsp;&nbsp;<b>Note</b>: If the HMO is configured as Null, entry to patient data is blocked for Opted Out patients (regardless of the patient HMO).<br/>\n        - Opt In: In a Federated CDR this option SHOULD NOT BE SELECTED.<br/>\n        <b>Note</b>: In order to for the change to take affect in the Patient Consent Admin Tool, please restart the DbmPatientConsentAdminPool Application Pool after changing this value.\n        ', null=True, verbose_name=b'HMO')),
                ('hmo_name', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'EMPI General',
                'history_meta_label': 'EMPI Type',
                'verbose_name_plural': 'EMPI Type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ViaPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('components', models.ManyToManyField(to='dbmconfigapp.Component', null=True)),
                ('services', models.ManyToManyField(to='dbmconfigapp.Service', null=True)),
            ],
            options={
                'verbose_name': 'VIA General',
                'history_meta_label': 'VIA Settings',
                'verbose_name_plural': 'VIA Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ViaVpo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vpo_personindex_dynamic_field_list_for_response', models.TextField(default=b'GNAME,FNAME,STATE,CITY,ADDR,GEN,BTHDAY,HOSP,PHONE,SSN,INSRNC,SRCINSRNC,ZIP,SENDFAC,SENDAPP,JHINMD,PAR_MDATE,PAR_CDATE,NONMASKSSN,LAST_MODIFIED_DATE', help_text=b'Defines the structure of the person index (demographic data as defined in the VPO request) returned to the VPO from VIA, as a comma-separated list.<br/>This list must be aligned with the VIA Attributes field in the EMPI Mapping (Patient) PP configuration.<br/><i>Default: GNAME,FNAME,STATE,CITY,ADDR,GEN,BTHDAY,HOSP,PHONE,SSN,INSRNC,SRCINSRNC,ZIP,SENDFAC,SENDAPP,JHINMD,PAR_MDATE,PAR_CDATE,NONMASKSSN,LAST_MODIFIED_DATE</i>', verbose_name=b'Person Index structure in VPO response')),
                ('vpo_patient_entrance_apply_cluster_filter', models.BooleanField(default=True, help_text=b'In a dbMotion federated system, enables filtering out an MPI cluster that does not include at least one patient index from the local node.<br/><i>Default: True</i>', verbose_name=b'VPO Federation Cluster Filter')),
                ('parent', models.ForeignKey(on_delete=models.CASCADE, default=1, to='via.ViaPage')),
            ],
            options={
                'verbose_name': 'EMPI VPO Settings',
                'history_meta_label': 'EMPI VPO Settings',
                'verbose_name_plural': 'EMPI VPO Settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='via',
            name='parent',
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to='via.ViaPage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='via',
            name='systems_parent',
            field=models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='via.AuthoritySystemsPage', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='initiatemappings',
            name='parent',
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to='via.InitiateMappingsPage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='initiateconnection',
            name='parent',
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to='via.InitiatePage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='initiate',
            name='parent',
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to='via.InitiatePage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='authoritysystems',
            name='parent',
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to='via.AuthoritySystemsPage'),
            preserve_default=True,
        ),
    ]
