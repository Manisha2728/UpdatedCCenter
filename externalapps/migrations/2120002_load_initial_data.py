# -*- coding: utf-8 -*-
# Auto generated using CCenter command smart_migrate
from __future__ import unicode_literals

from django.db import migrations
from dbmconfigapp.models import add_to_model_descriptor2
from dbmconfigapp.utils import modelsfactory

VERSION = '21.2'

def forward(apps, schema_editor):

    load_data(apps, schema_editor)

    pass

def backward(apps, schema_editor):
    pass

def load_data(apps, schema_editor):

    page = modelsfactory.createPage(apps.get_model('externalapps', 'DirectAddressEndpointsPage')(),
                                            "",
                                            "",
                                            "mu_reporting_endpoint",
                                            [], [])

    model = apps.get_model('externalapps', 'InstallationProfile')()
    model.pk = 0
    model.name = 'Default Profile'

    model.save()

    add_to_model_descriptor2('externalapps_installationprofile', ['CVA'])

    add_to_model_descriptor2('externalapps_appid', ['CVA','VPO'])
    add_to_model_descriptor2('externalapps_ehr', ['CVA'])
    add_to_model_descriptor2('externalapps_instance', ['CVA'])
    add_to_model_descriptor2('externalapps_instanceproperties', ['CVA'])
    add_to_model_descriptor2('externalapps_orderingfacilities', ['CVA'])
    add_to_model_descriptor2('externalapps_participant', ['CVA'])
    add_to_model_descriptor2('externalapps_patientcontext', ['CVA'])
    add_to_model_descriptor2('externalapps_sourcesystem', ['CVA'])
    add_to_model_descriptor2('externalapps_usercontext', ['CVA'])

class Migration(migrations.Migration):

    dependencies = [
        ('externalapps', '2120001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
