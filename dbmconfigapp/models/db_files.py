from .base import *
from django.db.models import ImageField as CoreImageField


class BlobField(models.Field):
    description = "Blob"

    def db_type(self, connection):
        if connection.vendor == 'sqlite':
            return 'blob'
        return 'ntext'
    

class DbFiles(models.Model):
    filename = models.CharField(max_length=100)
    data     = BlobField()
    size     = models.IntegerField()

    def __unicode__(self):
        return self.filename

    class Meta:
        app_label = "dbmconfigapp"
      
    
