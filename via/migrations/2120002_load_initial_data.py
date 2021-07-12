# -*- coding: utf-8 -*-
# Auto generated using CCenter command smart_migrate
from __future__ import unicode_literals

from django.db import migrations, connection
from dbmconfigapp.models import add_to_model_descriptor2
from dbmconfigapp.utils import modelsfactory
from dbmconfigapp.utils.modelsfactory import get_components_by_name

VERSION = '21.2'

def forward(apps, schema_editor):

    load_AuthoritySystemsPage_data(apps, schema_editor)
    load_EmpiPpolGeneralPage_data(apps, schema_editor)
    load_InitiateMappingsPage_data(apps, schema_editor)
    load_InitiatePage_data(apps, schema_editor)
    load_ViaPage_data(apps, schema_editor)

    pass

def backward(apps, schema_editor):
    pass

def load_AuthoritySystemsPage_data(apps, schema_editor):

    page = modelsfactory.createPage(apps.get_model('via', 'AuthoritySystemsPage')(),
                                            "",
                                            "",
                                            "via_authoritysystems",
                                            [], [])

    model = apps.get_model('via', 'AuthoritySystems')()
    model.source_system_dbMotion_oid = '2.16.840.1.113883.3.57.1.3.5.52.1.8.6'
    model.source_system_name = 'EPIC'
    model.source_system_display_name = 'EPIC'
    model.save()

    add_to_model_descriptor2('via_authoritysystems', ['ClinicalViewer','CVA','VPO','Via'])

    model = apps.get_model('via', 'dbMotionSystem')()
    model.dbmotion_system = 'DBMOTION'
    model.save()

    add_to_model_descriptor2('via_dbmotionsystem', ['Via'])

    model = apps.get_model('via', 'CCDAwithoutADTSystems')()
    model.save()

    add_to_model_descriptor2('via_ccdawithoutadtsystems', ['Via'])

def load_EmpiPpolGeneralPage_data(apps, schema_editor):

    page = modelsfactory.createPage(apps.get_model('via', 'EmpiPpolGeneralPage')(),
                                            "",
                                            "",
                                            "via_ppolgeneral",
                                            [], get_components_by_name(apps, ['Population Health', 'Patient View']))

    model = apps.get_model('dbmconfigapp', 'PpolGeneral')()
    model.save()

    add_to_model_descriptor2('dbmconfigapp_ppolgeneral', ['PPOL'])

    # Could not update foreign key to different application by model
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE dbmconfigapp_ppolgeneral SET parent_empi_id_id=1;")


def load_InitiateMappingsPage_data(apps, schema_editor):

    page = modelsfactory.createPage(apps.get_model('via', 'InitiateMappingsPage')(),
                                            "",
                                            "",
                                            "via_initiatemappings",
                                            [], [])

    InitiateMappings = apps.get_model("via", "InitiateMappings")
    db_alias = schema_editor.connection.alias

    InitiateMappings.objects.using(db_alias).bulk_create([
InitiateMappings(pk=1,dbmotion_attribute_name="GNAME",dbmotion_attribute_description="Given Name",initiate_hub_segment_name="memName",initiate_hub_attribute_code="PATNAME",initiate_hub_field_name="onmFirst",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=25),
InitiateMappings(pk=2,dbmotion_attribute_name="MNAME",dbmotion_attribute_description="Middle Initials",initiate_hub_segment_name="memName",initiate_hub_attribute_code="PATNAME",initiate_hub_field_name="onmMiddle",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=25),
InitiateMappings(pk=3,dbmotion_attribute_name="FNAME",dbmotion_attribute_description="Family Name",initiate_hub_segment_name="memName",initiate_hub_attribute_code="PATNAME",initiate_hub_field_name="onmLast",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=25),
InitiateMappings(pk=4,dbmotion_attribute_name="PRENAME",dbmotion_attribute_description="Patient Prefix",initiate_hub_segment_name="memName",initiate_hub_attribute_code="PATNAME",initiate_hub_field_name="onmPrefix",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=5),
InitiateMappings(pk=5,dbmotion_attribute_name="SUFNAME",dbmotion_attribute_description="Patient Suffix",initiate_hub_segment_name="memName",initiate_hub_attribute_code="PATNAME",initiate_hub_field_name="onmSuffix",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=5),
InitiateMappings(pk=6,dbmotion_attribute_name="MMNAME",dbmotion_attribute_description="Mother Maiden Name",initiate_hub_segment_name="memAttr",initiate_hub_attribute_code="MOTHERMAIDNM",initiate_hub_field_name="attrVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=25),
InitiateMappings(pk=7,dbmotion_attribute_name="COUNTRY",dbmotion_attribute_description="Country",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="PATADDRESS",initiate_hub_field_name="country",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=0),
InitiateMappings(pk=8,dbmotion_attribute_name="STATE",dbmotion_attribute_description="State",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="PATADDRESS",initiate_hub_field_name="state",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=9,dbmotion_attribute_name="CITY",dbmotion_attribute_description="City",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="PATADDRESS",initiate_hub_field_name="city",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=10,dbmotion_attribute_name="ADDR",dbmotion_attribute_description="Patient Address 1",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="PATADDRESS",initiate_hub_field_name="stLine1",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=11,dbmotion_attribute_name="ADDRLINE2",dbmotion_attribute_description="Patient Address 2",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="PATADDRESS",initiate_hub_field_name="stLine2",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=12,dbmotion_attribute_name="ZIP",dbmotion_attribute_description="Zip Code",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="PATADDRESS",initiate_hub_field_name="zipCode",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=13,dbmotion_attribute_name="WORK COUNTRY",dbmotion_attribute_description="Work Country",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="WORKADDR",initiate_hub_field_name="country",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=0),
InitiateMappings(pk=14,dbmotion_attribute_name="WORK STATE",dbmotion_attribute_description="Work State",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="WORKADDR",initiate_hub_field_name="state",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=15,dbmotion_attribute_name="WORK CITY",dbmotion_attribute_description="Work City",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="WORKADDR",initiate_hub_field_name="city",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=16,dbmotion_attribute_name="WORK ADDRLINE1",dbmotion_attribute_description="Work Patient Address 1",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="WORKADDR",initiate_hub_field_name="stLine1",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=17,dbmotion_attribute_name="WORK ADDRLINE2",dbmotion_attribute_description="Work Patient Address 2",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="WORKADDR",initiate_hub_field_name="stLine2",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=18,dbmotion_attribute_name="WORK ZIP",dbmotion_attribute_description="Work Zip Code",initiate_hub_segment_name="memAddr",initiate_hub_attribute_code="WORKADDR",initiate_hub_field_name="zipCode",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=13),
InitiateMappings(pk=19,dbmotion_attribute_name="BTHDAY",dbmotion_attribute_description="DOB",initiate_hub_segment_name="memDate",initiate_hub_attribute_code="BIRTHDT",initiate_hub_field_name="dateVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=5),
InitiateMappings(pk=20,dbmotion_attribute_name="GEN",dbmotion_attribute_description="Gender",initiate_hub_segment_name="memAttr",initiate_hub_attribute_code="GENDER",initiate_hub_field_name="attrVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=5),
InitiateMappings(pk=21,dbmotion_attribute_name="PHONE",dbmotion_attribute_description="Home phone",initiate_hub_segment_name="memPhone",initiate_hub_attribute_code="HOMEPHONE",initiate_hub_field_name="phNumber",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=100),
InitiateMappings(pk=22,dbmotion_attribute_name="WPHONE",dbmotion_attribute_description="Work phone",initiate_hub_segment_name="memPhone",initiate_hub_attribute_code="WORKPHONE",initiate_hub_field_name="phNumber",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=0,dbmotion_attribute_weight=None),
InitiateMappings(pk=23,dbmotion_attribute_name="MPHONE",dbmotion_attribute_description="Mobile Phone",initiate_hub_segment_name="memPhone",initiate_hub_attribute_code="MBLPHONE",initiate_hub_field_name="phNumber",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=0,dbmotion_attribute_weight=None),
InitiateMappings(pk=24,dbmotion_attribute_name="SSN",dbmotion_attribute_description="SSN",initiate_hub_segment_name="memIdent",initiate_hub_attribute_code="SSN",initiate_hub_field_name="idNumber",initiate_hub_id_issuer="SSA",mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=100),
InitiateMappings(pk=25,dbmotion_attribute_name="NONMASKSSN",dbmotion_attribute_description="SSN",initiate_hub_segment_name="memIdent",initiate_hub_attribute_code="SSN",initiate_hub_field_name="idNumber",initiate_hub_id_issuer="SSA",mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=100),
InitiateMappings(pk=26,dbmotion_attribute_name="PCONF",dbmotion_attribute_description="Patient Confidentiality",initiate_hub_segment_name="memAttr",initiate_hub_attribute_code="PATCONF",initiate_hub_field_name="attrVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=0),
InitiateMappings(pk=27,dbmotion_attribute_name="DEATHIND",dbmotion_attribute_description="Death Indicator",initiate_hub_segment_name="memAttr",initiate_hub_attribute_code="DEATHIND",initiate_hub_field_name="attrVal",initiate_hub_id_issuer=None,mapping_values="Y=Y;N=N;",dbmotion_attribute_input=0,dbmotion_attribute_weight=None),
InitiateMappings(pk=28,dbmotion_attribute_name="DECEASED_MDATE",dbmotion_attribute_description="Deceased Date",initiate_hub_segment_name="memDate",initiate_hub_attribute_code="DEATHDT",initiate_hub_field_name="dateVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=0,dbmotion_attribute_weight=None),
InitiateMappings(pk=29,dbmotion_attribute_name="JHINMD",dbmotion_attribute_description="Join HIN Mode",initiate_hub_segment_name="memAttr",initiate_hub_attribute_code="JHINMODE",initiate_hub_field_name="attrVal",initiate_hub_id_issuer=None,mapping_values="Yes=Y;No=N;",dbmotion_attribute_input=1,dbmotion_attribute_weight=0),
InitiateMappings(pk=30,dbmotion_attribute_name="PAR_CDATE",dbmotion_attribute_description="PAR Creation Date",initiate_hub_segment_name="memDate",initiate_hub_attribute_code="PAR_CDATE",initiate_hub_field_name="dateVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=0),
InitiateMappings(pk=31,dbmotion_attribute_name="PAR_MDATE",dbmotion_attribute_description="PAR Modification Date",initiate_hub_segment_name="memDate",initiate_hub_attribute_code="PAR_MDATE",initiate_hub_field_name="dateVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=0),
InitiateMappings(pk=32,dbmotion_attribute_name="VIP",dbmotion_attribute_description="Patient VIP",initiate_hub_segment_name="memAttr",initiate_hub_attribute_code="PATVIP",initiate_hub_field_name="attrVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=0,dbmotion_attribute_weight=None),
InitiateMappings(pk=33,dbmotion_attribute_name="PCPID",dbmotion_attribute_description="Primary Care Provider Id",initiate_hub_segment_name="memIdent",initiate_hub_attribute_code="PCPID",initiate_hub_field_name="idNumber",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=0),
InitiateMappings(pk=34,dbmotion_attribute_name="EMCONTACT",dbmotion_attribute_description="Emergency Contact",initiate_hub_segment_name="memAttr",initiate_hub_attribute_code="EMCONTACT",initiate_hub_field_name="attrVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=0,dbmotion_attribute_weight=None),
InitiateMappings(pk=35,dbmotion_attribute_name="LSTMDFDATE",dbmotion_attribute_description="Last modification date",initiate_hub_segment_name="memDate",initiate_hub_attribute_code="LASTMODDT",initiate_hub_field_name="dateVal",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=0,dbmotion_attribute_weight=None),
InitiateMappings(pk=36,dbmotion_attribute_name="CORPID",dbmotion_attribute_description="Corporate Id",initiate_hub_segment_name="memIdent",initiate_hub_attribute_code="CORPORATEID",initiate_hub_field_name="idNumber",initiate_hub_id_issuer="CORP_ID",mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=100),
InitiateMappings(pk=37,dbmotion_attribute_name="SECONDARYID",dbmotion_attribute_description="SECONDARYID",initiate_hub_segment_name="memIdent",initiate_hub_attribute_code="SECONDARYID",initiate_hub_field_name="idNumber",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=100),
InitiateMappings(pk=38,dbmotion_attribute_name="SECONDARYID_ISSUER",dbmotion_attribute_description="SECONDARYID_ISSUER",initiate_hub_segment_name="memIdent",initiate_hub_attribute_code="SECONDARYID",initiate_hub_field_name="idIssuer",initiate_hub_id_issuer=None,mapping_values=None,dbmotion_attribute_input=1,dbmotion_attribute_weight=100),
])

    add_to_model_descriptor2('via_initiatemappings', ['ClinicalViewer','CVA','Via'])

    # Could not update foreign key to different application by model
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE dbmconfigapp_demographysearchfields SET dbm_patient_attribute_id=24;" +     #SSN
            "UPDATE dbmconfigapp_searchresultgrid SET dbMotion_patient_attribute_name_id=20 WHERE id=5;" +  #Gender
            "UPDATE dbmconfigapp_searchresultgrid SET dbMotion_patient_attribute_name_id=24 WHERE id=6;")   #SSN

def load_InitiatePage_data(apps, schema_editor):
    
    page = modelsfactory.createPage(apps.get_model('via', 'InitiatePage')(),
                                            "",
                                            "",
                                            "via_initiate",
                                            [], [])

    model = apps.get_model('via', 'Initiate')()
    model.save()

    add_to_model_descriptor2('via_initiate', ['VPO','Via'])

    model = apps.get_model('via', 'InitiateConnection')()
    model.save()

    add_to_model_descriptor2('via_initiateconnection', ['Via'])

    model = apps.get_model('via', 'InitiateVpo')()
    model.save()

    add_to_model_descriptor2('via_initiatevpo', ['VPO'])

def load_ViaPage_data(apps, schema_editor):
    
    page = modelsfactory.createPage(apps.get_model('via', 'ViaPage')(),
                                            "",
                                            "",
                                            "via_general",
                                            [], [])

    model = apps.get_model('via', 'Via')()
    model.hmo_id = None
    model.save()

    add_to_model_descriptor2('via_via', ['VPO','Via'])

    model = apps.get_model('via', 'ViaVpo')()
    model.save()

    add_to_model_descriptor2('via_viavpo', ['VPO'])

class Migration(migrations.Migration):

    dependencies = [
        ('via', '2120001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
