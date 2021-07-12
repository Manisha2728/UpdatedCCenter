'''
Created on Dec 3, 2013

@authors: EBliacher, TBener
'''
import sys
from django.db import models
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel,\
    get_help_text
from django.core import validators
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from .database_storage import DatabaseStorage
from configcenter import settings
import re
from .common import Message

CLINICAL_LOGIN_SCREEN_LOGOS_CHOICES = (
    (0, 'In the upper area of the login screen, the dbMotion logo is displayed and the lower area is empty.'),
    (1, 'In the upper area of the login screen, the customer logo is displayed and the lower area displays the dbMotion logo. Please upload the customer logo file below.'),
    (2, 'In the upper area of the login screen, the customer logo is displayed and the sentence "Powered by dbMotion" is displayed beneath the customer logo. The lower area of the login screen is empty. Please upload the customer logo file below and define the position of the sentence.')
    )

USE_ORG_TYPE_MODE_CHOICES = (
    ('True', 'Use the INS (institute) code'),
    ('False', 'Use the first parent organization'),
                                 )

RETURN_ACT_ORGANIZATION_AS_UNIT_CHOICES = (
    ('True', 'The unit is displayed'),
    ('False', 'The facility is displayed'),
                             )

DBM_PARAMETERS_CHOICES = (
    ('USER_UserName', 'User name'),
    ('USER_FirstName', 'User first name'),
    ('USER_LastName', 'User last name'),
    ('PAT_Calc_MRN', 'Leading MRN'),
    ('Calc_MRN_System', 'MRN source system'),
    ('PAT_Calc_Given', 'Patient first name'),
    ('PAT_Calc_Family', 'Patient last name'),
    ('PAT_BirthDate', 'Patient birth date'),
    ('NAV_CVNAME', 'Current Clinical View'),
                          )

# Data for dbMotion Parameters dialog window
DBM_PARAMS = (
    ('USER_UserName', 'User name', 'Nirw', 'The user name as defined in dbMotion Security Manager', 'Available in all dbMotion CVs'),
    ('USER_FirstName', 'User first name', 'Michael', 'The user\'s first name as defined in dbMotion Security Manager', 'Available in all dbMotion CVs'),
    ('USER_LastName', 'User last name', 'Vainer', 'The user\'s last name as defined in dbMotion Security Manager', 'Available in all dbMotion CVs'),
    ('PAT_Calc_MRN', 'Leading MRN', '123ABC456DEF', 'The leading MRN that was selected by the user in the patient search C.V.', 'Available after entering patient file. (Not be available in Working Lists and Patient Search CVs)'),
    ('Calc_MRN_System', 'MRN source system', 'St.Pierre ADT', 'The system source  related to the MRN', 'Available after entering patient file. (Not be available in Working Lists and Patient Search CVs)'),
    ('PAT_Calc_Given', 'Patient first name', 'Emile', 'The patient given name as defined  in the leading record,  selected by the user, from the patient search results', 'Available after entering patient file. (Not be available in Working Lists and Patient Search CVs)'),
    ('PAT_Calc_Family', 'Patient last name', 'Prenoms', 'The patient family name as defined in the leading record, selected by the user, from the patient search results.', 'Available after entering patient file. (Not be available in Working Lists and Patient Search CVs)'),
    ('PAT_BirthTime', 'Patient birth date', '12/2/1997 00:00', 'The patient date of birth as defined  in the leading record,  selected by the user, from the patient search results', 'Available after entering patient file. (Not be available in Working Lists and Patient Search CVs)'),
    ('NAV_CVNAME', 'Current Clinical View', 'Encounters', 'The CV in use when launching the application', 'Available after entering patient file. (Not be available in Working Lists and Patient Search CVs)'),
        )

USER_NAME_DISPLAY_OPTIONS_PATTERN = "^{\d+}(\W*\s*\|\s*{\d+})*$"

class ClinicalViewerGeneralPage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Clinical Viewer General"
        
def validate_name_format(value):
    compiledPattern = re.compile(USER_NAME_DISPLAY_OPTIONS_PATTERN)
    if not compiledPattern.match(value):
        raise ValidationError('The name you entered does not conform to the format. The string cannot be empty and each name part should be separated by the | symbol. The format should conform to the example shown below.')

def validate_string_is_a_num(value):
    if not (str(value).isdigit()):
        raise ValidationError('Enter a whole number.')

             
class ClinicalViewerGeneral(ConfigurationEntityBaseModel):
    parent                          = models.ForeignKey('ClinicalViewerGeneralPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    DefaultDomain                   = models.CharField( verbose_name='Domain name', blank=True, max_length=100, default='', help_text='Defines the domain that opens by default after login.<br/><i>Default: N/A</i>')
    IsOtherGroupExpanded            = models.BooleanField( verbose_name='Others group is always expanded', default=True, help_text='Determines whether, in grouping scenarios, the Others group of unspecified medical information/results is always expanded.<br/>If True, this data is always expanded.<br/>If False, the  data is always collapsed.<br/>*Note: this configuration applies to Medications, Allergies, Problems, Diagnosis, and Procedures.<br/><i>Default: True</i>')
    IsTextWrappingUsedInCD          = models.BooleanField( verbose_name='Text wrapping is used in a Clinical Document', default=True, help_text='Defines whether text wrapping is used in a Clinical Document, in Clinical Documents and Imaging clinical domains.<br/><i>Default: True</i>')
    IsShowMessageSectionDisclaimer  = models.BooleanField( verbose_name='Show the message section of the disclaimer in the clinical view status bar.', default=False, help_text='Determines whether to show the message section of the disclaimer in the clinical view status bar.<br/><i>Default: False</i>')
    IsShowLinkSectionDisclaimer     = models.BooleanField( verbose_name='Show the link section of the disclaimer in the clinical view status bar', default=False, help_text='Determines whether to show the link section of the disclaimer in the clinical view status bar<br/><i>Default: False</i>')
    UrlOnLinkSectionDisclaimer      = models.CharField(verbose_name='Disclaimer link address', blank=True, max_length=500, default="/dbMotionInformationServices/dbMotionInformationPage.aspx", help_text='Defines the URL used when clicking on the link section of the disclaimer.<br/>The default URL: The System Info Page.<br/><i>Default: /dbMotionInformationServices/dbMotionInformationPage.aspx</i>')
    UserNameDisplayOptions          = models.CharField(verbose_name='User name format', blank=False, validators=[validate_name_format], max_length=100, default="{0}, |{1}, |{2}|{3}, |{4}, |{5}", help_text='Defines the format for the parts of the user&apos;s name displayed in the Clinical Viewer User Header.<br/>0 = Title<br/>1 = First Name<br/>2 = Last Name<br/>3 = TitleUnmanaged<br/>4 = FirstNameUnmanaged<br/>5 = LastNameUnmanaged<br/><i>Default: {0}, |{1}, |{2}|{3}, |{4}, |{5}</i>')
    CustomerLogoFileName            = models.CharField(verbose_name='Customer Logo file name', blank=True, max_length=100, default="", help_text='Defines the file name of the customer&#39;s logo displayed in the Clinical Viewer login screen. The logo file should manually be saved to:<br/>C:\Program Files\dbMotion\Web\Sites\WebApp35\SiteImages\logos<br/>This configuration applies only in the case that the "Logos display" selection above includes the customer logo.<br/>The following are the logo image type and size requirements:<br/>Type: gif<br/>Height: 60px<br/>Width: 365px<br/><br/>Note: The logo file name should include the extension<br/><i>Example: customer.gif</i><br/><i>Default: No default value</i>')
    WebApplicationName              = models.CharField( verbose_name='Web Application Name', blank=False, max_length=100, default='dbMotionClinicalViewer', help_text='Defines the name of Clinical View Web Application.<br/><i>Default: dbMotionClinicalViewer</i>')
    DefaultLogoFile                 = models.ImageField(default='', null=True, blank=True, upload_to='ClinicalViewer/Logo', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='Logo File', help_text='Defines the default logo presented in the Clinical Viewer.<br/>The following are the logo image type and size requirements:<br/>Type: gif<br/>Height: 28px<br/>Width: 84px<br/><i>Default: No default value</i>')
    LoginScreenLogosOptions         = models.IntegerField(verbose_name='Logos display', choices=CLINICAL_LOGIN_SCREEN_LOGOS_CHOICES, default=0, help_text='<i>Default: In the upper area of the login screen, the dbMotion logo is displayed and the lower area is empty.</i>')
    CreditTitlePosition             = models.IntegerField(verbose_name='Position of "Powered by dbMotion" sentence', validators=[validators.MinValueValidator(0), validators.MaxValueValidator(250)], null=True, blank=True, max_length=3, default=120, help_text='Defines the horizontal position of the "Powered by dbMotion" sentence relative to the left corner of the login logo container<br/>The default horizontal position is in the center of the logo container, 120.<br/>0 will position the sentence on the far left side of the login logo container.<br/>250 will position the sentence on the far right side of the login logo container.<br/>Possible values: 0-250<br/><i>Default: 120</i>')
    
    def __unicode__(self):
        return ''    
    

    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Clinical Viewer General"
        
class DisclaimerConfigAdminForm(ModelForm):
    class Meta:
        model = ClinicalViewerGeneral
        fields = '__all__'
        
        widgets = {
            'UrlOnLinkSectionDisclaimer': forms.TextInput(attrs={'size':'100'}),
        }  
        
class ClinicalViewerGeneralAdminForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(ClinicalViewerGeneralAdminForm, self).__init__(*args, **kwargs)
        self.fields['LoginScreenLogosOptions'].required = False
        
        
    class Meta:
        model = ClinicalViewerGeneral
        fields = '__all__'

        widgets = {
            'DefaultDomain': forms.TextInput(attrs={'size':'100'}),
            'UserNameDisplayOptions': forms.TextInput(attrs={'size':'100'}),
            'CustomerLogoFileName': forms.TextInput(attrs={'size':'100'}),      
        }                          


    def clean(self):  
        cleaned_data = super(ClinicalViewerGeneralAdminForm, self).clean()
        LoginScreenLogosOptions = cleaned_data.get("LoginScreenLogosOptions")
        CustomerLogoFileName = cleaned_data.get("CustomerLogoFileName")
        CreditTitlePosition = cleaned_data.get("CreditTitlePosition")
        
        if LoginScreenLogosOptions > 0 and CustomerLogoFileName=='':
            msg = 'Logo file name cannot be empty.'
            self._errors['CustomerLogoFileName'] = self.error_class([msg])
        if LoginScreenLogosOptions==2 and CreditTitlePosition==None:
            msg = 'Please provide a number between 0 to 250'
            self._errors['CreditTitlePosition'] = self.error_class([msg])
            
        return self.cleaned_data     

            
        
        
        
class DisclaimerText(Message):
    cv_general_page         = models.ForeignKey('ClinicalViewerGeneralPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    message_link_text       = models.CharField(max_length=60, verbose_name="link text")
    
    def __unicode__(self):
        return "[%s - %s | %s]" % (self.message, self.message_link_text, self.culture)
    
    class Meta:
        app_label = "dbmconfigapp"
        unique_together = ("culture",)
        history_meta_label = "Disclaimer Texts"
        verbose_name = "Disclaimer text"
    

class WebCulture(ConfigurationEntityBaseModel):
    cv_general_page         = models.ForeignKey('ClinicalViewerGeneralPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    culture                 = models.CharField(max_length=10, unique=True, help_text='The culture that will be relevant to the date/time definition. For projects with a single language this can be left as default.')
    short_date_pattern      = models.CharField(max_length=20, verbose_name='date format', help_text='The date fields format presented in the clinical view and Patient List.')
    short_time_pattern      = models.CharField(max_length=20, verbose_name='time format', help_text='The time fields format presented in all the clinical views and Patient List.')
    long_time_pattern       = models.CharField(max_length=20, verbose_name='PLV time format', help_text='The time fields format presented in PLV clinical view.')
    date_separator          = models.CharField(max_length=10, help_text='The date separator presented in the clinical view and Patient List.')
    time_separator          = models.CharField(max_length=10, help_text='The time separator presented in the clinical view and Patient List.')
    
    def __unicode__(self):
        return self.culture
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "Culture"
        verbose_name = "Culture"
        
class ExternalApplication(ConfigurationEntityBaseModel):
    cv_general_page         = models.ForeignKey('ClinicalViewerGeneralPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    name                    = models.CharField(max_length=40, help_text='Defines the Name of the icon and link displayed in the Clinical Viewer navigation toolbar.')
    culture                 = models.CharField(max_length=10, help_text='Defines the culture, For example: en-US.')
    is_active               = models.BooleanField(default=True, verbose_name='Active', help_text='Determines whether the External Application icon is displayed (Default: true)')
    uri                     = models.CharField(max_length=200, verbose_name='URI', help_text='The URI of the External Application.')
    method                  = models.CharField(max_length=4, default='GET', choices=(('GET', 'GET'), ('POST', 'POST')), help_text='Defines the method of access to the external application (Default: GET)')
    

    def name_url(self):
        if self.id:
            return '<a href="%s" onclick="return showEditPopup(this);" title="Click to edit">%s</a>' % ("/admin/dbmconfigapp/externalapplication/%s/" % self.id, self.name)
        else:
            return '<a href="%s" onclick="return showEditPopup(this);" >Add new Application</a>' % "/admin/dbmconfigapp/externalapplication/add/"
    
    name_url.allow_tags = True
    name_url.short_description = 'Name'
    
    def parameters(self):
        return '; '.join('{}: {}'.format(p.name, p.static_value if p.is_static else '[{}]'.format(dict(DBM_PARAMETERS_CHOICES)[p.dbm_param])) for p in ExternalApplicationParameter.objects.filter(external_application=self))
    
    parameters.allow_tags = True
    
    def override_add_button_link(self):
        return "/admin/dbmconfigapp/externalapplication/add/"
    
    def __unicode__(self):
        return self.name
    
    def page_title(self):
        return ''
    
    class Meta:
        app_label = "dbmconfigapp"
        history_meta_label = "External Application Links"
        verbose_name_plural = "External Application Links"
        


def build_dbm_params_html():
    html = '<table><thead><tr><th>Parameter Name<th>In list name<th>Example<th>Description<th>Comments</tr></thead><tbody>{}</tbody></table>'
    rows = []
    for r in DBM_PARAMS:
        rows.append('<tr><td>{}</td></tr>'.format('</td><td>'.join(r)))
    
    return html.format(''.join(rows))

class ExternalApplicationParameter(ConfigurationEntityBaseModel):
    external_application    = models.ForeignKey(ExternalApplication, on_delete=models.CASCADE, null=False)
    name                    = models.CharField(max_length=40, verbose_name='parameter name', help_text='Name of parameter used by other application.')
    dbm_param               = models.CharField(max_length=20, verbose_name='parameter value', null=True, blank=True, default=None, choices=DBM_PARAMETERS_CHOICES, help_text='In case the parameter is static, enter the value to pass. In case it is a dbMotion parameter, choose the parameter to pass from the drop down list.')
    static_value            = models.CharField(max_length=20, verbose_name='static value', null=True, blank=True, default=None)
    is_static               = models.BooleanField(default=False, help_text=get_help_text('Indication if the parameter value is static or dbMotion parameter.', 'False'))
    
    def __unicode__(self):
        return self.name
    
    def description(self):
        return 'For more information about dbMotion Parameters <a id="opener" href="javascript:void(0)" dlgtext="%s">click here</a>.' % build_dbm_params_html() 
        
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name_plural = "External Application Parameters"
        unique_together = ("name", "external_application")
            