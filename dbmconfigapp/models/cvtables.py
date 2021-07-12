from django.core import validators
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from dbmconfigapp.models import vpo
from dbmconfigapp.models.apps_reporting import FONT_TYPE_CHOICES
from .base import *
import sys
from django.template.defaultfilters import default

LAB_EVENTS_DEFAULT_GROUPING_CHOICES = (        
        (0, 'By order of events'),
        (1, 'By collection date'),
        (2, 'By the latest results'),
    )

LOCAL_CODE_DISPLAY_PRIORITIES = (
    ('Designation,DisplayName', 'Designation, DisplayName'),
    ('DisplayName,Designation', 'DisplayName, Designation'),
                                 )
DEMOGRAPHY_DETAILS_TYPE_CHOICES = (        
        (0, 'Leading record contacts'),
        (7, 'All contacts'),
    )

CONDITION_TYPE_TO_DISPLAY_CHOICES = (        
        (0, 'Display Diagnosis grid'),
        (1, 'Display Problems grid'),
        (2, 'Do not display either'),
    )

EXTERNAL_DOCUMENT_GROUPING_CHOICES = (        
        ('Type', 'By Type'),
        ('Author', 'By Author'),
        ('Date', 'By Date'),
        ('Facility', 'By Facility'),
    )


class DataElement(ConfigurationEntityBaseModel):
    clinical_domain         = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True)
    pl_parent               = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True)
    pv_parent_patient_display          = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, editable=False)
    name                    = models.CharField(max_length=60, blank=True, verbose_name='Elements (Vocabulary Domain Code)')
    enable                  = models.BooleanField(default=True, verbose_name='Enable', help_text = "Determines whether or not the column is displayed.")    
    page_width              = models.FloatField(null=True, verbose_name='Column Width', help_text = "Defines the column width, as a percentage of the screen's width. The sum of weight of all visible columns should be equal to 100% or higher.")
    default_width           = models.FloatField(verbose_name='Default Column Width', null=True)
    report_width            = models.FloatField(verbose_name='Report Column Width', null=True, help_text = "Defines the report column width, as a percentage of the screen's width. The sum of weight of all visible columns should be strongly equal to 100%.")
    default_report_width    = models.FloatField(verbose_name='Default Report Column Width', null=True)
    order                   = models.IntegerField(null=True, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)], help_text = "Determines the order of the column in the grid")
    clinical_view_name      = models.CharField(max_length=100, blank=True)
    report_field_name       = models.CharField(max_length=100, blank=True)
    grid_name               = models.CharField(max_length=100, blank=True)
    report_name             = models.CharField(max_length=100, blank=True)
    hide_uom                = models.BooleanField(default=False, verbose_name='Hide the UOM', help_text='Defines the Vital Signs measurement in which the UOM (Unit of Measurement) is hidden (not displayed), by default.\nDefault: BloodPressure, HeartRate\nThis configuration applies to Clinical Viewer and EHR Agent.')
    concatenate_values      = models.BooleanField(default=False, verbose_name='Concatenate Values', help_text='Defines which Vitals Measurements will be displayed as concatenated. For example: 65 kg 50 g or 65.5 kg\nDefault: BodyWeight, BodyHeight.\nThe Blood Pressure (BP) concatenation business rule is as follows:\nIf a BP Measurement event includes a combined BP Measurement value, display the combined value and do not display separate systolic and diastolic measurements.\nIf a BP Measurement event does not include a combined BP Measurement value and includes both systolic and diastolic measurements, display the concatenated value as systolic/diastolic.\nThis configuration applies to Clinical Viewer and EHR Agent.')
    _info                   = models.CharField(max_length=60, blank=True, null=True)
        
    def __unicode__(self):
        return self.name

    def clean(self):
        if self.name == "":
            raise ValidationError('Value cannot be empty')
        
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Grid Display Options'


class GridDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Grid Display Options'       


class FindingDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Related Findings grid"


class DocumentDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Related Documents grid'


class LocationHistoryDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Location History grid'
        
class ProviderRelationshipDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Provider Relationship grid'
        
class DiagnosesDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Diagnoses grid'
        
class AllergiesDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Allergies grid'
        
class MedicationsDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Medications grid'
        
class ProblemsDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Problems grid'

class DiagnosisDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Diagnosis grid'
        
class LabsDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Labs grid'
        
class DemographicsDetailsDEGrid(DataElement):
    '''
    This is the new class representing demographics, and REPLACES DemogrphicsDetailsGrid.
    '''
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Demographics Details Grid'

class InsuranceDataElement(DataElement):
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Insurance Grid'

# class PatientDetailsElements(DataElement):
#     class Meta:
#         app_label = "dbmconfigapp"
#         history_meta_label = 'PatientDetails'

        
class ClinicalDomainProperties(ConfigurationEntityBaseModel):    
    clinical_domain                         = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True)    
    pl_parent                               = models.ForeignKey('PlPatientDisplayPage', on_delete=models.SET_NULL, null=True)
    pv_parent_patient_display               = models.ForeignKey('PVPatientDisplayPage', on_delete=models.SET_NULL, null=True, editable=False)
    pv_ClinicalDocument_ShowExternalDocumentsLabel   = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, null=True, default=None, editable=False)
    ClinicalDocument_DD_ResetPasskey        = models.CharField(verbose_name='Reset Keyword',null=True, max_length=300, help_text = get_help_text("Defines the text displayed in the Patient View that explains how the patient can reset the Disclosure Directive password (maximum length of 300 Characters).<br>(For example: To reset keyword, the patient should call XXX-XXX-XXXX.)", 'empty'))    
    ClinicalDocument_DD_ProviderPolicy_URL  = models.CharField(verbose_name='Providers Policies Help Page', max_length=500, null=True, help_text=get_help_text("Defines the URL (or network drive) of the providers policies help page.", 'empty'))
    ClinicalDocument_DD_PatientPolicy_URL   = models.CharField(verbose_name='Patients Policies Help Page', max_length=500, null=True, help_text=get_help_text("Defines the URL (or network drive) of the patients policies help page.", 'empty'))
    ClinicalDocument_DD_OverrdieWithoutConsentOrgPolicy_URL = models.CharField(verbose_name='Override Without Consent Policy',max_length=500, null=True, help_text=get_help_text("Defines the URL (or network drive) of the Organization\'s Override Without Consent Policy Page.", 'empty'))
    help_1                                  = models.TextField(blank=True, null=True, verbose_name='help')
    help_2                                  = models.TextField(blank=True, null=True, verbose_name='help')
    show_cancelled_display                  = models.BooleanField(default=True, verbose_name='"Show Cancelled" is displayed')
    show_cancelled_selected                 = models.BooleanField(default=True, verbose_name='"Show Cancelled" is selected')
    help_3                                  = models.TextField(blank=True, null=True, verbose_name='help')
    grouped_by_display                      = models.BooleanField(default=True, verbose_name='"Grouped By" option is displayed')
    grouped_by_selected                     = models.BooleanField(default=True, verbose_name='"Grouped By" option is selected')
    code_system_name_display                = models.IntegerField(choices=vpo.CODE_SYSTEM_NAME_DISPLAY_CHOICES, default=0, verbose_name='CodeSystem name display within the Code column')
    display_not_inactive                    = models.BooleanField(default=False, verbose_name='Display only medications whose status is active')    
    display_grid                            = models.BooleanField(default=True, verbose_name='Display Location History Grid')
    show_record_count                       = models.BooleanField(default=True, verbose_name='The domain grid title bars display messages')
    Imaging_DisplayImagingMetaData          = models.BooleanField(default=False, verbose_name='The Imaging Details are displayed on the top of the imaging report')
    Imaging_ShowEmptyFolders                = models.BooleanField(default=False, verbose_name='Show Imaging folder even if it is empty')
    Documents_CompletionStatusAdded         = models.BooleanField(default=False, verbose_name='The presentation of the Document Completion Status is added to both the Preview and the Report (with title Report Status).')
    LabEvents_DefaultGrouping               = models.IntegerField(choices=LAB_EVENTS_DEFAULT_GROUPING_CHOICES, default=0, verbose_name='Default grouping of Lab events', help_text='Determines the default grouping of Lab events.<br><i>Default: By order of events</i>')
    ClinicalDocument_ShowEmptyFolders       = models.BooleanField(default=False, verbose_name='Show a Clinical Document folder even if it is empty', help_text='Determines whether to show a Clinical Document folder even if it is empty.<br/>If True, the empty folder is displayed.<br/>If False, the empty folder is not displayed.<br/><i>Default: False</i>')
    Laboratory_UseWrappedText               = models.BooleanField(default=True, verbose_name='Use wrapped text', help_text='Determines whether the full results and comments are displayed as wrapped.<br/>If True, the full result/comment is presented wrapped.<br/>If False, the results and comments are displayed in a single line with 3 dots.<br/><i>Default: True</i>')
    Laboratory_OpenMicroReportForMicroEvent = models.BooleanField(default=False, verbose_name='Open Microbiology Report   ', help_text='Determines whether to display the Microbiology lab report instead of the Lab Results Clinical View if the lab result is a microbiology lab (A microbiology lab is identified by the code 2.16.840.1.113883.6.1|MICRO). In that case, the report is available from all the places that the Lab Results clinical view is accessed for regular results (meaning, from Labs, from Labs in Summary Page, etc.) and by clicking on the report icon in the Labs clinical view.<br/><i>Default: False</i>')
    LabResults_FormatText                   = models.BooleanField(verbose_name='Change Lab Results/Remarks to be formatted text', default=False, help_text='Determines whether the Lab Results/Remarks font is changed to be formatted text (Courier New). If so, the text has the same alignment regardless of the letters that are used.<br/><em>Default: False</em>')
    demography_details_type                 = models.IntegerField(default=7, choices=DEMOGRAPHY_DETAILS_TYPE_CHOICES, help_text = get_help_text("Determines the mode that the patient's contact details are displayed in the Demographics clinical view.<br/>If the value is '%s', only the leading record contacts information is displayed. Additional information can be accessed only by clicking the More icon.<br/>If the value is '%s', the leading record contacts information is displayed and also all additional contacts are displayed." % (DEMOGRAPHY_DETAILS_TYPE_CHOICES[0][1], DEMOGRAPHY_DETAILS_TYPE_CHOICES[1][1]), DEMOGRAPHY_DETAILS_TYPE_CHOICES[1][1]))
    ClinicalDocument_ShowExternalDocumentsLabel = models.CharField(verbose_name='Show External Documents Checkbox Label', default='Show External Documents', max_length=50, blank=True, null=True, help_text = get_help_text("Determines the text to show for all External Documents on Disclaimer after the fixed text", "'Show External Documents' and Fixed text: 'You are about to access patient documents from external system(s) for the following reasons:'"))
    ClinicalDocument_BringExtDocsOnShowAll  = models.BooleanField(default=True, verbose_name='Retrieve External Documents on Show All', help_text=get_help_text('Determines whether external documents are retrieved and shown with other documents - when the user selects to Show All. <br/><b>True: </b>The External Documents checkbox will be selected automatically, so external documents will be retrieved and displayed with other documents. <br/><b>False: </b>The External Documents checkbox will not be selected automatically, so external documents will be not retrieved and displayed.', 'True'))
    ClinicalDocument_ShowExternalDocumentsLabelForAgent       = models.BooleanField(default=False, verbose_name='External Documents Display', help_text=get_help_text('Determines whether an External Document disclaimer will be displayed in EHR Agent when the user wants to access External Documents.<br><br><b>True:</b><br>In the EHR Agent a disclaimer message will be displayed before displaying the list of External Documents to the user. The user is expected to approve the disclaimer.  The disclaimer will concatenate a fixed text with a configurable text.<br>Fixed Disclaimer Text:\"You are about to access patient documents from external systems for the following reason(s):\"<br>Configured Disclaimer Text: This will be the same text configured for the label of the Show External Documents checkbox in the Clinical Viewer. (The label is configured in the Show External Documents Checkbox Label configuration.) The text will be the same for both applications.<br>This configured text will also be displayed above the list of External Documents in the EHR Agent.<br><br><b>False:</b><br>The EHR Agent will not display the disclaimer text and will not display the configured text above the External Documents list. However, this text, if configured for Clinical Viewer External Documents checkbox, will be displayed in the Clinical Viewer.', 'False'))
    ConditionTypeToDisplay                  = models.IntegerField(verbose_name='Displaying Diagnosis and Problems grid', default=1, choices=CONDITION_TYPE_TO_DISPLAY_CHOICES, help_text = "Determines whether the Diagnosis grid or Problems grid is displayed in the Summary clinical view.<br/><i>Default: Display Problems grid</i>")
    demography_display_insurances_grid      = models.BooleanField(default=True, verbose_name='Insurance grid is displayed', help_text='Determines whether the Insurance grid is visible in the Demographics clinical view.<br/><i>Default: True</i>')
    ClinicalDocument_DocPreviewFontFamily   = models.CharField(verbose_name='Clinical Document preview font type', choices=FONT_TYPE_CHOICES, default='Courier New', max_length=60, help_text="Defines the Font Type in the preview of Clinical Documents.<br/><i>Default: Courier New</i>")
    ClinicalDocument_SortTypeByDesignation  = models.BooleanField(default=True, verbose_name='Sort Clinical Documents by designation', help_text='Determines whether to sort documents by designation or by domain code.<br/><i>Default: True</i>')
    LabResultHistory_DisplaySearch          = models.BooleanField(default=False, verbose_name='Display Lab Search', help_text='Define whether to display the Lab search option in the Lab results history page.<br/><i>Default: False</i>')
    ClinicalDocument_DocsTreePaneWidth      = models.IntegerField(default=33, verbose_name='Documents Tree Pane Width',           null=False, validators=[validators.MinValueValidator(33), validators.MaxValueValidator(70)], help_text="Defines the width of the Documents pane (in percentage) in relation to the Preview pane. The value range is 33%-70%.<br/><i>Note: The horizontal width will be set after the user opens the Clinical Documents page. There is no need to click on External Documents.</i><br/><i>Default: 33%</i>")
    ClinicalDocument_ExtDocsTreePaneHeight  = models.IntegerField(default=35, verbose_name='External Documents Tree Pane Height', null=False, validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)], help_text="Defines the height of the External Documents area (in percentage) within the entire area of the Documents pane (including Internal and External Documents areas). The remainder of the Documents pane contains the internal Documents area (meaning, 100% minus this value). The value range is 0%-100%.<br/><i>Note: This configuration takes effect only after External Documents is selected.</i><br/><i>Default: 35%</i>")
    ExteranlDocument_Default_Grouping       = models.CharField(verbose_name='External Documents Default Grouping', max_length=60, null=True, choices=EXTERNAL_DOCUMENT_GROUPING_CHOICES, help_text=get_help_text("Defines the default grouping method for the External Documents domain in Clinical Viewer.<br>Note that this does not affect the \"Internal Documents\" grouping in this domain.", "By Date"))
    disclaimer                              = models.BooleanField(verbose_name='Disclaimer Required', default=False,  help_text = "Determines whether a disclaimer will be displayed in Patient view when the user wants to access any External Documents category.<br/><b>True: </b><br/>In the external documents category a disclaimer message will be displayed before displaying the list of External Documents to the user. The user is expected to approve the disclaimer. The disclaimer will concatenate a fixed text with a configurable text.<br/><b>False:</b><br/>The application will not display the disclaimer in any external documents category.<br/>Default: False.")



    def get_help_search_time(self):
        return format_html('<span>{0}</span>', self.help_1)
    def get_help_display_grid(self):
        return format_html('<span>{0}</span>', self.help_1)
    def get_help_show_record_count(self):
        return format_html('<span>{0}</span>', self.help_1)
    def get_help_Imaging_DisplayImagingMetaData(self):
        return format_html('<span>{0}</span>', self.help_1)
    def get_help_Imaging_ShowEmptyFolders(self):
        return format_html('<span>{0}</span>', self.help_2)
    def get_help_show_cancelled(self):
        return format_html('<span>{0}</span>', self.help_2)
    def get_help_grouped_by(self):
        return format_html('<span>{0}</span>', self.help_3)



    get_help_search_time.allow_tags = True
    get_help_show_cancelled.allow_tags = True
    get_help_grouped_by.allow_tags = True
    get_help_display_grid.allow_tags = True
    get_help_show_record_count.allow_tags = True
    get_help_Imaging_DisplayImagingMetaData.allow_tags = True
    get_help_Imaging_ShowEmptyFolders.allow_tags = True
    
    
    def __unicode__(self):
        return ""
    
    def clean(self):
        if not self.show_cancelled_display and self.show_cancelled_selected:
            raise ValidationError('"Show Cancelled" is not displayed but is selected')
        if not self.grouped_by_display and self.grouped_by_selected:
            raise ValidationError('"Grouped By" is not displayed but is selected')

    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = 'Display Options'


class ClinicalDomain(PageBaseModel):
    help_text_1         = models.TextField(blank=True, default='This is a help text section No. 1')
    help_text_2         = models.TextField(blank=True, default='This is a help text section No. 2')
    help_text_3         = models.TextField(blank=True, default='This is a help text section No. 3')
    clinical_view_name  = models.CharField(max_length=100, blank=True)
    report_name         = models.CharField(max_length=100, blank=True)
    
    def __unicode__(self):
        return self.page_name
    
    def page_title(self):
        return 'Set the Clinical Viewer %s Front End Settings' % self.page_name
    
    class Meta:
        app_label = "dbmconfigapp"

############################################################################################


class ImagingPacs(ConfigurationEntityBaseModel):
    clinical_domain         = models.ForeignKey('ClinicalDomain', on_delete=models.SET_NULL, null=True, editable=False, default=17)
    pv_clinical_domain_page   = models.ForeignKey('PVClinicalDomainPage', on_delete=models.SET_NULL, default=1, null=True, editable=False)
    device_id               = models.CharField(max_length=40, verbose_name='deviceId', blank=True, null=True, help_text='The Imaging study deviceId based on the Federation Node Id.<br/>For Any value define ALL.')
    use_code                = models.CharField(max_length=40, verbose_name='useCode', blank=True, null=True, help_text='The Imaging study useCode based on the UMS ImageValue.use.<br/>For Any value define ALL.')
    schema_code             = models.CharField(max_length=40, verbose_name='schemeCode', blank=True, null=True, help_text='The Imaging study SchemeCode based on the UMS ImageValue.Scheme.<br/>For Any value define ALL.')
    facility                = models.CharField(max_length=200, verbose_name='facility', blank=True, null=True, default='ALL', help_text='In some organizations the PACS URL depends on the user location. In order to configure the correct URL, according to the user location, the User Facility Identification should  be enabled and configured.<br/>If configured, the system will use the PACS URL with the facility that matches the user facility (it detects the facility mapped to the EHR instance intercepted by the Agent Hub).<br/>User Facility Identification should be configured in the following location: CCenter > Agent Hub -> EHR Integration -> EHR Instances -> User Facility Identification.<br/>Format: ID Root|ID Extension.<br/>For Any value define ALL.')
    uri                     = models.CharField(max_length=200, verbose_name='URI', help_text='The URI for the PACS.')
    method                  = models.CharField(max_length=4, default='GET', choices=(('GET', 'GET'), ('POST', 'POST')), help_text=get_help_text('For a Web Application, use one of the following:<br/><b>POST:</b> All the specified parameters are passed as hidden values.<br/><b>GET:</b> All the specified parameters are passed as a connection string, in the order they appear in the configuration.', 'GET'))

    def name_url(self):
        if self.id:
            return '<a href="%s" onclick="return showEditPopup(this);" title="Click to edit">%s</a>' % ("/admin/dbmconfigapp/imagingpacs/%s/" % self.id, self.uri)
        else:
            return '<a href="%s" onclick="return showEditPopup(this);" >Add new Application</a>' % "/admin/dbmconfigapp/imagingpacs/add/"
    
    name_url.allow_tags = True
    name_url.short_description = 'URI'
    
    def parameters(self):
        return '; '.join('{}: {}'.format(p.name, p.parameter_value) for p in ImagingPacsParameter.objects.filter(imaging_pacs = self))
    
    parameters.allow_tags = True
    
    def __unicode__(self):
        return self.uri
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Imaging PACS"
        verbose_name = "Imaging PACS"
        verbose_name_plural = "Imaging PACS"
        


class ImagingPacsParameter(ConfigurationEntityBaseModel):
    imaging_pacs            = models.ForeignKey(ImagingPacs, on_delete=models.CASCADE, null=False)
    name                    = models.CharField(max_length=40, verbose_name='parameter name', help_text='The name of the parameter that should be sent in the request. In projects where the Agent Hub user retrieves images from PACS systems that require validation of the request with a SAML token, enter a new PACS Parameter with the following name: SAMLResponse. For the Parameter Value, enter the certificate thumbprint. In projects where the Agent Hub user retrieves images from PACS systems that use IE different than IE 11, enter a new PACS Parameter with the following name: "X-UA-Compatible". For the Parameter Value, enter the X-UA-Compatible string for example "IE=7" for IE 7 emulation.')
    is_static               = models.BooleanField(default=True, help_text=get_help_text('If True (static), the value is taken as is.<br/>If False (dynamic), the value is taken from the Image Value Reference field.', 'True', '\n'))
    parameter_value         = models.CharField(max_length=500, help_text='In cases where the URI requires URL or HTML encoding (GET)/HTML(POST), add either the <b>UrlEncode_ or HtmlEncode_</b> prefix to non-static parameter values, as follows:\n- UrlEncode: Used for the GET method or if the parameter is part of the URL.\n- HtmlEncode: Used for the POST method.')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name_plural = "Imaging PACS Parameters"
        unique_together = ("name", "imaging_pacs")
    
############################################################################################

class ClinicalDomainPlv(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"

class ClinicalDomainAllergies(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"


class ClinicalDomainProblems(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"


class ClinicalDomainImmunizations(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"


class ClinicalDomainVitals(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"


class ClinicalDomainMedications(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"


class ClinicalDomainPathologies(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"


class ClinicalDomainDiagnoses(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"

class ClinicalDomainEncounters(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"
        
class ClinicalDomainEncounterDetails(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"

class ClinicalDomainSummary(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"
        
class ClinicalDomainProcedures(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"

class ClinicalDomainLabResultsHistory(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"

class ClinicalDomainImaging(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"

class ClinicalDomainLaboratory(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"

class ClinicalDomainDocuments(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"
        
class ClinicalDomainLabResults(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"

class ClinicalDomainDemographics(ClinicalDomain):
    class Meta:
        app_label = "dbmconfigapp"


