from django.core.exceptions import ValidationError

from dbmconfigapp.models.base import *
from dbmconfigapp.models.fields import TimeSpanField
from django.core import validators

TIME_SPAN_CHOICES = (
    (0, 'Years'),
    (1, 'Months'),
    (2, 'Weeks'),
    (3, 'Days'),
    (4, 'Hours'),
    )


DATE_FORMAT_CHOICES = (
    ('PY', 'Years'),
    ('PM', 'Months'),
    ('PW', 'Weeks'),
    ('PD', 'Days'),
    ('PYM' , 'Years and Months'),
    ('TH', 'Hours'),
    ('THM', 'Hours and Minutes'),
     )

INTERPRETATION_CHOICES = (
    ('2', 'Low'),
    ('4', 'Medium'),
    ('8', 'High'),
    ('16', 'Very High'),
    )

def validate_name_format(value):
    if value.find("{0}") < 0 or value.find("{1}") < 0:
        raise ValidationError('Last Name ({0}) and First Name ({1}) parts are mandatory.')


class AppsPatientDisplay(ConfigurationEntityBaseModel):
    cv_parent                   = models.ForeignKey('CvPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pv_parent_patient_display   = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pl_parent             = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    patient_search_name_format  = models.CharField(verbose_name='Patient Name Display in Patient Search', blank=False, null=False, default='{0}, |{1}', validators=[validate_name_format], max_length=60, help_text="This configuration is used to define the display of the patient name returned after performing a Patient Search in Collaborate or the Clinical Viewer.<br/>The order of the Patient Name parts is defined according to the following values. You can make changes by removing a value, adding a value, or changing the order of the values.<br/>Where:<br/>- {0} = Last Name<br/>- {1} = First Name<br/>The | symbol is required to separate the data in the value, but is not displayed in the output.<br/><i>Default: {0}, |{1}</i>")
    collaborate_address_format  = models.CharField(verbose_name='Patient Address Display (Collaborate, Agent Hub)', blank=True, null=True, default='{0} |{1}, |{2}, |{3}, |{4} |{5}', max_length=60, help_text="Defines the patient's address display in Collaborate and Agent Hub according to the following values.<br/>You can make changes to the display by removing a value, adding a value, or changing the order of the values.<br/>Where:<br/>- {0} = AddressLine1<br/>- {1} = AddressLine2<br/>- {2} = City<br/>- {3} = State<br/>- {4} = Country<br/>- {5} = Postal Code<br/>The | symbol is required to separate the data in the value, but is not displayed in the output. The comma is not required in the value. If it is in the value it will be displayed in the output. <br><i>Default: {0} |{1}, |{2}, |{3}, |{4} |{5}</i>")
    cv_address_format           = models.CharField(verbose_name='Patient Address Display (Clinical Viewer)', blank=True, null=True, default='{0}, |{1}, |{2}', max_length=60, help_text="Defines the patient address display in the Patient Search clinical view (in the Search Results table, Search History table, and Consent Manager form) according to the following values.<br/>You can make changes to the display by removing a value, adding a value, or changing the order of the values.<br/>Where:<br/>- {0} = Address<br/>- {1} = City<br/>- {2} = State<br/>The | symbol is required to separate the data in the value, but is not displayed in the output. The comma is not required in the value. If it is in the value it will be displayed in the output. <br><i>Default: {0}, |{1}, |{2}</i>")
    phone_format                = models.CharField(verbose_name='Patient Phone Number Format', blank=True, null=True, default='{0}-|{1}-|{2}|(#{3})', max_length=60, help_text="The appearance of the patient's telephone number in Collaborate is defined according to the values below. You can make changes to the appearance by removing a value, adding a value, changing the order of the values, etc.<br/>Where:<br/>- {0} = Country Code<br/>- {1} = Area Code<br/>- {2} = Phone Number<br/>- {3} = Extension<br/>The | symbol is required to separate the data in the value, but is not displayed in the output in Collaborate. <br/><i>Default: {0}-|{1}-|{2}|(#{3})</i>")
    
    def __unicode__(self):
        return ""
           
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Patient Display'   
 

# Patient Header
class AppsPatientDisplayWithAgent(ConfigurationEntityBaseModel):   
    cv_parent                   = models.ForeignKey('CvPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pv_parent_patient_display   = models.ForeignKey('PVPatientDisplayPage',on_delete=models.SET_NULL,  null=True, default=1, editable=False)
    pl_parent             = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    patient_name_format         = models.CharField(verbose_name='Patient Name Display', blank=False, null=False, default='{0}, |{1} |{2}', validators=[validate_name_format], max_length=60, help_text=get_help_text("This configuration is used to define the patient name display in:<br/>- Clinical Viewer Patient Header<br/>- EHR Agent Patient Header<br/>- Patient List<br/> The order of the Patient Name parts is defined according to the following values. You can make changes by removing a value, adding a value, or changing the order of the values.<br/>Where:<br/>- {0} = Last Name<br/>- {1} = First Name<br/>- {2} = Middle Initial<br/>The | symbol is required to separate the data in the value, but is not displayed in the output.", "{0}, |{1} |{2}"))
    def __unicode__(self):
        return ""
           
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Patient Display (Patient Header)'   

class AppsAdvanceDirectiveNodes(ConfigurationEntityBaseModel):  
    cv_parent           = models.ForeignKey('CvPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pl_parent           = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pv_parent_patient_display           = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    nodes               = models.CharField(max_length=500, verbose_name= "Advance Directive nodes", null=True, blank=True, default='',help_text=get_help_text('Define a comma-separated list of the dbMotion nodes (as a Node ID) to be queried for Advance Directive documents. <br/>An empty value will send the request to all the nodes. <br/>For example, for Node ID=1 and Node ID=12, enter the following value:  1,12', 'empty'))
    is_display_adv_dir  = models.BooleanField(verbose_name='Display Advance Directive', default=True, help_text=get_help_text('Enable the Advance Directive feature.', 'False'))
    adv_dir             = models.CharField(max_length=6, verbose_name= "Advance Directive indicator", default='ADVDIR',help_text=get_help_text('Define the displayed value of the Advance Directive indication.', 'ADVDIR'))

    def __unicode__(self):
        return ""
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Advance Directives'
    
        
class AppsPatientDisplayCommon(ConfigurationEntityBaseModel):
    cv_parent                     = models.ForeignKey('CvPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pl_parent                     = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    is_display_patient_mrn        = models.BooleanField(verbose_name='Display patient MRN in the applications', default=True, help_text='Determines whether the MRN is displayed in the Patient Details header of the Clinical Views and Clinical View Agent.<br/><i>Default: True</i>')
    is_display_patient_mrn_report = models.BooleanField(verbose_name='Display patient MRN in the reports', default=True, help_text='Determines whether the MRN is displayed in the Report Headers of Clinical Viewer and Clinical View Agent.<br/><i>Default: True</i>')

    def __unicode__(self):
        return ""
      
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Patient MRN Display' 

        
def get_choice_value(choices, value):
    # Returns the value that presented to the user, according to the selected value that is saved in the database.
    # Use this method for choices that don't have standard index (0, 1, 2, 3...)
    return choices[[x[0] for x in choices].index(value)][1] 


    
class AppsPatientDisplayAgeCalculation(ConfigurationEntityBaseModel):
    cv_parent                   = models.ForeignKey('CvPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pv_parent_patient_display   = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pl_parent                   = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    display_text                = models.CharField(max_length=60, verbose_name= "", default='Patient younger than:')
    age_calc_time_span          = TimeSpanField(verbose_name='Patient Age Range (Upper Value)', min_value=1, choices=TIME_SPAN_CHOICES, default='{0}|{1}'.format(1, TIME_SPAN_CHOICES[0][0]), help_text="")
    date_format                 = models.CharField(verbose_name='Date Unit To Display', choices=DATE_FORMAT_CHOICES, blank=False, null=False, max_length=5, help_text="")
    priority_order              = models.IntegerField(verbose_name='Order', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)], help_text = "")
     
     
     
    def __unicode__(self):
 
#         num, unit = (self.age_calc_time_span.split('|'))
#         unit = get_choice_value(TIME_SPAN_CHOICES, int(unit)) 
#         dateFormat = get_choice_value(DATE_FORMAT_CHOICES, self.date_format)
#         return 'Time Span =%s %s and Date Format= %s' % (num, unit, dateFormat)
        return 'Rule #%s' % (self.priority_order)
       
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Patient Age Display'  
        verbose_name = 'Age Calculation Rule'    
    
class AppsPatientDisplayValueBaseProgram(ConfigurationEntityBaseModel):
    cv_parent                   = models.ForeignKey('CvPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pl_parent                   = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pv_parent_patient_display   = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    vbp_oid_system     = models.CharField(max_length=120, verbose_name= "System OID", null=True, blank=True, default='', help_text=get_help_text('Defines the patient system OID (root id), which represents the patient\'s ID in the Value Based Program (VBP). This OID should also be configured in VIA.<br/> For example: 2.16.840.1.113883.3.57.1.3.5.52.1.8.6','empty'))
    vbp_display_name     = models.CharField(max_length=5, verbose_name= "Display Name", null=True, blank=True, default='', help_text=get_help_text('If the patient is in a VBP, defines the VBP name displayed in the EHR Agent and Clinical Viewer header. The value cannot exceed 5 chars.','empty'))
    vbp_risk_score_code     = models.CharField(max_length=200, verbose_name= "Risk Score Code", null=True, blank=True, default='', help_text=get_help_text('Defines the Code (in CodeSystem|Code format) of the patient\'s Risk Score.<br/>Code can be local or baseline<br/>For example: 2.16.840.1.113883.3.57.1.2.17.89|0006<br/><b>Note: The code that is configured and the code used to store the Risk Score in the CDR are assumed to be the same.</b>','empty'))
    vbp_low_risk_score    = models.BooleanField(verbose_name= "Low", default=False, help_text='')
    vbp_medium_risk_score    = models.BooleanField(verbose_name= "Medium", default=False, help_text='')
    vbp_high_risk_score    = models.BooleanField(verbose_name= "High", default=False, help_text='')
    vbp_very_high_risk_score    = models.BooleanField(verbose_name= "Very High", default=False, help_text='')
    
    def __unicode__(self):
        return ""
      
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Value Based Program' 


class AppsPatientDisplayVBP(ConfigurationEntityBaseModel):
    cv_parent                   = models.ForeignKey('CvPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pv_parent_patient_display   = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    vbp_oid_system              = models.CharField(max_length=120, verbose_name= "System OID", null=False, blank=False, default='', help_text=get_help_text('Defines the patient system OID (root id), which represents the patient\'s ID in the Value Based Program (VBP). This OID should also be configured in VIA.<br/> For example: 2.16.840.1.113883.3.57.1.3.5.52.1.8.6','empty'))
    vbp_display_name            = models.CharField(max_length=5, verbose_name= "Display Name", null=False, blank=False, default='', help_text=get_help_text('If the patient is in a VBP, defines the VBP name displayed in the EHR Agent and Clinical Viewer header. The value cannot exceed 5 chars.','empty'))
    vbp_description            = models.CharField(max_length=1000, verbose_name= "Description", null=True, blank=True, default='')
    vbp_display_name_long     = models.CharField(max_length=60, verbose_name= "Display Name", null=True, blank=True, default='', help_text=get_help_text('If the patient is in a VBP, defines the VBP name displayed in the EHR Agent and Clinical Viewer header. The value should not exceed 15 chars.','empty'))    
    pl_parent                   = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    
    def __unicode__(self):
        return self.vbp_oid_system
      
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Value Based Program' 
        verbose_name = "Value Based Program (VBP) entry"
 

class AppsPatientDisplayMetricCodeBasedIndicator(ConfigurationEntityBaseModel):
    pv_parent_patient_display   = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    mci_oid_system              = models.CharField(max_length=200, verbose_name= "Metric code system|Code", null=False, blank=False, default='', help_text=get_help_text('Defines the code of the metric result that is formatted Code System|Code. Code can be local or baseline and it is a mandatory field to fill. Example: 2.16.840.1.113883.3.57.1.3.5.52.2.119|0130. Default: Empty'))
    mci_interpretation          = models.CharField(max_length=15, verbose_name='Interpretation', choices=INTERPRETATION_CHOICES, blank=False, null=False, help_text='Defines the interpretation of the metric result to display. Select the value from the drop down. Default: Empty')
    mci_label                   = models.CharField(max_length=15, verbose_name= "Indicator label", null=False, blank=False, default='', help_text='Defines the Indicator text to display in Agent Hub and the patient banner. Maximum text length allowed is 15 characters. Default: Empty')
    mci_priority                = models.PositiveIntegerField(verbose_name= "Priority", validators=[validators.MinValueValidator(1)], help_text = 'Defines the priority of the indicator to display within many metric code based indications. Allows entering only unique numeric values. Default: Empty')
    mci_tooltip                 = models.CharField(max_length=1000, verbose_name= "Tool tip", null=True, blank=True, default='', help_text='Defines the tooltip to display when hovering over an indicator when metric result text in the database is empty. Default: Empty')
    
    def __unicode__(self):
        return "[%s - %s]" % (self.mci_oid_system, self.mci_interpretation)
      
    class Meta:
        app_label = "dbmconfigapp"    
        unique_together = ("mci_oid_system", "mci_interpretation")
        history_meta_label = 'Metric Code Based Indicator' 
        verbose_name = "Metric Code Based Indicator entry"

class PvPatientNameDisplay(ConfigurationEntityBaseModel):
    pv_parent_patient_display   = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    pv_patient_name_display     = models.CharField(max_length=200, verbose_name= "Patient Name Display", null=False, blank=False, default='{FNAME}, |{GNAME} |{MNAME}', help_text=get_help_text('Defines the display name and the order of the patient display name parts. Only the parts configured will be displayed in patient view. Example: {GNAME}, |{FNAME}. Default: {FNAME}, |{GNAME} |{MNAME}'))
      
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = 'Patient Name Display'
        verbose_name = "Patient Name Display" 
          
class PlPatientDisplayPage(PageBaseModel):
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Patient Display'
        history_meta_label = verbose_name

class PatientDetailsSectionOrdering(ConfigurationEntityBaseModel):
    pl_parent  = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1)
    pv_parent_patient_display     = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    display_name = models.CharField(max_length=60, blank=True, verbose_name='Patient details section')
    code = models.CharField(max_length=60, blank=True)
    priority_order = models.IntegerField(verbose_name='Section order', help_text = "")

    class Meta:
        app_label = "dbmconfigapp"
    
        


