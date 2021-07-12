from django.db import models
import inspect
from configcenter import settings

models.options.DEFAULT_NAMES += ('history_meta_label', 'help_text', 'add_link', 'model_descriptor')

HELP_TEXT_FORMAT = '%s<br/><i>Default: %s</i>'

def get_help_text(text, default=None, is_tooltip=None, add_no_export_note=False):
    new_line = '\n' if is_tooltip else '<br/>'
    if default:
        text = HELP_TEXT_FORMAT % (text, default)
    if is_tooltip:
        text = text.replace('<br/>', new_line).replace('\t', '')
    if add_no_export_note:
        text += new_line + '<b>Note:</b> this field will not be transferred in the export/import process.'
    return text



SEARCH_OPTIONS_CHOICES_ENLARGED = (
    (0, 'Year'),
    (1, 'Month'),
    (3, 'Day'),
    (4, 'All'),
    )

SEARCH_OPTIONS_CHOICES = (
    (0, 'Year'),
    (1, 'Month'),
    (4, 'All'),
    )

SEARCH_OPTIONS_UNITS = (
    (0, 'Year'),
    (1, 'Month'),
    (3, 'Day'),
    (6, 'Off'))

TIME_UNIT_CHOICES_YMD = (
    (0, 'Years'),
    (1, 'Months'),
    (3, 'Days'),
    )

TIME_UNIT_CHOICES_DH = (
    (3, 'Days'),
    (5, 'Hours'),
    )



class ConfigurationEntityBaseModel(models.Model):
    name = ''
    objects = models.Manager()
    
    _contains_file_fields = None
    file_fields = []
    
    # override __unicode__ to set the field(s) that represent a specific record of this model 
    def __unicode__(self):
        return self.name
    
    @classmethod
    def contains_file_fields(cls):
        if cls._contains_file_fields is None:
            cls.file_fields = [img for img in cls._meta.fields if type(img) == models.ImageField]
            cls._contains_file_fields = bool(cls.file_fields)
        return cls._contains_file_fields

    class Meta:
        abstract = True
        app_label = "dbmconfigapp"
        
       

class PageBaseModel(models.Model):
    services                = models.ManyToManyField('dbmconfigapp.Service', null=True)
    components              = models.ManyToManyField('dbmconfigapp.Component', null=True)
    page_name               = models.CharField(max_length=60, verbose_name='page name')
    page_help_text          = models.TextField(blank=True, default='This is a help text of the page')
    tree_id                 = models.CharField(max_length=60, default='no_id')
    
         
    def __unicode__(self):
        return self.page_name
    
    def get_name_for_title(self):
        title = self._meta.verbose_name #.title()
        #if title.endswith(' Page'): title = title[:-5]
        return title
    
    def page_title(self):
        return 'Set the %s Settings' % self.get_name_for_title()
    
    def get_affected_components(self):
        return ', '.join(component.verbose_name for component in self.components.all())        
    
    def get_restarted_services(self):
        return ', '.join(service.verbose_name for service in self.services.all())
    
    def get_tree_id(self):
        return self.tree_id
    
    class Meta:
        app_label = "dbmconfigapp"
        abstract = True
        verbose_name = "[no page name set]"

    
class Service(models.Model):
    name            = models.CharField(max_length=60)
    verbose_name    = models.CharField(max_length=60)
    code_name       = models.CharField(max_length=60)
    need_restart    = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.verbose_name
    
    class Meta:
        app_label = "dbmconfigapp"

class ModelDescriptor(models.Model):
    services       = models.ManyToManyField('Service', null=True)
    model_name    = models.CharField(max_length=200)    
    export_in_api      = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.model_name
    
    def get_services_to_restart(self):
        return list(service.verbose_name for service in self.services.filter(need_restart=True))
    
    class Meta:
        app_label = "dbmconfigapp"
        
class Component(models.Model):
    name            = models.CharField(max_length=60)
    verbose_name    = models.CharField(max_length=60)    
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "dbmconfigapp"