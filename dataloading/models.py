from django.db import models
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel, get_help_text
import datetime 
import xml.etree.ElementTree as ET
import os
import subprocess
from configcenter.settings import get_param
from configcenter import settings
from django.utils.functional import empty


_UNIT_CHOICES =(
    ('M', 'Minutes'),
    ('H', 'Hour'),)


_INTERVAL_CHOICES =(
    ('1', '1 Minute'),('2', '2 Minutes'),('3', '3 Minutes'),('5', '5 Minutes'),('10', '10 Minutes'),('20', '20 Minutes'),
    ('30', '30 Minutes'),('45', '45 Minutes'),('60', '60 Minutes'),('120', '120 Minutes'),)




# DataLoading Page model For Partitioning
class PartitioningPage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "dataloading"
        verbose_name = 'Partitioning'

        
        
# Models for partitioning
class Partitioning(ConfigurationEntityBaseModel):
    page            = models.ForeignKey('PartitioningPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    history_depth  = models.PositiveIntegerField(verbose_name='DELETE all records from ArchMessage tables that are older than (days)', null=True, blank=True, default=11000, help_text=get_help_text('This configuration DELETES old records from ArchMessage tables and moves them to DILMessagesArchive_Expired db as part of the database size reduction process. These messages will no longer be available in the DAT and the Replay tool.', '11000 days (about 30 years). It is recommended NOT to change the default value unless database size reduction is requested.'))
    
    def __unicode__(self):
        return self.name
           
    class Meta:
        app_label = "dataloading"
        verbose_name = 'Partitioning Details'
        history_meta_label = verbose_name

    
        


# DataLoading Page model for BatchLoading
class BatchLoadingPage(PageBaseModel):
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "dataloading"
        verbose_name = 'Batch Loading Scheduler'

# Models for partitioning
class BatchLoadingScheduler(ConfigurationEntityBaseModel):
    page             = models.ForeignKey('BatchLoadingPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    enable          = models.BooleanField(verbose_name='Enable', default=False, help_text=get_help_text('Enable/Disable the Scheduler.','Enable'))  
    start_boundary_time    = models.TimeField(verbose_name='Start Time' , help_text=get_help_text('Defines the time that the Scheduler begins to perform batch loading every day.<br><i>Default: 00:00:00</i></br>'))
    duration_unit   = models.CharField(verbose_name='Unit', max_length=20, choices=_UNIT_CHOICES, default=_UNIT_CHOICES[1][0], help_text=get_help_text(
                     'Defines the unit of measure for Duration Value', _UNIT_CHOICES[1][1]))
    duration_value  = models.PositiveIntegerField(verbose_name='Duration Value' ,help_text=get_help_text('Defines the time during that the scheduler performs batch loading every day.<br><i>Default: 24</i></br>'))   
    interval_value   = models.CharField(verbose_name='Interval', max_length=20, choices=_INTERVAL_CHOICES, default=_INTERVAL_CHOICES[4][0], help_text=get_help_text(
                     'Defines the amount of time that elapses between each time the Scheduler checks the configured In Folder/s for CSV files.', _INTERVAL_CHOICES[4][1]))
    arc_folder      = models.CharField(verbose_name='Archive Folder', max_length=260, help_text='Defines the Archive folder path')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "dataloading"
        verbose_name = 'Batch Loading Scheduler'


class BatchLoadingSchedulerInPath(ConfigurationEntityBaseModel):
    page            = models.ForeignKey('BatchLoadingPage', on_delete=models.CASCADE, default=1)
    in_folder       = models.CharField(verbose_name='In folder path',null=True,blank=True, max_length=260, help_text='Defines the In Folder path')#,'Can contain more than one address, with \';\' as separator')
    
    def __unicode__(self):
        return self.in_folder
    
    class Meta:
        app_label = "dataloading"
        verbose_name = 'Batch Loading In Folder path'       
        history_meta_label = "Folder(s) from which the CSV files are loaded"
     
     
        

    
    