# -*- coding: utf-8 -*-
# Auto generated using CCenter command smart_migrate
from __future__ import unicode_literals

from django.db import migrations, connection
from dbmconfigapp.models import add_to_model_descriptor2
from configcenter.settings import get_param
from dbmconfigapp.utils import modelsfactory

VERSION = '21.2'

def forward(apps, schema_editor):

    load_SecurityGeneralPage_data(apps, schema_editor)
    load_ADProviders_data(apps, schema_editor)
    load_InternalRoles_data(apps, schema_editor)

    pass

def backward(apps, schema_editor):
    pass

def load_SecurityGeneralPage_data(apps, schema_editor):

    page = modelsfactory.createPage(apps.get_model('security', 'SecurityGeneralPage')(),
                                            "",
                                            "",
                                            "security_general",
                                            [], [])

    model = apps.get_model('security', 'SecurityGeneral')()
    model.save()

    add_to_model_descriptor2('security_securitygeneral', ['CVA','VPO','ADR','PatientList'])

    model = apps.get_model('security', 'PatientAuthorization')()
    model.save()

    add_to_model_descriptor2('security_patientauthorization', ['Security','PPOL','CVA','VPO','PatientService'])

    model = apps.get_model('security', 'PatientProviderRelationship')()
    model.save()

    add_to_model_descriptor2('security_patientproviderrelationship', ['Security','CVA','VPO'])

def load_ADProviders_data(apps, schema_editor):

    model = apps.get_model('security', 'ADProviders')()
    model.pk=1
    model.domain_id = 1
    model.domain_name = get_param('user_absolute_domain')
    model.save()

    add_to_model_descriptor2('security_adproviders', ['Security','CVA'])
    add_to_model_descriptor2('security_applicationdomains', ['Security'])
    add_to_model_descriptor2('security_applications', ['Security'])

    thumbprint = get_param('default_domain_thumbprint')

    model = apps.get_model('security', 'SAMLIssuers')
    saml_issuer = model()
    saml_issuer.saml_issuer_name = 'dbMotion.com'
    saml_issuer.saml_certificate_thumbprint = thumbprint
    saml_issuer.save()
    saml_issuer = model()
    saml_issuer.saml_issuer_name = 'dbMotion SmartAgent'
    saml_issuer.saml_certificate_thumbprint = thumbprint
    saml_issuer.save()

    add_to_model_descriptor2('security_samlissuers', ['Security'])
    add_to_model_descriptor2('security_samlissuersunmanaged', ['Security'])

def load_InternalRoles_data(apps, schema_editor):

    InternalRoles = apps.get_model("security", "InternalRoles")
    db_alias = schema_editor.connection.alias

    InternalRoles.objects.using(db_alias).bulk_create([
        InternalRoles(role_name = 'EHR Common'),
        InternalRoles(role_name = 'EHR Extensive'),
        InternalRoles(role_name = 'EHR Restricted'),
        InternalRoles(role_name = 'EHR Researcher'),
        InternalRoles(role_name = 'General Practitioner'),
        InternalRoles(role_name = 'Nurse'),
        InternalRoles(role_name = 'Ward Manager'),
        InternalRoles(role_name = 'CB Office manager'),
        InternalRoles(role_name = 'CB Physician'),
        InternalRoles(role_name = 'CB Orders administrator'),
    ])

    add_to_model_descriptor2('security_internalroles', ['Security'])
    add_to_model_descriptor2('security_rolemapping', ['Security'])

class Migration(migrations.Migration):

    dependencies = [
        ('security', '2120001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
