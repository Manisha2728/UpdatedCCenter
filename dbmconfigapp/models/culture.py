'''
Created on Dec 1, 2015

@author: RBRILMANN
'''
from django.db import models
from dbmconfigapp.models.base import ConfigurationEntityBaseModel

class Culture(ConfigurationEntityBaseModel):
    agenthub_general_page = models.ForeignKey('AgentHubGeneralPage', on_delete=models.CASCADE, null=False, default=1, editable=False)
    name         = models.CharField(max_length=30, unique=False, verbose_name=b'Additional Languages', help_text=b'Define a new language for the user interface.')
    readonly     = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if(len(Culture.objects.filter(name=self.name)) > 0):
            CurrentCulture.objects.update(name=Culture.objects.filter(name=self.name)[0])
            return
        super(Culture, self).save(*args, **kwargs)
        CurrentCulture.objects.update(name=self)
    
    def delete(self, *args, **kwargs):
        super(Culture, self).delete(*args, **kwargs)
        if (CurrentCulture.objects.count() == 0):
            CurrentCulture.objects.get_or_create(name=Culture.objects.filter(name='en-US')[0])
     
    def __unicode__(self):
        return self.name    
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Language list"
        verbose_name = "Language"

def getLang():
    return  [(x.id, x.name) for x in Culture.objects.all()]
            
class CurrentCulture(ConfigurationEntityBaseModel):
    agenthub_general_page = models.ForeignKey('AgentHubGeneralPage', on_delete=models.CASCADE, null=False, default=1, editable=False)
    name         = models.ForeignKey(Culture, on_delete=models.CASCADE, choices=(),verbose_name=b'Select culture',help_text="This is the grey text")
    
    def __unicode__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        super(CurrentCulture, self).save(*args, **kwargs)
        
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Language list"
        verbose_name = "Language"