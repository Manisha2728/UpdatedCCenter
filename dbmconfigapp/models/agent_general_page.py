from django.db import models
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel,\
get_help_text



# creation of page model
class AgentHubGeneralPage(PageBaseModel):  
    def __unicode__(self):
        return self.page_name

    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "General Definitions"    
