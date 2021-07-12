# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from dbmconfigapp.migrations import noop

def forward(apps, schema_editor):
    # app = apps.get_app_config("dbmconfigapp")
    # MyModel = app.get_model("SomeModel")
    # or -
    # MyModel = apps.get_model("dbmconfigapp", "SomeModel")
    # and then -
    # MyModel.objects.filter(...)
    return None

def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('dbmconfigapp', '0005_update_cv_problems_filter_status_code_default'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]
