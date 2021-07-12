import sys
from django.db import models
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel
from django.core import validators
from dbmconfigapp.utils.custom_validators import *
from .base import *
from dbmconfigapp.models.fields import IntegerFieldEx
from dbmconfigapp.models.fields import TimeSpanField

NUMBER_OF_BLINKKS_CHOICES = (        
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )


FINAL_BLINK_STATE_CHOICES = (
    ('False', 'Final state is not blinked'),
    ('True', 'Final state is blinked')
    )

       
class EHRAgentClinicalDomainsProperties(ConfigurationEntityBaseModel):
    pv_parent                   = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    name                        = models.CharField(default='AllDomains', max_length=60)
    display_name                = models.CharField(default='All Clinical Domains', verbose_name='Clinical Domain', max_length=60, unique=True)
    attention_searching_time      = models.IntegerField(default=7, verbose_name='Attention Time Range', null=True)
    attention_searching_option    = models.IntegerField(choices=SEARCH_OPTIONS_UNITS, default=3, verbose_name='Attention Time Unit')
    default_attention_time        = models.CharField(default='7 Days', verbose_name='Default Attention Time', max_length=60)
    
    def __unicode__(self):
        return self.display_name
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Attention Rule Time Filter'
        verbose_name= "Attention Rule Time Filter"
        verbose_name_plural = "Attention Rule Time Filters (For Badging)"
        
    def clean(self):
        if self.attention_searching_option != 6 and self.attention_searching_time <= 0:
            raise ValidationError('Attention Time Range must be greater than 0')


class EHRAgentCVCommonClinicalDomainsProperties(ConfigurationEntityBaseModel):
    cv_parent                   = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True)
    name                        = models.CharField(max_length=60)
    display_name                = models.CharField(verbose_name='Clinical Domain', max_length=60, unique=True)
    default_searching_time      = models.IntegerField(default=0, verbose_name='Time Range', null=True, validators=[validators.MinValueValidator(0), validators.MaxValueValidator(sys.maxsize)])
    default_searching_option    = models.IntegerField(choices=SEARCH_OPTIONS_CHOICES_ENLARGED, default=4, verbose_name='Time Unit')
    default_time_range          = models.CharField(verbose_name='Default Time Range', max_length=60)

    def __unicode__(self):
        return self.display_name
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Time Range Filter"
        verbose_name_plural = "Time Range Filters"
        history_meta_label = 'Time Range Filter'
        
        
class EHRAgentLabratory(ConfigurationEntityBaseModel):
    max_lab_events              = IntegerFieldEx(verbose_name='Limit Number Of Lab Events', default=200, null=True, blank=True, validators=[validators.MinValueValidator(20), validators.MaxValueValidator(sys.maxsize)], help_text= get_help_text('Defines the maximum number of latest Lab Events to display in the EHR Agent.<br>The minimum value is 20 Lab Events. To display all labs, leave the field empty.','200') )
    max_clinical_document              = IntegerFieldEx(verbose_name='Limit Number Of Clinical Documents', default=200, null=True, blank=True, validators=[validators.MinValueValidator(20), validators.MaxValueValidator(sys.maxsize)], help_text= get_help_text('Defines the maximum number of latest Clinical Documents to display in the EHR Agent.<br>The minimum value is 20 Documents. To display all documents, leave the field empty.','200') )
     
    def __unicode__(self):
        return ""
      
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Limit Number Of Clinical Acts' 
    
class EHRAgentBlinks(ConfigurationEntityBaseModel):
    pv_parent                       = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    admission_interval = TimeSpanField(verbose_name='First Day Of Admission Interval', choices=TIME_UNIT_CHOICES_DH, default='{0}|{1}'.format(1, TIME_UNIT_CHOICES_DH[0][0]), help_text=get_help_text('Defines the time span from the start of an inpatient admission for which the Badging functionality is enabled.', '1 Day' ))
    admission_inpatient_domains = models.TextField(verbose_name='First Day Of Admission Encounter Type Domains', max_length=400, default='e757b766e61d08f435d3e9e6280f355c', null=False, help_text=get_help_text('Defines the Encounter Type domains (in a comma-separated list) used to define the inpatient encounter for which the Badging functionality is enabled.', 'e757b766e61d08f435d3e9e6280f355c (Inpatient encounter)' ))
     
    def __unicode__(self):
        return "" 
      
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'First Day Of Admission Behavior (For Badging)' 

class EHRAgentPastMedicalHistory(ConfigurationEntityBaseModel):
    cv_problem_parent             = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True, default=2, editable=False)
    pv_parent                   = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    problem_is_past_medical_history_by_end_date       = models.BooleanField(verbose_name='Determined by Effective Time End Date', default=False, help_text=get_help_text('True: Problems will be considered as Medical History (MH) if one of the following exist:<br>- Problem has ended (Effective Time End Date < Today).<br>- Problem Observation Type is the MH baseline code (or is mapped to MH baseline code).<br>False: Problems will be considered as Medical History if Problem Observation Type is MH baseline code (or is mapped to MH baseline code).<br>Medical History baseline code: 2.16.840.1.113883.6.96|417662000', 'False' ))     
    
    def __unicode__(self):
        return ""
      
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Medical History' 

class EHRAgentMedication(ConfigurationEntityBaseModel):
    medication_is_show_calculated_sig = models.BooleanField(verbose_name='Medication SIG Display', 
	default=True, 
	help_text=get_help_text('Defines the format of the Medication prescription instructions (SIG) that is displayed in the Clinical View Agent when the calc_sig field is not available. <br>Note: This configuration is applied only in the case that the calc_sig field is NOT populated. <br>- If the calc_sig field is populated, the SIG is displayed as a single line of text. <br>- If the calc_sig field is Null, the display of the SIG depends on this configuration. <br>The SIG includes the Dose, Route, and Frequency of the medication.<br>True (default): The SIG is displayed as calculated from the Dose, Route and the Frequency fields.<br>False: The SIG is displayed in a table format (Structured SIG).', 'True'))
    
    def __unicode__(self):
        return ""
      
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Medication' 

class VitalsInpatientMeasurement(ConfigurationEntityBaseModel):
    cv_vital_parent             = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, default=13, null=True, editable=False)
    pv_parent                   = models.ForeignKey('PVMeasurementPage', on_delete=models.SET_NULL, default=1, null=True, editable=False)
    include_inpatient_measurements       = models.BooleanField(verbose_name='Include Inpatient Measurements', default=False, help_text=get_help_text('Determines whether Inpatient Measurements are displayed in the Vital Signs domain in CV and EHR Agent.<br>True: Inpatient Measurements will be displayed in Vital Signs.<br>False: Inpatient Measurements will be filtered out and not displayed in Vital Signs.<br>Inpatient Encounter baseline codes: 2.16.840.1.113883.5.4|IMP^2.16.840.1.113883.5.4|ACUTE^2.16.840.1.113883.5.4|NONAC<br><br>Note that all Inpatient Measurements will be displayed. In extreme cases, this can increase system load and reduce performance and product usability. Therefore, we recommend loading only the relevant measurements to the CDR.', 'False' ))     
    include_emergency_measurements       = models.BooleanField(verbose_name='Include Emergency Measurements', default=False, help_text=get_help_text('Determines whether Emergency Measurements are displayed in the Vital Signs domain in CV and EHR Agent.<br>True: Emergency Measurements will be displayed in Vital Signs.<br>False: Emergency Measurements will be filtered out and not displayed in Vital Signs.<br>Emergency Encounter baseline codes: 2.16.840.1.113883.5.4|EMER<br><br>Note that all Emergency Measurements will be displayed. In extreme cases, this can increase system load and reduce performance and product usability. Therefore, we recommend loading only the relevant measurements to the CDR.', 'False' ))
    
    def __unicode__(self):
        return ""
      
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Inpatient Measurements' 
        
class EHRAgentSemanticDelta(ConfigurationEntityBaseModel):
    pv_parent                   = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    name                        = models.CharField(max_length=60)
    display_name                = models.CharField(verbose_name='Clinical Domain', max_length=60)
    enable_semantic_delta       = models.BooleanField(verbose_name='Enable Semantic Delta', default=True, help_text='Determines whether EHR Agent or Patient View filters out data from the selected domains according to semantic similarity.\nFor more details about the semantic delta behavior please refer to the functional specs.')
    
    def __unicode__(self):
        return self.display_name
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Enable Semantic Delta'
        verbose_name= "Enable Semantic Delta"
        verbose_name_plural = "Semantic Delta Configuration"
        
