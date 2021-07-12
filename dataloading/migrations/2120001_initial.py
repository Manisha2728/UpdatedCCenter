# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbmconfigapp', '2120002_initial2'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchLoadingPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('components', models.ManyToManyField(to='dbmconfigapp.Component', null=True)),
                ('services', models.ManyToManyField(to='dbmconfigapp.Service', null=True)),
            ],
            options={
                'verbose_name': 'Batch Loading Scheduler',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BatchLoadingScheduler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable', models.BooleanField(default=False, help_text=b'Enable/Disable the Scheduler.<br/><i>Default: Enable</i>', verbose_name=b'Enable')),
                ('start_boundary_time', models.TimeField(help_text=b'Defines the time that the Scheduler begins to perform batch loading every day.<br><i>Default: 00:00:00</i></br>', verbose_name=b'Start Time')),
                ('duration_unit', models.CharField(default=b'H', help_text=b'Defines the unit of measure for Duration Value<br/><i>Default: Hour</i>', max_length=20, verbose_name=b'Unit', choices=[(b'M', b'Minutes'), (b'H', b'Hour')])),
                ('duration_value', models.PositiveIntegerField(help_text=b'Defines the time during that the scheduler performs batch loading every day.<br><i>Default: 24</i></br>', verbose_name=b'Duration Value')),
                ('interval_value', models.CharField(default=b'10', help_text=b'Defines the amount of time that elapses between each time the Scheduler checks the configured In Folder/s for CSV files.<br/><i>Default: 10 Minutes</i>', max_length=20, verbose_name=b'Interval', choices=[(b'1', b'1 Minute'), (b'2', b'2 Minutes'), (b'3', b'3 Minutes'), (b'5', b'5 Minutes'), (b'10', b'10 Minutes'), (b'20', b'20 Minutes'), (b'30', b'30 Minutes'), (b'45', b'45 Minutes'), (b'60', b'60 Minutes'), (b'120', b'120 Minutes')])),
                ('arc_folder', models.CharField(help_text=b'Defines the Archive folder path', max_length=260, verbose_name=b'Archive Folder')),
                ('page', models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dataloading.BatchLoadingPage', null=True)),
            ],
            options={
                'verbose_name': 'Batch Loading Scheduler',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BatchLoadingSchedulerInPath',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('in_folder', models.CharField(help_text=b'Defines the In Folder path', max_length=260, null=True, verbose_name=b'In folder path', blank=True)),
                ('page', models.ForeignKey(on_delete=models.CASCADE, default=1, to='dataloading.BatchLoadingPage')),
            ],
            options={
                'verbose_name': 'Batch Loading In Folder path',
                'history_meta_label': 'Folder(s) from which the CSV files are loaded',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partitioning',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('history_depth', models.PositiveIntegerField(default=11000, help_text=b'This configuration DELETES old records from ArchMessage tables and moves them to DILMessagesArchive_Expired db as part of the database size reduction process. These messages will no longer be available in the DAT and the Replay tool.<br/><i>Default: 11000 days (about 30 years). It is recommended NOT to change the default value unless database size reduction is requested.</i>', null=True, verbose_name=b'DELETE all records from ArchMessage tables that are older than (days)', blank=True)),
            ],
            options={
                'verbose_name': 'Partitioning Details',
                'history_meta_label': 'Partitioning Details',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PartitioningPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_name', models.CharField(max_length=60, verbose_name=b'page name')),
                ('page_help_text', models.TextField(default=b'This is a help text of the page', blank=True)),
                ('tree_id', models.CharField(default=b'no_id', max_length=60)),
                ('components', models.ManyToManyField(to='dbmconfigapp.Component', null=True)),
                ('services', models.ManyToManyField(to='dbmconfigapp.Service', null=True)),
            ],
            options={
                'verbose_name': 'Partitioning',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='partitioning',
            name='page',
            field=models.ForeignKey(on_delete=models.SET_NULL, default=1, editable=False, to='dataloading.PartitioningPage', null=True),
            preserve_default=True,
        ),
    ]
