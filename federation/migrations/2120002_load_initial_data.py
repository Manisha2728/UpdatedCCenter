# -*- coding: utf-8 -*-
# Auto generated using CCenter command smart_migrate
from __future__ import unicode_literals

from django.db import migrations
from configcenter.settings import get_param
from dbmconfigapp.models import add_to_model_descriptor2

VERSION = '21.2'

def forward(apps, schema_editor):

    load_data(apps, schema_editor)

    pass

def backward(apps, schema_editor):
    pass

def load_data(apps, schema_editor):

    group = apps.get_model('federation', 'Group')
    group_none = group()
    group_none.pk = -1
    group_none.name = '<None>'
    group_none.save()
    group_all = group()
    group_all.pk = 0
    group_all.name = '<All>'
    group_all.save()

    node = apps.get_model('federation', 'Node')()
    node.pk=1
    node.uid = 1
    node.name = 'NODE1'
    node.application_server = get_param('application_server')
    node.request_from_id = 0
    node.response_to_id = 0
    node.save()

    add_to_model_descriptor2('federation_group', services_codes=['Federation'])
    add_to_model_descriptor2('federation_group_node', services_codes=['Federation'])
    add_to_model_descriptor2('federation_nodes_view', services_codes=['Security','Federation'])

class Migration(migrations.Migration):

    dependencies = [
        ('federation', '2120001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
