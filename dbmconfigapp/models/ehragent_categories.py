from django.db import models
from dbmconfigapp.models.base import *
from django.core import validators

GROUPING_CHOICES = (
    (0, 'Disabled'),
    (1, 'Collapsed'),
    (2, 'Expanded'),
    )

class EHRAgentCategoriesTopic(models.Model):
    topic_name      = models.CharField(max_length=60)
    def __unicode__(self):
        return self.topic_name
    class Meta:
        app_label = "dbmconfigapp"
        
class EHRAgentTooltips(ConfigurationEntityBaseModel):
    category            = models.ForeignKey('EHRAgentCategoriesProperties', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    tooltip             = models.CharField(max_length=40)
    enabled             = models.BooleanField(default=True)
    
    def __unicode__(self):
        return '"%s" tooltip in "%s" category' % (self.tooltip, self.category.category_name)
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Tooltips Definition"
        
class EHRAgentCategoriesProperties(ConfigurationEntityBaseModel):
    name                        = models.CharField(max_length=60)
    category_name               = models.CharField(verbose_name='Category', max_length=60, unique=True)   
    enable_category             = models.BooleanField(verbose_name='Category Enabled', default=True)
    category_opened             = models.BooleanField(verbose_name='Opened By Default ', default=False, help_text = 'Display a category as opened by default')
    grouping_option             = models.IntegerField(choices=GROUPING_CHOICES, default=1, null=False, verbose_name='Grouping')
    category_order              = models.IntegerField(null=True, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)], help_text = "Determines the order of the category in the application. The category order configuration is relevant for the CVA main page only.")
    topic                       = models.ForeignKey('EHRAgentCategoriesTopic', on_delete=models.SET_NULL, null=True, default=1)
    has_tooltips                = models.BooleanField(default=False)
    show_in_encounter_details   = models.BooleanField(verbose_name='Categories Displayed in Encounter Details Page', default=False, help_text='Select the categories to be displayed in the Encounter Details page. The Encounter-related acts of these categories will be displayed in the Encounter Details page.')
   
    def tooltips(self):
        link = '/admin/dbmconfigapp/ehragentcategoriesproperties/%s/' % self.id
        tt_list = EHRAgentTooltips.objects.filter(category=self, enabled=True)
        text = ', '.join(t.tooltip for t in tt_list) if tt_list else '(No tooltips selected)'
        return '<a href="%s" onclick="return showEditPopup(this);" title="Click to edit">%s</a>' % (link, text )
    
    tooltips.allow_tags = True
    tooltips.short_description = 'Tooltips'

    
    def __unicode__(self):
        return self.category_name
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Categories Definition'
        verbose_name= "Categories Definition"
        verbose_name_plural = "Categories Definition"
        

