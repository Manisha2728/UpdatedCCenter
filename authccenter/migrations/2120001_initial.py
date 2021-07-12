# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ADGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'ad group',
                'verbose_name_plural': 'ad groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CCenterGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='name')),
                ('permissions', models.ManyToManyField(to='auth.Permission', verbose_name='permissions', blank=True)),
            ],
            options={
                'verbose_name': 'ccenter group',
                'verbose_name_plural': 'ccenter groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CCenterUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100, null=True, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, verbose_name='last name', blank=True)),
                ('username', models.CharField(max_length=100, verbose_name='username')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('session_key', models.CharField(max_length=100, null=True, verbose_name='session key', blank=True)),
                ('groups', models.ManyToManyField(related_query_name=b'ccenter_user', related_name='ccenter_user_set', to='authccenter.ADGroup', blank=True, help_text='The groups this user belongs to.', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'ccenter user',
                'verbose_name_plural': 'ccenter users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SettingsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active_directory_mode', models.BooleanField(default=False, verbose_name='AD mode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='adgroup',
            name='ccneter_group',
            field=models.ForeignKey(on_delete=models.SET_NULL, to='authccenter.CCenterGroup'),
            preserve_default=True,
        ),
    ]
