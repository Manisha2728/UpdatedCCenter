# -*- coding: utf-8 -*-
# Auto generated using CCenter command smart_migrate
from __future__ import unicode_literals

from django.db import migrations

VERSION = '21.2'

def forward(apps, schema_editor):
    load_auth_user()
    load_authccenter_ccentergroup(apps, schema_editor)

    pass

def backward(apps, schema_editor):
    pass

def load_auth_user():

    from django.contrib.auth.models import User
    from authccenter.utils import FAKE_DJANGO_USER_NAME

    user, created = User.objects.get_or_create(username = 'admin')
    user.username = 'admin'
    user.is_active = True
    user.password = 'pbkdf2_sha256$10000$cHYPTzH7yCCR$oCIMCgN+aH/4VV97I6oYAjmkQs/sVPXUWsIfzHypxJc='
    user.is_superuser = True
    user.is_staff = True
    user.save()

    user, created = User.objects.get_or_create(username = FAKE_DJANGO_USER_NAME)
    user.username = FAKE_DJANGO_USER_NAME
    user.is_active = False
    user.set_unusable_password()
    user.save()

def load_authccenter_ccentergroup(apps, schema_editor):
    Groups = apps.get_model("authccenter", "CCenterGroup")

    db_alias = schema_editor.connection.alias

    Groups.objects.using(db_alias).bulk_create([
        Groups(name='ccenter_admins_group'),
        Groups(name='ccenter_guests_group'),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('authccenter', '2120001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
