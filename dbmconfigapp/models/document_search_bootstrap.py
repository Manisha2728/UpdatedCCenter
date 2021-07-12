import sys
from django.db import models
from django.core.exceptions import ValidationError
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel,\
    get_help_text
from django.core import validators

FREQUENCY_MODE = (
    (1, 'Continuous'),
    (2, 'Time Frame')
    )

class DocumentSearchBootstrap(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Document Search Bootstarp"
        
class DocumentSearchBootstrapProperties(ConfigurationEntityBaseModel):
    parent =                models.ForeignKey('DocumentSearchBootstrap', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    frequency_mode   =        models.IntegerField(verbose_name='Bootstrap frequency mode:', choices=FREQUENCY_MODE, default=1, help_text='Each insert, update, and delete of a clinical document in the CDR triggers queuing the document in an operational table for Elasticsearch indexing. Specify how often the indexing occurs.<br/>* <b>Continuous</b><br/>* <b> Time frame:</b><br/><i>Default: Continuous.</i>')
    start_scheduled_time       =        models.TimeField(verbose_name="Bootstrap start time:", blank = True, default = None, null = True, help_text='Enter a time in format HH:MM:SS, click Now, or click the clock icon to select from a list of start times.<br/><i>Default: Empty</i>')
    end_scheduled_time         =        models.TimeField(verbose_name="Bootstrap end time:", blank = True, default = None, null = True, help_text='Enter a time in format HH:MM:SS, click Now, or click the clock icon to select from a list of start times.<br/><i>Default: Empty</i>')
    protected_systems1    = models.TextField(verbose_name='Group #1 protected systems', blank=True, default='', help_text=get_help_text('''
        Specify a list of systems not affected by content requests by the group. Use the pipe symbol [|] as a delimiter between systems.
    ''','Empty'))
    protected_systems_rate1    = models.IntegerField(verbose_name='Group #1 aggregated rate (req/min)', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(sys.maxsize)], blank=True, null=True, help_text=get_help_text('''
        Define the aggregated rate of content requests to systems from group.
    ''','Empty'))
    protected_systems2    = models.TextField(verbose_name='Group #2 protected systems', blank=True, default='', help_text=get_help_text('''
        Specify a list of systems not affected by content requests by the group. Use the pipe symbol [|] as a delimiter between systems.
    ''','Empty'))
    protected_systems_rate2    = models.IntegerField(verbose_name='Group #2 aggregated rate (req/min)', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(sys.maxsize)], blank=True, null=True, help_text=get_help_text('''
        Define the aggregated rate of content requests to systems from group.
    ''','Empty'))
    unprotected_systems_rate    = models.IntegerField(verbose_name='Standard aggregated rate (req/min)', default=8000, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(sys.maxsize)], blank=False, null=False, help_text=get_help_text('''
        Define the maximum standard rate of content requests for unprotected sources. Changing this setting might affect the system.
    ''','8000'))
    def __unicode__(self):
        return ''
		
    def clean(self):        
        if (self.frequency_mode == 2 and (self.start_scheduled_time == None or self.end_scheduled_time == None)):
            raise ValidationError('Start time and End time should be valid not empty dates.')
        if (self.frequency_mode == 2):
            if (self.start_scheduled_time == self.end_scheduled_time):
                raise ValidationError('Start time and End time should be different.')
            if (self.start_scheduled_time.hour == self.end_scheduled_time.hour and self.start_scheduled_time.minute == self.end_scheduled_time.minute):
                raise ValidationError('Start time and End time must be different for HH:MM.')
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Document Search Bootstarp"