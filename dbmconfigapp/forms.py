from django import forms
from dbmconfigapp.models.cvtables import *
from dbmconfigapp.models.ehragent_clinical_domains import EHRAgentCVCommonClinicalDomainsProperties
from dbmconfigapp.models.clinical_domain_laboratory import LabChartDisplayOptions
from dbmconfigapp.models.apps_reporting import AppsReporting, LOGO_MAX_WIDTH, LOGO_MAX_HEIGHT
from dbmconfigapp.models.vpo import Vpo, CODE_SYSTEM_FORMAT_TEMPLATE, VpoCommon
from django.forms.models import BaseInlineFormSet
from dbmconfigapp.models.clinical_viewer_general import WebCulture, ExternalApplicationParameter, DBM_PARAMETERS_CHOICES
from dbmconfigapp.models.patient_view import CarequalityIntegrationSettingsModel
from dbmconfigapp.models.patient_view import PrefetchSettingsModel
from dbmconfigapp.models.direct_messaging_acdm import DirectMessagingAcdm
from dbmconfigapp.models.operational_manager import UsageReports, Status
from dbmconfigapp.models.clinical_code_display import ClinicalCodeDisplay
from dbmconfigapp.models.apps_patient_display import AppsPatientDisplayVBP
from dbmconfigapp.models.apps_patient_display import AppsPatientDisplayMetricCodeBasedIndicator
from dbmconfigapp.models.apps_patient_display import PvPatientNameDisplay
from dbmconfigapp.models.patient_view import PatientViewPage, LOGO_MAX_WIDTH, LOGO_MAX_HEIGHT, ImagingPacsDisclaimer
import xml.etree.ElementTree as ET

class ClinicalDomainAdminForm(forms.ModelForm):
    
    show_cancelled_selected         = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'widget-indent'}), label='"Show Cancelled" is selected')
    grouped_by_selected             = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'widget-indent'}), label='"Grouped By" option is selected')
    
    class Meta:
        model = ClinicalDomainProperties
        fields = '__all__'


class ClinicalDomainDataElementsAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClinicalDomainDataElementsAdminForm, self).__init__(*args, **kwargs)
        self.fields['enable'].help_text = "Determines whether or not the column is displayed"
        if ('page_width' in self.fields): self.fields['page_width'].help_text = "Defines the column width, as a percentage of the screen's width."
        if ('page_width' in self.fields): self.fields['page_width'].verbose_name = 'Column Width'
        if ('order' in self.fields): self.fields['order'].help_text = "Determines the order of the column in the grid"

    class Meta:
        model = DataElement
        fields = '__all__'


def CheckTimeFields(self, cleaned_data, fld_amount, fld_unit):         
    if cleaned_data.get(fld_unit)<4:
        if cleaned_data.get(fld_amount, None)==None:
            unit_name = ''
            for unit in SEARCH_OPTIONS_CHOICES_ENLARGED:
                if unit[0] == cleaned_data.get(fld_unit):
                    unit_name = unit[1]
            self._errors[fld_amount] = ErrorList([u'Please provide number of %ss' % unit_name])
    else:
        if cleaned_data.get(fld_amount, None)==None:
            cleaned_data[fld_amount] = 0
    
class ClinicalDomainTimeFilterAdminForm(forms.ModelForm):
    page = ''
    entity = ''
    
    def __init__(self, *args, **kwargs):
        super(ClinicalDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)
        if self.entity == '':
            self.entity = self.page
        if 'default_searching_option' in self.fields.keys():   
            self.fields['default_searching_option'].required = False
            self.fields['default_searching_option'].label = ''
               
            default = '0: All. Displays all data (no filtering)'
            
            if self.page in ('Immunizations', 'Pathology', 'Procedures', 'Problems'):
                default = '5 Years'
            elif (self.page in('Clinical Documents', 'Encounters', 'Imaging', 'Medications')):
                default = '1 Year'
            elif (self.page == 'Laboratory'):
                default = '9 Months'
            elif (self.page =='Diagnoses'):
                default = '6 Months'
            elif (self.page == 'Vitals'):
                default = '3 Years'
            elif self.page == 'Lab Results History':
                default = '2 Months'
            elif (self.page == 'PLV'):
                default = '1 Month'
            
            if (self.page != 'Allergies'):
                self.fields['default_searching_option'].choices = SEARCH_OPTIONS_CHOICES
            if self.page == 'Lab Results History' or self.page == 'PLV':
                help_text = "The textbox determines the time Range used to filter the patient's %(p)s list when using the Show option.<br/>The dropdown menu defines the time Unit used to filter the patient's %(p)s list. For example, if the Unit is \"month\" and the Range is 10, the patient's %(p)s over the past 10 months are displayed.<br><i>Default: %(d)s.</i>"
            else:
                help_text = "The textbox determines the time Range used to filter the patient's %(p)s list when using the Show option.<br/>The dropdown menu defines the time Unit used to filter the patient's %(p)s list. For example, if the Unit is \"month\" and the Range is 10, the patient's %(p)s over the past 10 months are displayed.<br>This configuration affects the Clinical Viewer and EHR Agent.<br><i>Default: %(d)s.</i>"
            
            self.fields['default_searching_option'].help_text = help_text % {'p':self.page, 'd':default}
            
        if 'default_searching_time' in self.fields.keys():   
            self.fields['default_searching_time'].required = False
            self.fields['default_searching_time'].label = 'Time range filter'

    class Meta:
        model = EHRAgentCVCommonClinicalDomainsProperties
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super(ClinicalDomainTimeFilterAdminForm, self).clean()
                        
        if 'default_searching_time' in self.changed_data or 'default_searching_option' in self.changed_data:
            CheckTimeFields(self, cleaned_data, 'default_searching_time', 'default_searching_option')

        return cleaned_data
                          
class ClinicalDomainPropertiesAdminForm(forms.ModelForm):
    page = ''
    entity = ''

    def __init__(self, *args, **kwargs):
        super(ClinicalDomainPropertiesAdminForm, self).__init__(*args, **kwargs)
        if self.entity == '':
            self.entity = self.page
        if 'show_cancelled_display' in self.fields.keys():
            self.fields['show_cancelled_display'].help_text = "Determines whether the \"Show Cancelled\" checkbox is displayed in Clinical Viewer.<br>If False: Show Cancelled checkbox is not displayed, and cancelled items are not displayed in the Clinical Viewer.<br>If True: Show Cancelled checkbox is displayed. Its default behavior is based on the \"Show Cancelled is selected\" configuration.<br><i>Default: True</i>"

        if 'show_cancelled_selected' in self.fields.keys():
            if (self.page == 'Allergies') | (self.page == 'Clinical Documents'):
                self.fields['show_cancelled_selected'].help_text = "Determines whether the Show Cancelled checkbox (if displayed) is selected.<br><i>Default: True</i>"
            else:
                self.fields['show_cancelled_selected'].help_text = "Determines whether the Show Cancelled checkbox (if displayed) is selected.<br><i>Default: False</i>"   

        if 'grouped_by_display' in self.fields.keys():
            self.fields['grouped_by_display'].help_text = "Determines whether to enable grouping of the " + self.page + " list.  If True, the Grouping option is displayed. If False, no Grouping option is displayed.<br><i>Default: True</i>"

        if 'grouped_by_selected' in self.fields.keys():
            self.fields['grouped_by_selected'].help_text = "Determines whether, by default, " + self.page + " are grouped.<br><i>Default: True</i>"
            self.fields['grouped_by_selected'].label = self.page + " are grouped by default"

        if 'code_system_name_display' in self.fields.keys():
            self.fields['code_system_name_display'].help_text = "Determines how to display the CodeSystem name.<br><i>Default: %s</i>" % vpo.CODE_SYSTEM_NAME_DISPLAY_CHOICES[0][1]
            self.fields['code_system_name_display'].required = False

        if 'display_grid' in self.fields.keys():
            self.fields['display_grid'].help_text = "Determines whether the Locations History grid is displayed.<br><i>Default: True</i>"
        
        if 'show_record_count' in self.fields.keys():
            self.fields['show_record_count'].help_text = "Determines whether the domain grid title bars display messages in the Summary clinical view.<br><i>Default: True</i>"
        
        if 'Imaging_DisplayImagingMetaData' in self.fields.keys():
            self.fields['Imaging_DisplayImagingMetaData'].help_text = "Determines whether the Imaging Details are displayed when printing an Imaging Report.<br><i>Default: True</i>"
        if 'Imaging_ShowEmptyFolders' in self.fields.keys():
            self.fields['Imaging_ShowEmptyFolders'].help_text = "Determines whether to show Imaging folder even if it is empty.<br>If True, displays empty folder.<br>If False, does not display empty folder.<br><i>Default: True</i>"

        if 'Documents_CompletionStatusAdded' in self.fields.keys():
            self.fields['Documents_CompletionStatusAdded'].help_text = "Determines whether in the Clinical Documents clinical view the presentation of the Document Completion Status is added to both the Preview and the Report (with title Report Status).<br/>Note: This configuration applies only to a document opened in the Clinical Document clinical view, but not to the same document opened in an Imaging clinical view.<br/><i>Default: False</i>"           
        if 'ClinicalDocument_DocPreviewFontFamily' in self.fields.keys():
            self.fields['ClinicalDocument_DocPreviewFontFamily'].required = False;
            
    class Meta:
        model = ClinicalDomainProperties
        fields = '__all__'      

class AllergiesDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Allergies'
    entity = 'Clinical Allergy'

    def __init__(self, *args, **kwargs):
        super(AllergiesDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class AllergiesDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Allergies'
    entity = 'Clinical Allergy'

    def __init__(self, *args, **kwargs):
        super(AllergiesDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)


class ImmunizationsDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Immunizations'
    entity = 'Clinical Immunizations'

    def __init__(self, *args, **kwargs):
        super(ImmunizationsDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class ImmunizationsDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Immunizations'
    entity = 'Clinical Immunizations'

    def __init__(self, *args, **kwargs):
        super(ImmunizationsDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)


class VitalsDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Vitals'

    def __init__(self, *args, **kwargs):
        super(VitalsDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class VitalsDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Vitals'

    def __init__(self, *args, **kwargs):
        super(VitalsDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)


class ProblemsDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Problems'
    entity = 'Clinical Problems'

    def __init__(self, *args, **kwargs):
        super(ProblemsDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class ProblemsDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Problems'
    entity = 'Clinical Problems'

    def __init__(self, *args, **kwargs):
        super(ProblemsDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)

class DiagnosesDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Diagnoses'
    entity = 'Clinical Diagnoses' 

    def __init__(self, *args, **kwargs):
        super(DiagnosesDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class DiagnosesDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Diagnoses'
    entity = 'Clinical Diagnoses' 

    def __init__(self, *args, **kwargs):
        super(DiagnosesDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)

class PathologiesDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Pathology'
    entity = 'Clinical Pathology'

    def __init__(self, *args, **kwargs):
        super(PathologiesDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class PathologiesDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Pathology'
    entity = 'Clinical Pathology'

    def __init__(self, *args, **kwargs):
        super(PathologiesDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)
        
class EncountersDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Encounters'

    def __init__(self, *args, **kwargs):
        super(EncountersDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class EncountersDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Encounters'

    def __init__(self, *args, **kwargs):
        super(EncountersDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)
        
class EncounterDetailsDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Encounter Details'

    def __init__(self, *args, **kwargs):
        super(EncounterDetailsDomainPropertiesAdminForm, self).__init__(*args, **kwargs)
        
class SummaryDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Summary'
    entity = 'Clinical'
        
    def __init__(self, *args, **kwargs):
        super(SummaryDomainPropertiesAdminForm, self).__init__(*args, **kwargs) 
        
        self.fields['ConditionTypeToDisplay'].required = False           

class MedicationsDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Medications'
    entity = 'Clinical Medication'

    def __init__(self, *args, **kwargs):
        super(MedicationsDomainPropertiesAdminForm, self).__init__(*args, **kwargs)
        self.fields['display_not_inactive'].help_text = "Determines whether by default the Medications view filters out all inactive medications when the user first launches the Medications clinical view.<br/>If True, the view only displays medications whose status is active.<br/>If False, the view displays all medications.<br><i>Default: False</i>"

class MedicationsDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Medications'
    entity = 'Clinical Medication'

    def __init__(self, *args, **kwargs):
        super(MedicationsDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)

class PlvDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'PLV'

    def __init__(self, *args, **kwargs):
        super(PlvDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class PlvDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'PLV'

    def __init__(self, *args, **kwargs):
        super(PlvDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)
        
class ProceduresDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Procedures'
    entity = 'Clinical Procedures'

    def __init__(self, *args, **kwargs):
        super(ProceduresDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class ProceduresDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Procedures'
    entity = 'Clinical Procedures'

    def __init__(self, *args, **kwargs):
        super(ProceduresDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)

class ImagingDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Imaging'
    entity = 'Imaging Type'

    def __init__(self, *args, **kwargs):
        super(ImagingDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class ImagingDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Imaging'
    entity = 'Imaging Type'

    def __init__(self, *args, **kwargs):
        super(ImagingDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)

class ImportFileAdminForm(forms.Form):
    file        = forms.FileField()

    def clean(self):
        import os
        cleaned_data = super(ImportFileAdminForm, self).clean()

        file = cleaned_data.get("file")
        if file:
            fileName, fileExtension = os.path.splitext(file.name)

            if fileExtension != ".json":
                raise forms.ValidationError("File must be a valid export file (extension: .json)")

        # Always return the full collection of cleaned data.
        return cleaned_data

    
class LabResultsHistoryDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page ='Lab Results History'

    def __init__(self, *args, **kwargs):
        super(LabResultsHistoryDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class LabResultsHistoryDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page ='Lab Results History'

    def __init__(self, *args, **kwargs):
        super(LabResultsHistoryDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)

class DocumentsDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Clinical Documents'
    entity = 'Clinical Documents'

    def __init__(self, *args, **kwargs):
        super(DocumentsDomainPropertiesAdminForm, self).__init__(*args, **kwargs)

class DocumentsDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page = 'Clinical Documents'
    entity = 'Clinical Documents'

    def __init__(self, *args, **kwargs):
        super(DocumentsDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)

class LaboratoryDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page ='Laboratory'

    def __init__(self, *args, **kwargs):
        super(LaboratoryDomainPropertiesAdminForm, self).__init__(*args, **kwargs)        

class LaboratoryDomainTimeFilterAdminForm(ClinicalDomainTimeFilterAdminForm):
    page ='Laboratory'

    def __init__(self, *args, **kwargs):
        super(LaboratoryDomainTimeFilterAdminForm, self).__init__(*args, **kwargs)        
        
class LabChartDisplayOptionsForm(forms.ModelForm):
    
    
    class Meta:
        model = LabChartDisplayOptions
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(LabChartDisplayOptionsForm, self).__init__(*args, **kwargs)
        self.fields['chart_format'].required = False
        self.fields['range_values'].required = False
        self.fields['abnormal_values'].required = False
        self.fields['date_format'].required = False
        
class LabResultsDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page ='Lab Results'
    entity = 'Test field, in the Lab Results'

    def __init__(self, *args, **kwargs):
        super(LabResultsDomainPropertiesAdminForm, self).__init__(*args, **kwargs)        

class DemographyDisplayOptionsInlineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(DemographyDisplayOptionsInlineForm, self).__init__(*args, **kwargs)
        
        self.fields['demography_details_type'].required = False
          
############################################################

from PIL import Image
from django.forms.utils import ErrorList

def CheckImage(image, frm, fld):
    if image:
        img = Image.open(image)
        image.seek(0)
        w, h = img.size
        if w > LOGO_MAX_WIDTH or h > LOGO_MAX_HEIGHT:
            frm._errors[fld] = ErrorList([u'Image size should not exceed %sx%s px (%s size is %sx%s px)' 
                                          % (LOGO_MAX_WIDTH, LOGO_MAX_HEIGHT, image.name, w, h)])

def CheckImageSize(image, frm, fld):
	if image:
		image.seek(0)
		megabyte_limit = 2097152 # 2 MB
		if image.size > megabyte_limit:
			frm._errors[fld] = ErrorList([u' Sorry, but the uploaded image file size is too large. Please upload a smaller image according to the recommended size'])

class AppsReportingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppsReportingForm, self).__init__(*args, **kwargs)
        self.fields['header_footer_font_type'].required = False
        self.fields['date_time_format'].required = False
    
    class Meta:
        model = AppsReporting
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super(AppsReportingForm, self).clean()
        if 'dbmotion_logo' in self.changed_data:
            CheckImage(cleaned_data.get('dbmotion_logo', False), self, 'dbmotion_logo')
                
        if 'customer_logo' in self.changed_data:
            CheckImage(cleaned_data.get('customer_logo', False), self, 'customer_logo')
       
        return cleaned_data

class PatientViewPageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientViewPageForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = PatientViewPage
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super(PatientViewPageForm, self).clean()

        if 'background_image' in self.changed_data:
            CheckImageSize(cleaned_data.get('background_image', False), self, 'background_image')

        return cleaned_data       

HELP_TEXT_TEMPLATE = '{0}<br/><i>Default: {1}</i>'
TIME_FILTER_TEXT = 'The Textbox determines the time Range for which to display {0}.<br/>The Dropdown menu defines the time Unit for which to display {0}. For example, if the Unit is "Month" and the Range is 10, the patients\' {0} over the past 10 months are displayed. Unit "All" displays all data (no filtering).<br><i>Notice: The final behavior is determined by the specific security role History Depth Configuration</i>'
    

class VpoInlineAdminForm(forms.ModelForm):
    entity = ''
    page = 'not_set'
    def __init__(self, *args, **kwargs):
        super(VpoInlineAdminForm, self).__init__(*args, **kwargs)
        
        if 'lab_susceptibility_methods_code_type' in self.fields.keys():
            self.fields['lab_susceptibility_methods_code_type'].required = False
        
        
        if 'filter_mood_codes' in self.fields.keys():
            if self.page == 'Medications':
                help_text = 'Defines the Mood code used to filter out (not display) Medications from the Medications clinical view, Medications Grid in the Summary Page and Medications Grid in the Diabetes clinical view ' + CODE_SYSTEM_FORMAT_TEMPLATE + '.'
                self.fields['filter_mood_codes'].label = 'Mood Codes to filter out'
            elif self.page == 'Immunizations':
                help_text = 'Defines the Mood code used to filter in (display) the Immunizations list ' + CODE_SYSTEM_FORMAT_TEMPLATE + ' so that only the Immunizations that were actually performed are displayed.'
                self.fields['filter_mood_codes'].label = 'Mood Codes to filter in'
            else:
                help_text = ''
                default_mood_code = ''
            
            self.fields['filter_mood_codes'].help_text = '%s<br/><i>Default: %s</i>' % (help_text, self.default_mood_code)
        
         
        if 'filter_cancelled_items' in self.fields.keys():
            if self.page == 'Problems':
                self.fields['filter_cancelled_items'].help_text = 'Determines whether the business functionality filters the cancelled items before they arrive to the Front End.<br/>If True, cancelled items are not retrieved.<br/>If False, cancelled items are retrieved.<br/>This configuration applies only in the case that "Show Cancelled is displayed" (above) is unchecked.<br/><i>Default: False</i>'
            else:
                self.fields['filter_cancelled_items'].help_text = 'Determines whether the business functionality filters the cancelled items before they arrive to the Front End.<br/>If True, cancelled items are not retrieved.<br/>If False, cancelled items are retrieved.<br/><i>Default: False</i>'

        if 'filter_status_code' in self.fields.keys():
            self.fields['filter_status_code'].label = self.fields['filter_status_code'].label % self.page
            if self.page == 'Summary':
                defValue = '2.16.840.1.113883.5.14|cancelled^2.16.840.1.113883.6.96|inactive^2.16.840.1.113883.6.96|resolved^2.16.840.1.113883.6.96|73425007^2.16.840.1.113883.6.96|185981001^2.16.840.1.113883.5.1068|pending^2.16.840.1.113883.5.14|held'
            elif self.page == 'Immunizations':
                defValue = '2.16.840.1.113883.5.14|cancelled^2.16.840.1.113883.6.96|185981001'
            elif self.page == 'Problems':
                defValue = '2.16.840.1.113883.5.14|cancelled^2.16.840.1.113883.6.96|185981001^2.16.840.1.113883.5.1068|pending'
            elif self.page == 'Diagnoses':
                defValue = '2.16.840.1.113883.5.14|cancelled^2.16.840.1.113883.6.96|185981001'   
            else:
                defValue = '2.16.840.1.113883.5.14|cancelled'
            self.fields['filter_status_code'].help_text = self.fields['filter_status_code'].help_text % (self.page, defValue)
          
        if self.page == 'Summary':
            for key in list(key for key in self.fields.keys() if key.startswith('summary_top_') or key.startswith('summary_time_filter_')):
                self.fields[key].required = False 
                
            time_amount_verbose_name = 'Time period to display %s'
            self.fields['summary_time_filter_amount_labs'].label = time_amount_verbose_name % 'Lab Events'
            self.fields['summary_time_filter_unit_labs'].help_text = HELP_TEXT_TEMPLATE.format(TIME_FILTER_TEXT.format('Lab Events'), '1 Month')
            self.fields['summary_time_filter_amount_encounter'].label = time_amount_verbose_name % 'Encounters'
            self.fields['summary_time_filter_unit_encounter'].help_text = HELP_TEXT_TEMPLATE.format(TIME_FILTER_TEXT.format('Encounters'), 'All')
            self.fields['summary_time_filter_amount_meds'].label = time_amount_verbose_name % 'Medications'
            self.fields['summary_time_filter_unit_meds'].help_text = HELP_TEXT_TEMPLATE.format(TIME_FILTER_TEXT.format('Medications'), 'All')
        
        if self.page == 'Vitals':
            codes_format = '&lt;%scode system&gt;,&lt;code&gt;'
            codes_format = '%s|%s' % ('%s;%s' % (codes_format % 'first priority - ', codes_format % ''), '%s;%s' % (codes_format % 'second priority - ', codes_format % ''))
            verbose_name = 'UOM priority order to display concatenated %s'
            help_text = 'Defines the priority order to display concatenated %s measurements, when there are different types of UoM (Units of Measurement).<br/>If the value is empty, all measurement types are displayed in a comma-separated list.<br/>If the priorities are defined, the system displays the first (concatenated) measurement type if it exists. If it does not exist, the second priority is displayed, and so on.<br/>If the concatenation configuration above is on, then the results will be concatenated.<br/>The list of priorities must be displayed in the following format. If not, the display of vital signs will fail.<br/>' + codes_format + '<br/><br/>Note: When ticking this checkbox, please fill out the relevant configuration of UOM priory, in order for it to take effect.<br/><i>Default: %s</i>'
            
            self.fields['unit_priority_list_body_weight'].label = verbose_name % 'Body Weight'
            self.fields['unit_priority_list_body_height'].label = verbose_name % 'Body Height'
            
            self.fields['unit_priority_list_body_weight'].help_text = help_text % ('Body Weight', '2.16.840.1.113883.6.8,kg;2.16.840.1.113883.6.8,g|2.16.840.1.113883.6.8,[lb_av];2.16.840.1.113883.6.8,[oz_av]')
            self.fields['unit_priority_list_body_height'].help_text = help_text % ('Body Height', '2.16.840.1.113883.6.8,[ft_us];2.16.840.1.113883.6.8,[in_us]|2.16.840.1.113883.6.8,m;2.16.840.1.113883.6.8,cm')
        if 'grouping_mode' in self.fields.keys():
            self.fields['grouping_mode'].required = False;
        
                    
    class Meta:
        model = Vpo
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super(VpoInlineAdminForm, self).clean()
        if 'summary_time_filter_amount_labs' in self.changed_data or 'summary_time_filter_unit_labs' in self.changed_data:
            CheckTimeFields(self, cleaned_data, 'summary_time_filter_amount_labs', 'summary_time_filter_unit_labs')
        if 'summary_time_filter_amount_encounter' in self.changed_data or 'summary_time_filter_unit_encounter' in self.changed_data:
            CheckTimeFields(self, cleaned_data, 'summary_time_filter_amount_encounter', 'summary_time_filter_unit_encounter')
        if 'summary_time_filter_amount_meds' in self.changed_data or 'summary_time_filter_unit_meds' in self.changed_data:
            CheckTimeFields(self, cleaned_data, 'summary_time_filter_amount_meds', 'summary_time_filter_unit_meds')
        
        if 'encounters_emergency_threshold' in self.changed_data: 
            if cleaned_data.get('encounters_emergency_threshold', None)==None:
                cleaned_data['encounters_emergency_threshold'] = 24
                
        if 'patient_privacy_minor_min' in self.changed_data or 'patient_privacy_minor_max' in self.changed_data:
            min_age = cleaned_data.get('patient_privacy_minor_min', None)
            max_age = cleaned_data.get('patient_privacy_minor_max', None)
            if min_age and max_age:
                if min_age >= max_age:
                    if 'patient_privacy_minor_min' in self.changed_data:
                        self._errors['patient_privacy_minor_min'] = ErrorList([u'Minor minimum age must be smaller than the maximum age'])
                    if 'patient_privacy_minor_max' in self.changed_data:
                        self._errors['patient_privacy_minor_max'] = ErrorList([u'Minor maximum age must be larger than the minimum age'])
            
        if 'lab_susceptibility_methods_code_type' in self.changed_data:    
            if self.page == "Reporting":
                vpo = Vpo.objects.get(clinical_domain = 19)
            else:
                vpo = Vpo.objects.get(reporting_cv = 1)
            vpo.lab_susceptibility_methods_code_type = cleaned_data['lab_susceptibility_methods_code_type']
            vpo.save()
            
        if 'facility_filter_enable' in self.changed_data or 'user_facility_root_oid' in self.changed_data:
            if cleaned_data.get('facility_filter_enable') and not cleaned_data.get('user_facility_root_oid'):
                self._errors['user_facility_root_oid'] = ErrorList([u'This field is required when \'%s\' is checked.' % self.fields['facility_filter_enable'].label])
                    
        return cleaned_data

class PvVpoInlineAdminForm(forms.ModelForm):
    entity = ''
    page = 'not_set'
    clinical_object = any
    def __init__(self, *args, **kwargs):
        super(PvVpoInlineAdminForm, self).__init__(*args, **kwargs)
        if self.instance.clinical_domain_id == 18:
            self.fields['grouping_mode'].label = 'Documents Grouping Priority Order'
        elif self.instance.clinical_domain_id == 17:
            self.fields['grouping_mode'].label = 'Imaging Grouping Priority Order'
        self.fields['grouping_mode'].required = False

class PvVpoBusinessRulesInlineAdminForm(forms.ModelForm):
    entity = ''
    page = 'not_set'
    clinical_object = any
    def __init__(self, *args, **kwargs):
        super(PvVpoBusinessRulesInlineAdminForm, self).__init__(*args, **kwargs)
        self.fields['encounters_remove_duplicated'].required = False
        self.fields['encounters_remove_duplicated'].label = 'Encounter Details: Remove duplicated Location records'

class PvDocumentsDomainPropertiesAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Clinical Documents'
    entity = 'Clinical Documents'

    def __init__(self, *args, **kwargs):
        super(PvDocumentsDomainPropertiesAdminForm, self).__init__(*args, **kwargs)
        self.fields['ClinicalDocument_ShowExternalDocumentsLabel'].label = 'Disclaimer Text'
        self.fields['ClinicalDocument_ShowExternalDocumentsLabel'].widget =  forms.TextInput(attrs={'size':'100'})
      
class PVOverrideDisclosureDirectiveAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Clinical Documents'
    entity = 'Clinical Documents'

    def __init__(self, *args, **kwargs):
        super(PVOverrideDisclosureDirectiveAdminForm, self).__init__(*args, **kwargs)
        self.fields['ClinicalDocument_DD_ResetPasskey'].required = False
        self.fields['ClinicalDocument_DD_ProviderPolicy_URL'].required = False
        self.fields['ClinicalDocument_DD_PatientPolicy_URL'].required = False
        self.fields['ClinicalDocument_DD_OverrdieWithoutConsentOrgPolicy_URL'].required = False

    class Meta:
        widgets = {
            'ClinicalDocument_DD_ResetPasskey': forms.TextInput(attrs={'size':'100'}),
            'ClinicalDocument_DD_ProviderPolicy_URL': forms.TextInput(attrs={'size':'100'}),
            'ClinicalDocument_DD_PatientPolicy_URL': forms.TextInput(attrs={'size':'100'}),
            'ClinicalDocument_DD_OverrdieWithoutConsentOrgPolicy_URL': forms.TextInput(attrs={'size':'100'}),
        } 

class VpoAllergiesInlineAdminForm(VpoInlineAdminForm):
    entity = 'Clinical Allergy'

class VpoProblemsInlineAdminForm(VpoInlineAdminForm):
    page = 'Problems'
    entity = 'Clinical Problems'

class VpoDiagnosisInlineAdminForm(VpoInlineAdminForm):
    page = 'Diagnoses'
    entity = 'Clinical Diagnoses'

class VpoProceduresInlineAdminForm(VpoInlineAdminForm):
    page = 'Procedures'
    entity = 'Clinical Procedures'

class VpoImmunizationsInlineAdminForm(VpoInlineAdminForm):
    page = 'Immunizations'
    default_mood_code = '2.16.840.1.113883.5.1001|EVN'
    
class VpoMedicationsInlineAdminForm(VpoInlineAdminForm):
    page = 'Medications'
    default_mood_code = '2.16.840.1.113883.3.57.1.2.17.82|ADMSTRD^'

class VpoImagingInlineAdminForm(VpoInlineAdminForm):
    page = 'Imaging'
    entity = 'Clinical Imaging'

class VpoSummaryInlineAdminForm(VpoInlineAdminForm):
    page = 'Summary'

class VpoVitalsInlineAdminForm(VpoInlineAdminForm):
    page = 'Vitals'
    
class VpoPatientDisplayInlineAdminForm(VpoInlineAdminForm):
    page = 'Patient Display'
    
class VpoReportingInlineAdminForm(VpoInlineAdminForm):
    page = 'Reporting'
    

######### VPO Common #########

class VpoCommonInlineAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(VpoCommonInlineAdminForm, self).__init__(*args, **kwargs)
        
        if 'clinical_data_display_options' in self.fields.keys():
            self.fields['clinical_data_display_options'].required = False
        
        if 'code_system_name_display' in self.fields.keys():
            self.fields['code_system_name_display'].required = False
        
        
    class Meta:
        model = VpoCommon
        fields = '__all__'
        
class VpoPPOLInlineAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(VpoPPOLInlineAdminForm, self).__init__(*args, **kwargs)
        
        if 'patient_privacy_mask_ssn' in self.fields.keys():
            self.fields['patient_privacy_mask_ssn'].required = False
            
########################## Message model ###############################################

class MinimumOneFormSet(BaseInlineFormSet):
    
    def clean(self):
        super(MinimumOneFormSet, self).clean()
        initial_num = len(filter(lambda f: not self._should_delete_form(f), self.initial_forms))
        extra_num = len(filter(lambda f: f.has_changed() and not self._should_delete_form(f), self.extra_forms))
        if initial_num + extra_num < 1:
            raise forms.ValidationError("Please provide at least one item")


class EmergencyDeclarationReasonsFormSet(MinimumOneFormSet):
    
    def __init__(self, *args, **kwargs):
        super(EmergencyDeclarationReasonsFormSet, self).__init__(*args, **kwargs)
        self.form.base_fields.get('message').label = "Emergency Declaration Reason"
        self.form.base_fields.get('message').help_text = "The option presented in the dropdown menu."
        self.form.base_fields.get('culture').help_text = "The culture the option belongs to. The user will see only the list related to his culture."
 

class PatientSearchTooltipFormSet(MinimumOneFormSet):
    
    def __init__(self, *args, **kwargs):
        super(PatientSearchTooltipFormSet, self).__init__(*args, **kwargs)
        self.form.base_fields.get('message').label = "Search Tip"
        self.form.base_fields.get('message').help_text = "The message text presented to the user."
        self.form.base_fields.get('culture').help_text = "The culture for which the tip will be presented."
    

class DisclaimerTextFormSet(MinimumOneFormSet):
    
    def __init__(self, *args, **kwargs):
        super(DisclaimerTextFormSet, self).__init__(*args, **kwargs)
        self.form.base_fields.get('message').label = "Disclaimer Text"
        self.form.base_fields.get('message_link_text').label = "Link Text"
        
        self.form.base_fields.get('message').help_text = "Defines the text in the message section of the disclaimer displayed in the clinical view status bar."
        self.form.base_fields.get('message_link_text').help_text = "Defines the text in the link section of the disclaimer displayed in the clinical view status bar."
        self.form.base_fields.get('culture').help_text = "The culture for which the text will be presented."   



class WebCultureInlineForm(forms.ModelForm):
    class Meta:
        model = WebCulture
        fields = '__all__'
        
        culture_size = '12'
        pattern_size = '26'
        char_size = '5'

        widgets = {
            'culture': forms.TextInput(attrs={'size':culture_size}),
            'short_date_pattern': forms.TextInput(attrs={'size':pattern_size}),
            'short_time_pattern': forms.TextInput(attrs={'size':pattern_size}),
            'long_time_pattern': forms.TextInput(attrs={'size':pattern_size}),
            'date_separator': forms.TextInput(attrs={'size':char_size}),
            'time_separator': forms.TextInput(attrs={'size':char_size}),
        }
        
class ExternalApplicationParameterInlineForm(forms.ModelForm):
         
    def clean(self):
        cleaned_data = super(ExternalApplicationParameterInlineForm, self).clean()
         
        if self.changed_data:
            # According to 'is_static' value, the 'static_value' or 'dbm_param' must be provided 
            if cleaned_data.get('is_static'):
                if not cleaned_data.get('static_value', None):
                    self._errors['static_value'] = ErrorList([u"This field is required."])
            else:
                print(cleaned_data.get('dbm_param', None))
                if not cleaned_data.get('dbm_param', None):
                    self._errors['dbm_param'] = ErrorList([u"This field is required."])
 
        return cleaned_data
    
    class Meta:
        model = ExternalApplicationParameter
        fields = '__all__'
        
class ExternalApplicationAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ExternalApplicationAdminForm, self).__init__(*args, **kwargs)
        
        self.fields['method'].required = False
        
class ImagingPacsForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ImagingPacsForm, self).__init__(*args, **kwargs)
        
        self.fields['method'].required = False
        
    
class DirectMessagingAcdmInlineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(DirectMessagingAcdmInlineForm, self).__init__(*args, **kwargs)
        
        #self.fields['gatewayUrl'].required = False
         
    def clean(self):
        cleaned_data = super(DirectMessagingAcdmInlineForm, self).clean()
    
    class Meta:
        model = DirectMessagingAcdm
        fields = '__all__'
#
class PatientSearchDisplayOptionsInlineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PatientSearchDisplayOptionsInlineForm, self).__init__(*args, **kwargs)
        
        self.fields['cluster_selection_behavior'].required = False


class PatientSearchDefaultSearchInlineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PatientSearchDefaultSearchInlineForm, self).__init__(*args, **kwargs)
        
        self.fields['default_search'].required = False


class OperationalManagerInlineForm(forms.ModelForm):
    
    class Meta:
        model = UsageReports
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(OperationalManagerInlineForm, self).__init__(*args, **kwargs)
                
        if 'instance' in kwargs.keys():
            ur = kwargs['instance']
            # This will reset the messages on screen
            if ur.status in (Status.applied, Status.error, Status.to_apply):
                ur.status = Status.none
                ur.save() 
        
class DataAccessAuditingForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(DataAccessAuditingForm, self).__init__(*args, **kwargs)
        
        self.fields['auditing_type'].required = False    
        self.fields['server_principals'].required = False    
   
    
class BaseModelAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BaseModelAdminForm, self).__init__(*args, **kwargs)
        
        if 'services' in self.fields:
            self.fields['services'].required = False
        if 'components' in self.fields:
            self.fields['components'].required = False


from dbmconfigapp.widgets import HorizontalSortable
CODE_DISPLAY_CHOICES = (
                        ('Preferred', 'Preferred'),
                        ('Baseline', 'Baseline'),
                        ('Local', 'Local'),
                        ('Text', 'Text'),                        
    )


class ClinicalCodeDisplayForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ClinicalCodeDisplayForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = ClinicalCodeDisplay
        fields = '__all__'
        
        widgets = {
            'display_as': HorizontalSortable(choices=CODE_DISPLAY_CHOICES),
            }
            
class AppsPatientDisplayVBPForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(AppsPatientDisplayVBPForm, self).__init__(*args, **kwargs)
        
        self.fields['vbp_oid_system'].required = False
        self.fields['vbp_display_name_long'].required = False

    def clean(self):
        cleaned_data = super(AppsPatientDisplayVBPForm, self).clean()
        return cleaned_data

    class Meta:
        model = AppsPatientDisplayVBP
        fields = '__all__'

        widgets = {
            'vbp_oid_system': forms.TextInput(attrs={'size':'120'}),
        }

class PvPatientNameDisplayForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PvPatientNameDisplayForm, self).__init__(*args, **kwargs)
        
        self.fields['pv_patient_name_display'].required = True

    def clean(self):
        cleaned_data = super(PvPatientNameDisplayForm, self).clean()
        return cleaned_data

    class Meta:
        model = PvPatientNameDisplay
        fields = '__all__'

        
class AppsPatientDisplayMetricCodeBasedIndicatorForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(AppsPatientDisplayMetricCodeBasedIndicatorForm, self).__init__(*args, **kwargs)
        
        self.fields['mci_oid_system'].required = True
        self.fields['mci_interpretation'].required = True
        self.fields['mci_label'].required = True
        self.fields['mci_priority'].required = True

    def clean(self):
        cleaned_data = super(AppsPatientDisplayMetricCodeBasedIndicatorForm, self).clean()
        return cleaned_data

    class Meta:
        model = AppsPatientDisplayMetricCodeBasedIndicator
        fields = '__all__'

        widgets = {
            'mci_oid_system':forms.TextInput(attrs={'size':'65'}),
        }
        

class CCDADisplayInlineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CCDADisplayInlineForm, self).__init__(*args, **kwargs)
        #self.fields['environment'].required = False
        #self.fields['display_mode'].required = False
        self.fields['source_system'].required = True
        self.fields['cve_renew_certificate'].required = True
        if 'display_mode' in self.fields.keys():
            self.fields['display_mode'].required = False
        if 'service_location' in self.fields.keys():
            self.fields['service_location'].required = False
        
    
    class Meta:
        fields = '__all__'

        widgets = {
            'cve_renew_certificate': forms.TextInput(attrs={'size':'100'}),
            'source_system': forms.TextInput(attrs={'size':'100'}),
            'retrieval_key_cloud_service':forms.TextInput(attrs={'size':'100'}),
            'Cve_document_conversion':forms.TextInput(attrs={'size':'100'}),
            'Pdf_document_conversion':forms.TextInput(attrs={'size':'100'}),
            'vaas_document_conversion':forms.TextInput(attrs={'size':'100'}),
            'transformation_cloud_service':forms.TextInput(attrs={'size':'100'}),
            'transformation_service_subscription':forms.TextInput(attrs={'size':'100'}),
            'customer_name':forms.TextInput(attrs={'size':'100'})
        }

class SearchResultGridFormSet(MinimumOneFormSet):
    
    def __init__(self, *args, **kwargs):
        super(SearchResultGridFormSet, self).__init__(*args, **kwargs)
        self.form.base_fields.get('label').label = "Label"
        self.form.base_fields.get('dbMotion_patient_attribute_name').label = "DbMotion Patient Attribute Name"
        self.form.base_fields.get('column_order').label = "Column Order"

class PvImagingPacsDisclaimerAdminForm(ClinicalDomainPropertiesAdminForm):
    page = 'Clinical Documents'
    entity = 'Clinical Documents'

    def __init__(self, *args, **kwargs):
        super(PvImagingPacsDisclaimerAdminForm, self).__init__(*args, **kwargs)
        self.fields['Pacs_Disclaimer_Text'].label = 'PACS Disclaimer Text'
        self.fields['Pacs_Disclaimer_Text'].widget =  forms.TextInput(attrs={'size':'100'})
        self.fields['Grouping_by_Modality'].widget =  forms.CheckboxInput()
        self.fields['Grouping_by_Modality'].label = 'Imaging Grouping by Modality'

class CarequalityIntegrationSettingsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(CarequalityIntegrationSettingsForm, self).clean()
        enable_carequality_integration  = cleaned_data.get('enable_carequality_integration')
        home_community_id  = cleaned_data.get('home_community_id')
        certificate_thumptrint  = cleaned_data.get('certificate_thumptrint')
        patient_discovery_endpoint  = cleaned_data.get('patient_discovery_endpoint')
        find_documents_endpoint  = cleaned_data.get('find_documents_endpoint')
        retrieve_document_endpoint  = cleaned_data.get('retrieve_document_endpoint')
        if(enable_carequality_integration is True):
            if (home_community_id is None or home_community_id == ''):   
                self._errors['home_community_id'] = ErrorList([u'Value should not be empty.'])
            if (certificate_thumptrint is None or certificate_thumptrint == ''):   
                self._errors['certificate_thumptrint'] = ErrorList([u'Value should not be empty.'])
            if (patient_discovery_endpoint is None or patient_discovery_endpoint == ''):   
                self._errors['patient_discovery_endpoint'] = ErrorList([u'Value should not be empty.'])
            if (find_documents_endpoint is None or find_documents_endpoint == ''):   
                self._errors['find_documents_endpoint'] = ErrorList([u'Value should not be empty.'])
            if (retrieve_document_endpoint is None or retrieve_document_endpoint == ''):   
                self._errors['retrieve_document_endpoint'] = ErrorList([u'Value should not be empty.'])
        return cleaned_data
    class Meta:
        model = CarequalityIntegrationSettingsModel
        fields = '__all__'


        widgets = {
            'home_community_id': forms.TextInput(attrs={'size':'100'}),
            'certificate_thumptrint': forms.TextInput(attrs={'size':'100'}),
            'patient_discovery_endpoint': forms.TextInput(attrs={'size':'100'}),
            'find_documents_endpoint': forms.TextInput(attrs={'size':'100'}),
            'retrieve_document_endpoint': forms.TextInput(attrs={'size':'100'})
        }
        

    

class PrefetchSettingsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(PrefetchSettingsForm, self).clean()
        enable_prefetch  = cleaned_data.get('enable_prefetch')
        api_url  = cleaned_data.get('api_url')
        api_subscription_key  = cleaned_data.get('api_subscription_key')
        if(enable_prefetch is True):
            if (api_url is None or api_url == ''):   
                self._errors['api_url'] = ErrorList([u'Value should not be empty.'])
            if (api_subscription_key is None or api_subscription_key == ''):   
                self._errors['api_subscription_key'] = ErrorList([u'Value should not be empty.'])
        return cleaned_data
    
    class Meta:
        model = PrefetchSettingsModel
        fields = '__all__'

        widgets = {
            'enable_prefetch': forms.CheckboxInput(),
            'api_url': forms.TextInput(attrs={'size':'100'}),
            'api_subscription_key': forms.PasswordInput(attrs={'size':'100'},render_value=True)            
        }
    
def getCareQualiryIndication(self,model_name, attrinute_name):
    cleaned_data = super(model_name, self).clean()
    return cleaned_data_parent.get(attrinute_name)
