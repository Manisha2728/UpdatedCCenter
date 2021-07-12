from django.db import models
from dbmconfigapp.models.base import *


class EHRAgentSemanticGroup(ConfigurationEntityBaseModel):
    display_name      = models.CharField(max_length=200, verbose_name='Group Display Name')
    order             = models.IntegerField(verbose_name='Group Order')
    pv_measurement    = models.ForeignKey('PVMeasurementPage', on_delete=models.SET_NULL, null=True, default=1)
    def page_title(self):
        return 'Set the %s Settings' % self._meta.verbose_name
    
    def measurements(self):
        return ', '.join([m.__unicode__() for m in EHRAgentMeasurementProperties.objects.filter(semantic_group=self)])

    def __unicode__(self):
        return self.display_name

    def name_url(self):
        if self.id:
            return '<a href="%s" onclick="return showEditPopup(this);" title="Click to edit">%s</a>' % ("/admin/dbmconfigapp/ehragentsemanticgroup/%s/" % self.id, self.display_name)
        else:
            return '<a href="%s" onclick="return showEditPopup(this);" >Add new Application</a>' % "/admin/dbmconfigapp/ehragentsemanticgroup/add/"
    
    name_url.allow_tags = True
    name_url.short_description = display_name.verbose_name

    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Semantic Group'
        verbose_name= "Measurements Domain Grouping"
        help_text = 'For the following Measurements configurations, see the <a href="/admin/dbmconfigapp/clinicaldomainvitals/13/">Vitals</a> page under Clinical Viewer Clinical Domains: <ul><li>Displaying/hiding the UOM</li><li>Concatenating Measurement Values</li><li>Defining UOM priority order to display concatenated Body Weight</li><li>Defining UOM priority order to display concatenated Body Height</li></ul>'
        
class EHRAgentMeasurementProperties(ConfigurationEntityBaseModel):
#    parent                      = models.ForeignKey('EHRAgentMeasurementsPage', null=True, default=1, editable=False)
    semantic_group              = models.ForeignKey('EHRAgentSemanticGroup', on_delete=models.SET_NULL, null=True, default=1)
    domain_id                   = models.CharField(verbose_name='Vocabulary Domain', max_length=60, unique=True)
    order                       = models.IntegerField(verbose_name='Order')
    hide_uom                    = models.BooleanField(default=False, verbose_name='Hide the UOM', help_text='Defines the vital sign measurement in which the UOM (Unit Of Measurement) is hidden. Default: BloodPressure, HeartRate. This configuration applies to Patient View')
    def __unicode__(self):
        return self.domain_id
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Measurement Definition'
        verbose_name= "Measurement Definition"
        verbose_name_plural = "Measurement Definition"

class PVMeasurementPage(PageBaseModel):
    def page_title(self):
        return "Set Measurement Settings"
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Measurement"       
        history_meta_label = verbose_name 
