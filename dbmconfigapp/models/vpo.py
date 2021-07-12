from .base import models, ConfigurationEntityBaseModel, SEARCH_OPTIONS_CHOICES, get_help_text

LOCAL_CODE_DISPLAY_PRIORITIES_CHOICES = (
    ('Designation,DisplayName', 'Designation, DisplayName'),
    ('DisplayName,Designation', 'DisplayName, Designation'),
                                 )

LABS_METHOD_TYPE_CHOICES = (
    ('MIC', 'MIC: Displays all types of test results in a MIC captioned column.'),
    ('KB', 'KB: Displays all types of test results in a KB captioned column.'),
    ('Both', 'Both: Displays all types of results in a Zone\MIC captioned column and also the following designation in the Remarks column: Vocabulary Domain designation or Method Unknown.'),
                                 )

RANGE_RECORDS_TO_DISPLY = (
        (-1, 'All'),
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

FACILITY_SOURCE_CHOICES = (
    (0, 'Display the first participant organization'),
    (1, 'Display the first parent of the first participant organization'),
    (2, 'Display the first participant or parent organization that is defined by the INS (institute) code'),
                             )

DEF_FACILITY = 2

SSN_DIGITS_TO_DISPLAY_CHOICES = (
        (-1, 'All'),
        (0, 'Do not display'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
    )

CLINICAL_DATA_DISPLAY_OPTIONS_CHOICES = (
    (0, 'Only the returned calculated value is displayed on the page'),
    (1, 'The displayName from the original message is added in brackets (concatenated) to the calculated value')
    )

CODE_SYSTEM_NAME_DISPLAY_CHOICES = (
    (0, 'Display the CodeSystem Name only as a tooltip when the user hovers the cursor over the Code column'),
    (1, 'Display the CodeSystem Name in parentheses attached to the Code within the Code column'),
    )

FILTER_TYPE_CHOICES = (
    (0, 'Filter Out'),
    (1, 'Filter In')
    )

GROUPING_CODE_CHOICES = (
    (1, 'Baseline, Local'),
    (0, 'Local, Baseline'),
    )

def summary_top_help_text(domain, domains, default):
    return "Defines the number of the patients' latest %s records to display in the %s Summary.<br><i>Default: %s</i>" % (domain, domains, default)

CODE_SYSTEM = '&lt;code system&gt;|&lt;code&gt;'
CODE_SYSTEM_FORMAT = CODE_SYSTEM + '^' + CODE_SYSTEM
CODE_SYSTEM_FORMAT_TEMPLATE = '(using the %s format)' % CODE_SYSTEM_FORMAT

## IMPORTANT
## 1. Avoid setting default values here - the default value should be set in the Migration (when adding the record)
## 2. blank=True, null=True - for everyone except for CHOICES (radio button) field which should include only null=True 
class Vpo(ConfigurationEntityBaseModel):
    clinical_domain                     = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True, editable=False)
    cv_patient_display                  = models.ForeignKey('CvPatientDisplayPage', on_delete=models.SET_NULL, null=True, editable=False)
    pl_patient_display                  = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, editable=False)
    reporting_cv                        = models.ForeignKey('CVReportingPage', on_delete=models.SET_NULL, null=True, editable=False)
    reporting_pl                        = models.ForeignKey('PlReportingPage', on_delete=models.SET_NULL, null=True, editable=False)
    reporting_pv                        = models.ForeignKey('PVReportingPage', on_delete=models.SET_NULL, null=True, editable=False)    
    cv_general                          = models.ForeignKey('ClinicalViewerGeneralPage', on_delete=models.SET_NULL, null=True, editable=False)
    pv_parent                           = models.ForeignKey('PVMeasurementPage', on_delete=models.SET_NULL, null=True, default=None, editable=False)
    pl_parent                           = models.ForeignKey('PlGeneralPage', on_delete=models.SET_NULL, null=True, default=None, editable=False)
    pv_grouping_mode                    = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=None, editable=False)       
    pv_parent_patient_display           = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=None, editable=False)   
    patient_id_type_display_priority    = models.CharField(verbose_name='Patient ID display priority', default='', blank=True, null=True, max_length=20, help_text='This configuration applies to Clinical Viewer only.<br/>Defines the priority for displaying the patient ID in the Patient Details header (can be used to display the patient\'s PHIN instead of displaying the MRN), using the &lt;code&gt;|&lt;code&gt; format.<br/><i>Default: MRN|SSN</i>')
    pv_patient_id_type_display_priority = models.CharField(verbose_name='Patient ID display priority', default='', blank=True, null=True, max_length=100, help_text='This configuration applies to Patient View.<br/>Defines the priority for displaying the patient ID in the Patient Banner, this configuration can be used to display the patient\'s PHIN instead of displaying the MRN.<br/>Patient View - using the &lt;code&gt;^label|&lt;code&gt;^label format, user can define the code priority and label of it for displaying on Patient Banner.<br/>If label is not configured, by default code is displayed as label.<br/><i>Default: MRN|SSN</i>')
    patient_name_type_priority          = models.CharField(verbose_name='Name parts sorting order', default='', blank=True, null=True, max_length=20, help_text='Defines the sorting order of name parts to display in the Name grid , using the &lt;code&gt;|&lt;code&gt; format.<br/><i>Default: FAM|GIV|PFX</i>')
    medical_staff_types_priority        = models.TextField(verbose_name='Priority of Medical staff types', blank=True, null=True, help_text='Defines the code ' + CODE_SYSTEM_FORMAT_TEMPLATE + ' used to determine the priority order for displaying the Medical Staff type in the Document label.<br/>For example, if the priority is Author, Authenticator, then the Author of the document is displayed. If there is no Author, the Authenticator is displayed.<br/>If both exist, the first is displayed.<br/><i>Default: 2.16.840.1.113883.5.90|AUT^2.16.840.1.113883.5.90|AUTHEN</i>')
    filter_mood_codes                   = models.TextField(verbose_name='Mood Codes to filter out', blank=True, null=True)
    encounter_types_to_display          = models.TextField(verbose_name='Encounter types to display', blank=True, null=True, help_text='Defines which Encounter Types to filter (to display) in the Encounter Summary grid. By default all Types are displayed.<br/>To display only one or multiple specific Encounter Types, the ' + CODE_SYSTEM_FORMAT + ' format must be used.<br/><i>Default: ALL</i>')
    encounters_remove_duplicated        = models.BooleanField(verbose_name='Remove duplicated Location records', default=False, blank=True, help_text='Determines whether to display all Locations in the Location History grid as retrieved (that is, including, if relevant, the same location consecutively more than once) or to filter the Locations by removing consecutive duplicate records.<br/>If True, the second and any subsequent consecutive duplicate location records are removed.<br/>If False, all locations records are displayed as retrieved.<br/><i>Default: False</i>')
    encounters_enable_episode_filter    = models.BooleanField(verbose_name='Enable Episode filter', default=False, blank=True, help_text='Determines whether to Enable the Episode Filter<br/>When the value is True, only Encounters with End date = Null with Inpatient Code =2.16.840.1.113883.5.4|IMP are treated as open encounters (Episode). Emergency Code =2.16.840.1.113883.5.4|EMER will cause encounters to be treated as episodes based on the Duration of emergency encounter parameter (below) and other Encounter codes will be treated as closed encounters (Events).<br/>When the value is False, every encounter with End date = Null is treated as an open encounter (an Episode). Duration of emergency encounter parameter is ignored.<br/><i>Default: False</i>')
    encounters_emergency_threshold      = models.PositiveSmallIntegerField(verbose_name='Duration of emergency encounter', blank=True, null=True, help_text='This configuration point is only relevant if the Enable Episode Filter parameter (above) is True.<br/>Defines the duration, in number of hours, of an Emergency Encounter when there is no Discharge Date (Discharge Date = NULL).<br/><i>Default: 24</i>')
    lab_susceptibility_methods_code_type = models.CharField(verbose_name='Labs method type', max_length=20, null=True, choices=LABS_METHOD_TYPE_CHOICES, help_text='Determines how the Lab Results and Lab Results History clinical views and reports (in the Clinical Viewer, Collaborate, Patient List and EHR Agent applications) display the types of Microbiology Test results.<br/><i>Default: %s</i>' % LABS_METHOD_TYPE_CHOICES[0][1])
    summary_top_encounters              = models.IntegerField(choices=RANGE_RECORDS_TO_DISPLY, verbose_name='Number of Encounter records to display', default=-1, null=False, help_text=summary_top_help_text('Encounter', 'Encounters', '4')) 
    summary_top_allergy_intolerance     = models.IntegerField(choices=RANGE_RECORDS_TO_DISPLY, verbose_name='Number of Allergy records to display', default=-1, null=False, help_text=summary_top_help_text('Allergy', 'Allergies', '4'))
    summary_top_conditions              = models.IntegerField(choices=RANGE_RECORDS_TO_DISPLY, verbose_name='Number of Problem records to display', default=-1, null=False, help_text=summary_top_help_text('Problem', 'Problems ', '5'))
    summary_top_laboratory_events       = models.IntegerField(choices=RANGE_RECORDS_TO_DISPLY, verbose_name='Number of Lab records to display', default=-1, null=False, help_text=summary_top_help_text('Lab', 'Labs', 'All'))
    summary_top_substance_administration= models.IntegerField(choices=RANGE_RECORDS_TO_DISPLY, verbose_name='Number of Medication records to display', default=-1, null=False, help_text=summary_top_help_text('Medication', 'Medications', 'All'))
    summary_med_filter_undefined_status = models.BooleanField(verbose_name='Display Medications whose status is Undefined.', default=False, blank=True, help_text='Determines whether to filter (display) Medications whose status is Undefined.<br/>If True, the medication is displayed.<br/>If False, the medication is not displayed.<br/><i>Default: True</i>')
    summary_time_filter_amount_labs     = models.PositiveSmallIntegerField(null=True)
    summary_time_filter_unit_labs       = models.IntegerField(choices=SEARCH_OPTIONS_CHOICES, verbose_name='', null=False, default=0)
    summary_time_filter_amount_encounter = models.PositiveSmallIntegerField(null=True)
    summary_time_filter_unit_encounter  = models.IntegerField(choices=SEARCH_OPTIONS_CHOICES, verbose_name='', null=False, default=0)
    summary_time_filter_amount_meds     = models.PositiveSmallIntegerField(null=True)
    summary_time_filter_unit_meds       = models.IntegerField(choices=SEARCH_OPTIONS_CHOICES, verbose_name='', null=False, default=0)
    domains_to_hide_uom                 = models.TextField(verbose_name='Vitals Measurements in which to hide the UOM', blank=True, null=True, help_text='Defines the Vital Signs measurement in which the UOM (Unit of Measurement) is hidden (not displayed), by default.<br/>Note: Multiple measurements should be separated by commas (Example: BodyWeight,BodyHeight).<br/><i>BloodPressure</i>') # currently this field is not displayed - updated by DataElement form
    domains_to_concatenate_values       = models.TextField(verbose_name='Vitals Measurements to display with concatenated values', blank=True, null=True, help_text='Defines the Vitals Measurements to be displayed as concatenated. For example: 65 kg 50 g or 65.5 kg<br/>Note: Multiple measurements should be separated by commas (Example: BodyWeight,BodyHeight).<br/><i>BloodPressure</i>') # currently this field is not displayed - updated by DataElement form
    filter_cancelled_items              = models.BooleanField(verbose_name='Filter cancelled items', default=False)
    filter_status_code                  = models.TextField(verbose_name='%s filter status code', blank=True, null=True, help_text='Defines the code used to filter the %s list (using the &lt;code system&gt;|&lt;code&gt^&lt;code system&gt|&lt;code&gt; format).<br/><i>Default: %s</i>')
    unit_priority_list_body_weight      = models.TextField(null=True, blank=True)
    unit_priority_list_body_height      = models.TextField(null=True, blank=True)
    patient_privacy_indicate_minority   = models.NullBooleanField(verbose_name='Indicate if a patient is a minor', help_text=get_help_text('This configuration applies to Clinical Viewer and Patient View.<br/>Determines whether the system indicates if a patient is a minor in the Patient Details area.', 'False'))
    patient_privacy_minor_min           = models.PositiveSmallIntegerField(null=True, verbose_name='Minor minimum age', help_text=get_help_text('This configuration applies to Clinical Viewer and Patient View.<br/>Defines the minimum age in years (inclusive) that determines if the patient is a minor.', '11'))
    patient_privacy_minor_max           = models.PositiveSmallIntegerField(null=True, verbose_name='Minor maximum age', help_text=get_help_text('This configuration applies to Clinical Viewer and Patient View.<br/>Defines the maximum age in years (inclusive) that determines if the patient is a minor.', '18'))
    lab_report_fixed_width_font         = models.BooleanField(verbose_name='Display report text in fixed-width font', default=True, help_text='Determines whether to show the Lab Report Remark and Result text in fixed-width font.<br/>True: Displays text in fixed-width font.<br/>False: Does not display text in fixed-width font.<br/><i>Default: True</i>')
    facility_filter_enable              = models.BooleanField(default=False, help_text=get_help_text("Determines whether the User Facility filter is enabled.<br/>If false, the user will see the patient record regardless of the facility related to the patient's acts.<br/>If true, the user will only be authorized to enter the patient record if at least one patient index includes the user's facility or a child of the user's facility. If no patient index includes the user facility, the user will not be authorized to enter patient file (the system's behavior will be identical to the behavior that occurs with patient confidentiality).", "false"))
    user_facility_root_oid              = models.CharField(max_length=40, verbose_name='User Facility Root OID', blank=True, null=True, help_text=get_help_text("Defines the root Identifier of the Facility for which the Facility filter is enabled. This identifier enables the system to identify all the relevant parent and child facilities. This OID must be identical to the root OID that was used to load the customer's organizational structure to dbMotion CDR.", "empty"))
    grouping_mode                       = models.IntegerField(choices=GROUPING_CODE_CHOICES, default=1, null=True, verbose_name='Grouping Priority Order', help_text=get_help_text('Determines the priority order for grouping:<br>Baseline, Local: First, group by baseline subdomain; if local code is unmapped, group by local subdomain.<br>Local, Baseline: First, group by local subdomain; if local code is under the root domain, and is mapped to a baseline code, group by baseline subdomain.<br>If local code is unmapped and is under a root domain, display under "Others".<br>This configuration applies to Clinical Viewer, EHR Agent and Patient View .', 'Baseline, Local'))
    

    def __unicode__(self):
        return ""
    
    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = 'Business Rules'

# Notes:        
# clinical_data_display_options should have been Boolean but this causes Django to add the 'None' option as first radio button no matter what.
class VpoCommon(ConfigurationEntityBaseModel):
    clinical_domain                     = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True, editable=False)
    cv_general                          = models.ForeignKey('ClinicalViewerGeneralPage', on_delete=models.SET_NULL, null=True, editable=False)
    pl_parent                          = models.ForeignKey('PlGeneralPage', on_delete=models.SET_NULL, null=True, default=None, editable=False)        
    clinical_data_display_options       = models.IntegerField(verbose_name='Concatenate Display Name', choices=CLINICAL_DATA_DISPLAY_OPTIONS_CHOICES, null=True, default=0, help_text=get_help_text('Determines how clinical data is displayed in the Clinical Viewer.<br/>This configuration affects the Clinical Viewer page and all the reports.<br/>The behavior of this parameter depends on the Local/Baseline/Calculated property definitions and the value of the &lt;clinical view domain&gt;_LocalCodeDisplayPriorities parameter as configured for that page.<br/>If the displayName in the original message received from the customer, is different from the value that is returned after the calculation, the system behaves as follows:<br/>First option: Only the returned calculated value is displayed on the page.<br/>Second option: The displayName from the original message is added in brackets (concatenated) to the calculated value.<br/>This parameter is relevant for the following clinical data fields:<br/>- Summary page Allergy grid: Allergy To<br/>- Summary page Problems grid: Problem<br/>- Summary page Labs grid: Test<br/>- Daily Summary page Labs grid: Test<br/>- Problem List grid: Problem<br/>- Allergies page Allergies grid: Allergy To<br/>- Immunizations page Immunizations grid: Name<br/>- Labs page Labs grid: Test<br/>- Lab Results page Labs Results grid: Test<br/>- Diagnoses page Diagnoses grid: Diagnosis<br/>- Procedures page Procedures grid: Procedure<br/>- Daily Summary Procedures grid: Procedure', CLINICAL_DATA_DISPLAY_OPTIONS_CHOICES[0][1]))
    code_system_name_display            = models.IntegerField(verbose_name='CodeSystem name display within the Code column', choices=CODE_SYSTEM_NAME_DISPLAY_CHOICES, default=0, help_text=get_help_text('Determines how to display the CodeSystem name.<br/>This configuration affects the Clinical Viewer page and the Clinical Summary Selected Items report.',CODE_SYSTEM_NAME_DISPLAY_CHOICES[0][1]))
    
    def __unicode__(self):
        return ""
    
    class Meta:
        app_label = "dbmconfigapp"   
    

class VpoPPOL(ConfigurationEntityBaseModel):
    clinical_domain                     = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True, editable=False)
    cv_patient_display                  = models.ForeignKey('CvPatientDisplayPage', on_delete=models.SET_NULL, null=True, editable=False)
    pl_patient_display                  = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True, editable=False)
    pv_patient_display                  = models.ForeignKey('PVPatientSearchPage', on_delete=models.SET_NULL, null=True, editable=False)#why it's not patient search ?
    pv_parent_patient_display           = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    patient_privacy_mask_ssn            = models.IntegerField(null=False, default=0, choices=SSN_DIGITS_TO_DISPLAY_CHOICES, verbose_name='number of SSN digits to display', help_text=get_help_text('This configuration applies to Clinical Viewer and Collaborate.<br/>Defines the number of SSN digits to display (masking the rest).<br/>For example, if the number is 4, then only the last 4 digits of the SSN will be displayed.<br/>This configuration affects the Identifiers grid in Demographics page and the Search Results grid in Patient Search page.', '4'))
    patient_privacy_remove_excluded_clusters = models.NullBooleanField(verbose_name='Filter patient cluster when patient is partially confidential', default=False,
                                                help_text=get_help_text('Determines whether the system does NOT return a patient cluster which includes at least one confidential patient index that the user does not have permission to see.<br/>If True, clusters with at least one confidential index that the user does not have permission to see will NOT be returned.<br/>If False, the cluster will be returned; however, the indexes that the user does not have permission to see will be disabled.<br/>This configuration is supported by CV and Agent Hub.', 'False'))
    
    def __unicode__(self):
        return ""
    
    class Meta:
        app_label = "dbmconfigapp"   
    
# Looks like this class is not in use anymore
class VpoEHRAgent(ConfigurationEntityBaseModel):
    parent_cv_general                   = models.ForeignKey('ClinicalViewerGeneralPage', on_delete=models.SET_NULL, null=True, editable=False)
    pl_parent                          = models.ForeignKey('PlGeneralPage', on_delete=models.SET_NULL, null=True, default=None, editable=False)    
    return_act_organization_as_unit     = models.NullBooleanField(verbose_name='Display of the organization related to patient\'s clinical data')
    use_org_type_mode                   = models.NullBooleanField(verbose_name='Calculating the Facility field')
    facility_source                     = models.IntegerField(verbose_name='Calculation of the Facility field', null=True, choices=FACILITY_SOURCE_CHOICES, help_text=get_help_text('Determines how to calculate the organization shown in the Facility field.<br/>This configuration affects both Clinical Viewer and EHR Agent.', FACILITY_SOURCE_CHOICES[DEF_FACILITY][1]))
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Business Rules'

class VpoFacilityDisplay(ConfigurationEntityBaseModel):
    parent_cv_general                   = models.ForeignKey('ClinicalViewerGeneralPage', on_delete=models.SET_NULL, null=True, editable=False, default=1)
    pl_parent                          = models.ForeignKey('PlGeneralPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)       
    clinical_domain                     = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True, editable=False)
    patient_view                     = models.ForeignKey('PatientViewPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    
    display_name                        = models.CharField(verbose_name='Clinical Domain', max_length=60, unique=True)
    return_act_organization_as_unit     = models.NullBooleanField(default=True, verbose_name='Display of the organization related to patient\'s clinical data')
    use_org_type_mode                   = models.NullBooleanField(default=True, verbose_name='Calculating the Facility field')
    facility_source                     = models.IntegerField(verbose_name='Calculation of the Facility field', null=False, default=2, choices=FACILITY_SOURCE_CHOICES, help_text=get_help_text('Determines how to calculate the organization shown in the Facility field.<br/>This configuration affects Clinical Viewer, EHR Agent, Patient View and Patient List. ', FACILITY_SOURCE_CHOICES[DEF_FACILITY][1]))

    def __unicode__(self):
        return self.display_name

    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Facility Display Prioritization'
        verbose_name_plural = "Facility Display Prioritization"
        
    def save(self):
        self.return_act_organization_as_unit = self.facility_source > 0
        self.use_org_type_mode = self.facility_source == 2
        super(VpoFacilityDisplay, self).save()
#venky
class VpoEHRAgentDomains(ConfigurationEntityBaseModel):
    '''    
    This Model is connected to the Services: VPO, EHR Agent.
    To add the "EHR Agent Client" to the "Services to restart" list add the following code to the Admin class:

    def get_services_to_restart(self):
        from dbmconfigapp.models.base import ModelDescriptor, Service
        return list(ModelDescriptor.objects.get(model_name=self.get_db_model_descriptor()).services.filter(need_restart=True)) + [Service.objects.get(code_name='EHRAgentClient')]
        
        OR use super:
        qs = super([your_class], self).get_services_to_restart()
        # continue with qs...
        
    '''
    clinical_domain                     = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True, editable=False)
    filter_codes                        = models.TextField(blank=True, null=True)
    filter_type                         = models.SmallIntegerField(default=0, choices=FILTER_TYPE_CHOICES)
    pv_parent							= models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)

    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Filtering Clinical Data'
        verbose_name_plural = 'Filtering Clinical Data'
        
        

class VpoCommunication(ConfigurationEntityBaseModel):
    parent_cv_general                   = models.ForeignKey('ClinicalViewerGeneralPage', on_delete=models.SET_NULL, default=1, null=True, editable=False)
    pl_parent                          = models.ForeignKey('PlGeneralPage', on_delete=models.SET_NULL, null=True, default=None, editable=False)    
    pvp_parent                          = models.ForeignKey('PatientViewPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)    
    is_encounter_conf_inheritance       = models.BooleanField( verbose_name='Enable encounter confidentiality inheritance flow', default=True, help_text=get_help_text('Determines whether to enable the inheritance from an encounter to its related acts.<br/>It also supports the inheritance of the encounter type code confidentiality to its related acts.<br/>This configuration affects Clinical viewer, Clinical View Agent, Patient View, SDK. In addition, supported when dbMotion serves as an XDS.b repository.<br/>For more information, look for "Data type level confidentiality" in the "Data Integration Layer Implementation Guide" ', 'True'))
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Confidentiality'
        verbose_name = 'Confidentiality'
    
    
    
    