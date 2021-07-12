from django.db import models

class MigrationManager(models.Model):
    app_name    = models.CharField(max_length=255)
    version     = models.CharField(max_length=255, null=True, blank=True)
    ga_migration    = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return '{0:13}|{1:5}|{2}'.format(self.app_name, self.version, self.ga_migration)
    
    class Meta:
        app_label = "dbmconfigapp"

class VersionManager(models.Model):
    version         = models.CharField(max_length=255)
    install_date    = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return self.version
    
    class Meta:
        app_label = "dbmconfigapp"