from django.db import models
from dbmconfigapp.models.base import ConfigurationEntityBaseModel
from dbmconfigapp.models.cvtables import DataElement, ClinicalDomain
from .common import Message
from dbmconfigapp.utils.custom_validators import *
from .base import *
from dbmconfigapp.models.patient_view import *



from django.core import validators

SELECTION_BEHAVIOR_CHOICES = (
    (1, 'Previous selected linkage set is cleared'),
    (0, 'Previous selected linkage set is not cleared')
    )


class PatientSearchPage(ClinicalDomain):
    
    def page_title(self):
        return "Set the %s Settings" % self.page_name
    
    class Meta:
        app_label = "dbmconfigapp"

class CvPatientSearch(PatientSearchPage):
    
    def get_tree_id(self):
        return "cv_patient_search"
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Patient Search (from Clinical Viewer)"



class CollaboratePatientSearchProperties(ConfigurationEntityBaseModel):
    parent                                 = models.ForeignKey(PatientSearchPage, on_delete=models.SET_NULL, default=14, null=True)
    pv_parent                              = models.ForeignKey('PVPatientSearchPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    MrnSystemSelectorMaxDropItems          = models.IntegerField(verbose_name='Max items displayed in the standard MRN System Selector dropdown list', validators=[validators.MinValueValidator(2), validators.MaxValueValidator(100)], default=6, help_text='Defines the maximum number of items that can be displayed in the standard MRN System Selector dropdown list. If the maximum value is exceeded, the enhanced MRN System Selector dropdown list is provided to display all the items on the list.<br/>The possible values are 2-100<br/><em>Default: 6</em>')
    MrnSystemSelectorMaxColumnCount        = models.IntegerField(verbose_name='Max columns displayed in the MRN System Selector dropdown list', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)], default=2, help_text='Defines the maximum number of columns that can be displayed in the MRN System Selector dropdown list.<br/>The possible values are 1-5<br/><em>Default: 2</em>')
    MrnSystemSelectorIsSortingEnabled      = models.BooleanField(verbose_name='MRN System Selector is sorted in ascending order', default=True, help_text='Supported by Clinical Viewer only.<br/>Determines whether the MRN System Selector dropdown list is sorted.<br/>If true, the list is sorted in ascending order.<br/>If false, the list is not sorted and the displayed order is taken from the configuration of the systems.<br/><em>Default: True</em>')
    MrnSystemSelectorIsEmptyItemEnabled    = models.BooleanField(verbose_name='MRN System Selector is enabled if it is empty', default=True, help_text='Supported by Clinical Viewer only.<br/>Determines whether the MRN System Selector dropdown list is enabled if it is empty.<br/>If true, the application adds an item titled Empty and if a user selects this item, the selected system is null.<br/>If false, the list is disabled when empty.<br/><em>Default: True</em>')
    PatientSearch_IsDirectEnterPatientFile = models.BooleanField(verbose_name='Enter the patient\'s file automatically when the search results via MRN return a cluster', default=True, help_text='Determines whether when the search results via MRN return a cluster, the system automatically enters the patient&#39;s file.<br/>If False, the system displays the cluster and the user can then choose to enter the patient&#39;s file.<br/>In External Mode access, this value is always True<br/>Note : Affects only Clinical Viewer and Patient View<br/><em>Default: True</em>')
    PatientSearch_IsDirectEnterPatientFile_Demographics = models.BooleanField(verbose_name='Enter the patient\'s file automatically when the search results via Demographics return a cluster', default=True, help_text='Determines whether when the search results via demographics return a cluster, the system automatically enters the patient&#39;s file.<br/>If False, the system displays the cluster and the user can then choose to enter the patient&#39;s file.<br/>In External Mode access, this value is always True<br/>Note : Affects only Clinical Viewer<br/><em>Default: True</em>')
    PatientSearch_IsDirectEnterPatientFile_Demographics_MinScore = models.IntegerField(verbose_name='Minimum score', validators=[validators.MinValueValidator(0), validators.MaxValueValidator(10000)], default=140, help_text='Determines the minimum score, to enter the patient file automatically following a demographic search, when a single cluster is returned. If the score is lower, the system displays the cluster, and the user can then choose to enter the patient\'s file.<br/>Note: Affects only Clinical Viewer, including External Mode access.<br/><em>Default: 140</em>')    
    LeadingPatientRecordPolicy             = models.CharField(verbose_name='Leading patient record policy', blank=True, max_length=500, default="", help_text='Supported by Clinical Viewer only.<br/>Determines the Leading Patient Record (including which MRN is displayed in the Patient Details header and in the Demographics clinical view) in response to a Patient Search by MRN.<br/>This includes the Leading Patient Record that opens in the following cases:<br/>&nbsp;&nbsp;&nbsp;&nbsp;- When launching the Clinical Viewer from an EHR.<br/>&nbsp;&nbsp;&nbsp;&nbsp;- When launching the Clinical Viewer from EHR Agent or Collaborate.<br/>&nbsp;&nbsp;&nbsp;&nbsp;- When searching for the patient by MRN.<br/><b>By default,</b> the leading record chosen will be the record with the same MRN that the user entered in the Patient Search.<br/>The following configurable options enable the customer to determine cases in which the Leading Patient Record will be the first index returned by the MPI.<br/>In these cases, the MPI might determine a Leading Patient Record with a different MRN than the MRN used in the Patient Search.<br/>The following configurable options are available. In all of the following cases, the CV will choose the first record returned by the MPI regardless of the MRN used in the Patient Search or in the launching application.<br/><b>EMR1|EMR2 =</b> In the case of Clinical Viewer launch from <b>only these defined client applications.</b> If the CV is launched from any undefined application, the behavior is the default behavior.<br/><b>All =</b> In the case of Clinical Viewer launch from any (all) existing client applications.<br/><b>Empty =</b> In the case of an MRN search when the clientApplicationId was not sent by the EHR or launching application (as configured in the Launch API). This includes also a case where the CV is launched by an undefined application (for example if a user opened a browser and accessed the CV login page).<br/><em>Default: No default value</em>')
    System_label                           = models.CharField(blank=True, verbose_name='Enter the label for System',  max_length=120, default="System",)
    MRN_label                              = models.CharField(blank=True, verbose_name='Enter the label for MRN', max_length=120,default="MRN")
    MinSQQ                                 = models.IntegerField(verbose_name='Minimum SQQ score', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)], default=50, help_text='Defines the minimum MPI SQQ score (quality of a search query) from which VIA will return records.<br/>Before submitting the patient search query, it must undergo a quality check to minimize the possibility of a large number of search results.<br/>The SQQ score is determined by calculating the sum of weights of the various search attributes that participate in the query.<br/>Only if the SQQ score is equal to or greater than the MinSQQ value, the search query passes the quality check.<br/><em>Default: 50</em>')
    ContinueSearchAfterSQQCheckFailure     = models.BooleanField(verbose_name='Continue search although SQQ score is too low', default=False, help_text='Determines whether if the configured MinSQQ score is too low, the user is given an option to continue the search.<br/>If True, a message is displayed enabling the user to continue the search or cancel it.<br/>If false, a message informs the user that the score is too low and the search is discontinued.<br/><em>Default: False</em>')
    DemographicSearch_AutoEnter            = models.IntegerField(blank=True,null=True,verbose_name='Enter the patient\'s file automatically using Demographic search', validators=[validators.MinValueValidator(1)], help_text='This configuration determines when the system will auto enter into a patient\'s file using demographic search.<br/>Auto enter, using demographic search, happens only when the search result\'s return one cluster and the OOB strength of the search fields is more than the strength defined in this configuration.<br/>If Empty, the system displays the cluster and the user can then select to enter the patient\'s file. This configuration only allows numeric values.<br/><b>Note :</b> Affects only Patient View, stand alone and Launch API modes.<br/><em>Default: Empty</em>')
    PatientSearch_LeadingPatientRecordPolicy = models.BooleanField(verbose_name=b"Leading patient record policy (When the searched MRN and source is not found)", default=False, help_text=b'Determines leading index if VIA response does not have searched MRN and source. The leading index is selected based on configuration:<br/>False - Use the same MRN from a different source, else first index from the VIA response is selected.<br/>True - Use the first index from VIA response.<br/><em>Default: False</em>')
   
    def __unicode__(self):
        return ''

    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Patient Search"

# represents the first data elements grid in the page
class PatientSearchDataElement(DataElement):
        
    class Meta:
        app_label = "dbmconfigapp"    
        history_meta_label = "Patient Search Results Grid"
        
# represents the second data elements grid in the page
class PatientSearchHistoryDataElement(DataElement):
        
    class Meta:
        app_label = "dbmconfigapp"      
        history_meta_label = "Patient Search History Grid"
        
class PatientSearchDisplayOptions(ConfigurationEntityBaseModel):
    patient_search_page     = models.ForeignKey(PatientSearchPage, on_delete=models.SET_NULL, default=14, null=True)
    pv_patient_search_page     = models.ForeignKey(PVPatientSearchPage, on_delete=models.SET_NULL, default=1, null=True)
    display_warning         = models.BooleanField(default=False, verbose_name='Display a warning message when the selected leading record has no data', help_text='Note: Only for Clinical Viewer<br>Determines whether the system displays a warning message when the selected leading record has no data. In this case the system displays the latest record (from those selected by the user) for the same patient that exists in the CDR.<br>If True, a message informs the user that the leading record has been changed.<br>If False, no message is displayed.<br><i>Default: True</i>')
    cluster_selection_behavior  = models.IntegerField(verbose_name='Cluster selection behavior', choices=SELECTION_BEHAVIOR_CHOICES, blank=False, default=0, help_text='Supported by Clinical Viewer only.<br/>This configuration enables or disables the option to clear the previously selected linkage set.<br><i>Default: Previous selected linkage set is not cleared</i>')
    display_user_attestation    = models.BooleanField(default=False, verbose_name='Display Confirmation Message Before User Enters Patient Record', help_text=get_help_text('Determines whether the system displays a confirmation message before the user enters the patient record.<br>True: A confirmation message is displayed.<br>False: No message is displayed.<br>Note: This configuration is supported by Agent hub.<br><i>Default: False</i>'))
    attestation_text            = models.TextField(blank=True, null=True, verbose_name='Attestation Message Text', help_text=get_help_text('Define the Attestation Message Text displayed to the user','Please note that you are about to enter the patient record. Please confirm you requested to view the patient clinical information explicitly for treatment reasons only, and not for other reasons (such as research, etc).'))
    authority_text              = models.CharField(blank=True, null=True, max_length=260, verbose_name='Specify patient assigning authority to enable retry', help_text=get_help_text('Define the patient assigning authority used to retry fetch patient data that exists in the enterprise master patient index (EMPI), but not in the dbMotion Clinical Data Repository (CDR). If the patient assigning authority is defined, the system attempts to fetch patient data for 10 seconds. If the patient assigning authority is not defined, the feature is unavailable.'))
    enable_death_indicator      = models.BooleanField(verbose_name='Display Deceased indicator on patient search results grid', default=True, help_text=get_help_text('Specifies if the Deceased indicator is displayed in the patient search results grid.<br><i>Default: True</i>'))

    def __unicode__(self):
        return ""
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Display Options"
        

######################################################################

class EmergencyDeclarationText(ConfigurationEntityBaseModel):
    patient_search_page     = models.ForeignKey(PatientSearchPage, on_delete=models.SET_NULL, default=14, null=True)
    pv_emg_declaration_patient_search = models.ForeignKey('PVPatientSearchPage', on_delete=models.SET_NULL, null= True, default = 1, editable=False) 
    text         = models.TextField(verbose_name='Text', blank=True, help_text=get_help_text('Define the Emergency Declaration Text which will be displayed in the Declare Emergency windows.','Organizational policy prevents some patient information from being displayed. Restrictions about patient data can be overridden. To view the data in emergency mode, select a reason to remove the restriction and click Break Glass. To continue without viewing the restricted data, click Cancel. All override actions are audited.<br/><i>Note: there is a permanent text always displayed on Emergency Declaration dialog: "To view the patient record in Emergency mode, select a Reason for Declaration and Click Break Glass. To Exit without viewing the patient record, click Cancel".</i>'))
    
    def __unicode__(self):
        return ""
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Emergency Declaration Text"

        
class EmergencyDeclarationReasons(Message): 
    pv_patient_search = models.ForeignKey('PVPatientSearchPage', on_delete=models.SET_NULL, null= True, default = 1, editable=False) 
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Emergency Declaration Reasons"
        verbose_name = "Emergency Declaration Reason"
        unique_together = ("culture", "message")
         
class PatientSearchTooltip(Message):
    pv_parent = models.ForeignKey('PVPatientSearchPage', on_delete=models.SET_NULL, null= True, default = 1, editable=False)  
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Patient Search Tooltips"
        unique_together = ("culture", "message")

DEFAULT_SEARCH_CHOICES = (
    (0, 'Search by MRN'),
    (1, 'Search by Demographics')
    )

class PatientSearchDefaultSearch(ConfigurationEntityBaseModel):
    patient_search_page = models.ForeignKey(PatientSearchPage, on_delete=models.SET_NULL, default=14, null=True)
    default_search = models.IntegerField(verbose_name='Default Search method', choices=DEFAULT_SEARCH_CHOICES, blank=False, default=1, help_text='Supported by Clinical Viewer only.<br/>Defines the default type of the patient search method.<br><i>Default: Search by Demographics</i>')
    
    def __unicode__(self):
        return ""
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Default Patient Search"
        