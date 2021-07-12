from django.db import models

class PatientSystems(models.Model):
    system_oid      = models.CharField(max_length=60, verbose_name='System Id')
    system_name     = models.CharField(max_length=60, verbose_name='System Name')
    def __unicode__(self):
        return self.system_name
    class Meta:
        app_label = "dbmconfigapp"
