import sys
from dbmconfigapp.models.base import *
from django.core import validators
from .database_storage import DatabaseStorage
from configcenter import settings
#from dbmconfigapp.models.cvtables import LOCAL_CODE_DISPLAY_PRIORITIES
from dbmconfigapp.models.vpo import Vpo

#########
# Logos maximum size vars are used for dbMotion_logo and customer_logo for:
# - help_text
# - validation (forms.py)
# - error messages
LOGO_MAX_WIDTH = 220
LOGO_MAX_HEIGHT = 60
#########

FONT_TYPE_CHOICES = (
    ('Arial', 'Arial'),
    ('Courier New', 'Courier New')
    )

DATE_TIME_FORMAT_CHOICES = (
    ('d', 'Short date: 4/17/2006'),
    ('D', 'Long date: Monday, April 17, 2006'),
    ('t', 'Short time: 2:22 PM'),
    ('T', 'Long time: 2:22:48 PM'),
    ('f', 'Full date/short time: Monday, April 17, 2006 2:22 PM'),
    ('F', 'Full date/long time: Monday, April 17, 2006 2:22:48 PM'),
    ('g', 'General date/short time: 4/17/2006 2:22 PM'),
    ('G', 'General date/long time (default): 4/17/2006 2:22:48 PM'),
    ('M', 'Month: April 17'),
    ('R', 'RFC1123: Mon, 17 Apr 2006 21:22:48 GMT'),
    ('s', 'Sortable: 2006-04-17T14:22:48'),
    ('u', 'Universal sortable (invariant): 2006-04-17 21:22:48Z'),
    ('U', 'Universal full date/time: Monday, April 17, 2006 9:22:48 PM'),
    ('Y', 'Year: April, 2006'),
    ('o', 'Roundtrip (local): 2006-04-17T14:22:48.2698750-07:00')
    )

MICRO_REPORT_LAYOUT_CHOICES = (
    (0, 'Standard product Microbiology Display'),
    (1, 'UPMC specific Microbiology Display')
    )

class AppsReporting(ConfigurationEntityBaseModel):
    cv_parent                       = models.ForeignKey('CVReportingPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    reporting_pl                    = models.ForeignKey('PlReportingPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)    
    reporting_pv                    = models.ForeignKey('PVReportingPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)    
    font_size                       = models.IntegerField(verbose_name='Report Font Size', default=9, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(1000)], help_text='Defines the Font Size to use in the report.<br/>This applies to:<br/>- Collaborate: TXT reports.<br/>- EHR Agent: TXT reports.<br/>- Patient List: TXT reports.<br/>- Patient View: TXT reports.<br/><i>Default: 9</i>')
    header_footer_font_type         = models.CharField(verbose_name='Report Header and Footer Font Type', choices=FONT_TYPE_CHOICES, default='Arial', max_length=60, help_text="Defines the Font Type in the header and footer of the report.<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><i>Default: Arial</i>")
    date_time_format                = models.CharField(verbose_name='Date Time Format', choices=DATE_TIME_FORMAT_CHOICES, blank=False, default='G', max_length=1, help_text="Defines the Date and Time format of the Report footer.<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><i>Default: General date/long time</i>")
    microbiology_report_layout      = models.IntegerField(verbose_name='Microbiology Report Layout', choices=MICRO_REPORT_LAYOUT_CHOICES, default=0, help_text='Defines the Microbiology Report Layout.<br><i>Default: Standard product Microbiology Display</i>')
    show_confidentiality_disclamer  = models.BooleanField(default=False, verbose_name='Show Confidentiality Disclaimer in Report', help_text = 'Determines whether the Clinical Viewer, Patient View, Collaborate and EHR Agent reports use the special disclaimer template (Word file) which displays the confidentiality disclaimer.<br/>True: The system uses the special Disclaimer templates for reports.<br/>False: The system uses the regular OOB templates for the reports (default).<br/><i>Default: False</i>')
    customer_logo                   = models.ImageField(null=True, blank=True, upload_to='Logos/Customer', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Customer Logo', help_text='Defines the customer logo image that will be displayed in the report:<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><b>Note:</b> Only .gif files are supported. The recommended size is: 120x40 px. The size cannot exceed %sx%s px.' % (LOGO_MAX_WIDTH, LOGO_MAX_HEIGHT))
    dbmotion_logo                   = models.ImageField(null=True, blank=True, upload_to='Logos/dbMotion', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='dbMotion Logo', help_text='Defines the dbMotion logo image that will be displayed in the report.<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><b>Note:</b> Only .gif files are supported. The recommended size is: 120x40 px. The size cannot exceed %sx%s px.' % (LOGO_MAX_WIDTH, LOGO_MAX_HEIGHT))
    MrnText                         = models.CharField(verbose_name='Patient identifier caption in reports', max_length=60, null=False, blank=False, default='MRN', help_text='Defines the caption used for the Patient Identifier field in the report header. For example, MRN or PHIN.<br/>This applies to:<br/>- Clinical Viewer: RTF, TIF and Clinical Summary selected items reports.<br/>- Collaborate: All reports.<br/>- EHR Agent: All reports.<br/>- Patient List: All reports.<br/>- Patient View: All reports.<br/><i>Default: MRN</i>')
    rtf_report_remove_reference_fields  = models.BooleanField(verbose_name='Remove internal links from RTF documents', default=False, help_text=get_help_text('Determines whether to remove internal links in RTF documents, because these internal links occasionally produce error messages in the document upon conversion to PDF.<br/>True: Removes RTF internal links. The links will still exist in the PDF file as text.<br/>False: Does not remove RTF internal links.', 'False'))
    

    def __unicode__(self):
        return ""
           
    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = 'Reporting'
               
class CVReportingPage(PageBaseModel):
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Reporting'
       
class PlReportingPage(PageBaseModel):
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Reporting'

class PVReportingPage(PageBaseModel):
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Reporting'
