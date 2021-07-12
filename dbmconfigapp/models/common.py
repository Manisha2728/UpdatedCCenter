from django.db import models
from dbmconfigapp.models.base import ConfigurationEntityBaseModel



class Message(ConfigurationEntityBaseModel):
    clinical_domain         = models.ForeignKey(to='ClinicalDomain', on_delete=models.SET_NULL, default=14, null=True)
    message                 = models.CharField(max_length=120, verbose_name="text")
    culture                 = models.CharField(max_length=12)
    description             = models.CharField(max_length=120, null=True, blank=True)
    
    def __unicode__(self):
        return "[%s | %s]" % (self.message, self.culture)
       
    class Meta:
        app_label = "dbmconfigapp"
        unique_together = ("culture", "message")
        verbose_name = "Item"
        abstract = True