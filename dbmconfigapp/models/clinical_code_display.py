from dbmconfigapp.models.base import *

class ClinicalCodeDisplayPage(PageBaseModel):
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Clinical Code Display'
       
class PlClinicalCodeDisplayPage(PageBaseModel):
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Patient list Clinical Code Display'
        history_meta_label = verbose_name

class PVClinicalCodeDisplayPage(PageBaseModel):
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Clinical Code Display'
        history_meta_label = verbose_name

class ClinicalCodeDisplay(ConfigurationEntityBaseModel):
    cv_parent               = models.ForeignKey('ClinicalCodeDisplayPage', on_delete=models.SET_NULL, default=1, null=True, editable=False)
    pl_parent               = models.ForeignKey('PlClinicalCodeDisplayPage', on_delete=models.SET_NULL, default=1, null=True, editable=False)
    pv_parent               = models.ForeignKey('PVClinicalCodeDisplayPage', on_delete=models.SET_NULL, default=None, null=True, editable=False)
    business_aspect         = models.CharField(max_length=40)
    business_table          = models.CharField(max_length=40, help_text='The business table within the business aspect.')
    code_name               = models.CharField(max_length=40, help_text='The business codes.')
    vocabulary_domain       = models.CharField(max_length=40, help_text='The relevant Vocabulary domain of the codes.')
    display_as              = models.CharField(max_length=50, default='Preferred|Baseline|Local|Text',  null=True, blank=True, help_text='Change the priority order by dragging and dropping the text in the required field.')
    
    def __unicode__(self):
        # This will stand for the row in history log 
        return "%s-%s-%s" % (self.business_aspect, self.business_table, self.code_name)
           
    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = 'Clinical Code Display'


        