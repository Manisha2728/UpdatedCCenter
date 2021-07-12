# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from dbmconfigapp.models import add_to_model_descriptor2
from django.db import models, migrations

def forward(apps, schema_editor):
    #ADDING CVA MODEL DESCRIPTOR TO EXISTING TABLE
    srv_list = ['ACDM','CVA']
    add_to_model_descriptor2(model_name='dbmconfigapp_myhrorganizationsentity', services_codes=srv_list)  

    pass

def backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('dbmconfigapp', '2120003_load_initial_data'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]

