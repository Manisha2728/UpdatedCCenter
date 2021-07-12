# -*- coding: utf-8 -*-
# Auto generated using CCenter command smart_migrate
from __future__ import unicode_literals
from django.db import models, migrations

from dataloading.utils import add_to_model_descriptor
from dbmconfigapp.utils import modelsfactory
import datetime
from configcenter.settings import DBM_SHARED_FOLDER
from os import path

VERSION = '21.2'


def forward(apps, schema_editor):
    load_services(apps, schema_editor)
    load_partitioningpage(apps, schema_editor)
    load_batchloadingpage(apps, schema_editor)

def load_services(apps, schema_editor):
    Service = apps.get_model("dbmconfigapp", "Service")

    db_alias = schema_editor.connection.alias

    Service.objects.using(db_alias).bulk_create([
        Service(name='dbMotion Data Loading', verbose_name='dbMotion Data Loading', code_name='DataLoading', need_restart = True),
    ])

def load_partitioningpage(apps, schema_editor):
    # Add Partitioning page
    page = modelsfactory.createPage(apps.get_model('dataloading', 'PartitioningPage')(),
                                        "",
                                        "",
                                        "data_loading_app",
                                        [], [ ])      
    
    newdata = apps.get_model('dataloading', 'Partitioning')()
    newdata.save()

def load_batchloadingpage(apps, schema_editor):
    srv_list = ['DataLoading']
    add_to_model_descriptor(model_name='dataloading_batchloadingscheduler', services_codes=srv_list)    
    add_to_model_descriptor(model_name='dataloading_batchloadingschedulerinpath', services_codes=srv_list)
    # Add Batch Loading page
    page = modelsfactory.createPage(apps.get_model('dataloading', 'BatchLoadingPage')(),
                                        "",
                                        "",
                                        "data_loading_batch",
                                        [], [ ])      
    
    newdata = apps.get_model('dataloading', 'BatchLoadingScheduler')()
    newdata.page = page
    newdata.enable = True
    newdata.duration_value = 24
    newdata.start_boundary_time =datetime.time(00, 00, 00)
    newdata.arc_folder = path.join(DBM_SHARED_FOLDER, 'CSV4BL')
    newdata.save()
    
    newdata = apps.get_model('dataloading', 'BatchLoadingSchedulerInPath')()
    newdata.in_folder = path.join(DBM_SHARED_FOLDER, 'inCSV4BL')
    newdata.save()   
    pass

def backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('dataloading', '2120001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
