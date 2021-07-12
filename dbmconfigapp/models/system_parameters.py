from django.db import models
from dbmconfigapp.models.base import ConfigurationEntityBaseModel, get_help_text

# Create your models here.
class SystemParameters(ConfigurationEntityBaseModel):
    param_name          = models.CharField(verbose_name='Parameter Name',max_length=100, unique=True)
    param_value         = models.CharField(verbose_name='Parameter Value',max_length=100)
    
    def __unicode__(self):
        return self.name
           
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'System Parameters'