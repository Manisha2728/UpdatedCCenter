'''
Created on Dec 3, 2013

@authors: EBliacher, TBener
'''
from django.db import models
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel
from django.core.exceptions import ValidationError
from dbmconfigapp.admin.dbm_ModelAdmin import get_grid_help_text

class PlGeneralPage(PageBaseModel):
    
    def __str__(self):
        return self.page_name
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Patient List General"
       
def validate_string_is_a_num(value):
    if not (str(value).isdigit()):
        raise ValidationError('Enter a whole number.')

def validate_diagnosis_format(value):
    digits = value.split(',');
    
    for d in digits :                    
        if not (str(d).isdigit()):
            raise ValidationError('Enter Comma separated numbers')
    
    
class EncounterDiagnosisRelationship(ConfigurationEntityBaseModel):
    pl_parent                          = models.ForeignKey('PlGeneralPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)        
    pv_parent                          = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    primary_diagnosis           = models.CharField(verbose_name='Primary Diagnosis', default='1', max_length=50, validators=[validate_diagnosis_format], help_text='Determines the value(s) used for the main (primary) diagnosis of the patient during an encounter, such as a hospitalization.<br/>Possible values: Any value can be configured. For example:  American market: 1   Israeli market: 1, 6, or 1,6<br/>Default Value: 1 (American market)<br/>')
    admitted_diagnosis          = models.CharField(verbose_name='Admitting Diagnosis', default='0', max_length=50, blank=True, validators=[validate_string_is_a_num], help_text='Determines the value(s) used for the admitting diagnosis given when the patient was first admitted to the hospital.<br/>Possible Values: Any value can be configured. For example:  American market: 0   Israeli market: Null (empty)<br/>Default Value: 0 (American market)<br/>')
    
    def __str__(self):
        return '' 
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Configure the Encounter Diagnosis"
        verbose_name = history_meta_label
        help_text = get_grid_help_text("This configuration determines the code used for the display of the Encounter Diagnosis (or Encounter reason) in the clinical applications (for example, the data displayed in Discharge Diagnosis or the Visit Reason field). The business logic for the displayed data differs depending on the customer location and on the specific field in the application.  For a detailed description of the business logic, see the Functional Specification documentation.")        
