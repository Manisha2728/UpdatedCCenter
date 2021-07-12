from django.contrib import admin

from dbmconfigapp.models.clinical_viewer_general import ClinicalViewerGeneral, ClinicalViewerGeneralPage, ClinicalViewerGeneralAdminForm, DisclaimerText, WebCulture, DisclaimerConfigAdminForm, ExternalApplication, ExternalApplicationParameter
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline, get_grid_help_text, dbmBaseAdminTabularInline
from dbmconfigapp.models.vpo import VpoCommon, VpoCommunication, VpoFacilityDisplay
from dbmconfigapp.forms import VpoCommonInlineAdminForm, DisclaimerTextFormSet, WebCultureInlineForm, MinimumOneFormSet, ExternalApplicationParameterInlineForm, ExternalApplicationAdminForm

class VpoFacilityDisplayInline(dbmBaseAdminTabularInline):
    model = VpoFacilityDisplay

    list_display = ('display_name', 'facility_source')
    fields = ('display_name', 'facility_source')
    readonly_fields = ('display_name',)
    
    class Meta:
        help_text = "%s. %s." % (get_grid_help_text('Determines how to calculate the organization shown in the Facility field. This configuration affects Clinical Viewer, EHR Agent, Patient View and Patient List. ', 'Display the first participant or parent organization that is defined by the INS (institute) code'), "This option supports only the INS type and no other types")
    
class VpoCommunicationInline(dbmBaseAdminStackedInline):
    model = VpoCommunication
    fieldsets = [
                 (model._meta.history_meta_label, {'fields': ['is_encounter_conf_inheritance'], 'classes': ['wide', 'extrapretty']}),
                 ]

class VpoCommonInline(dbmBaseAdminStackedInline):
    model = VpoCommon
    form = VpoCommonInlineAdminForm
    section_name = 'Clinical Data Display Options'
    fieldsets = [
                 (section_name, {'fields': ['clinical_data_display_options'], 'classes': ['wide', 'extrapretty']}),
                 ]
    radio_fields = {'clinical_data_display_options': admin.VERTICAL}

    
class ClinicalViewerGeneralInline(dbmBaseAdminStackedInline):
    form = ClinicalViewerGeneralAdminForm
    model = ClinicalViewerGeneral
    fieldsets = [              
        ('Web Application Settings', {'fields': ['DefaultDomain', 'WebApplicationName', 'DefaultLogoFile'], 'classes': ['wide', 'extrapretty']}),
        ('Display Options', {'fields': ['IsOtherGroupExpanded', 'IsTextWrappingUsedInCD'], 'classes': ['wide', 'extrapretty']}),
        ('User Name Display', {'fields': ['UserNameDisplayOptions'], 'classes': ['wide', 'extrapretty']}),
        ('Login Screen Settings', {'fields': ['LoginScreenLogosOptions', 'CustomerLogoFileName', 'CreditTitlePosition'], 'classes': ['wide', 'extrapretty']}),
        ]
    
    radio_fields = {'LoginScreenLogosOptions': admin.VERTICAL}
    
class DisclaimerConfigInline(dbmBaseAdminStackedInline):
    form = DisclaimerConfigAdminForm
    model = ClinicalViewerGeneral
    fieldsets = [              
        ('Disclaimer in Status Bar', {'fields': ['IsShowMessageSectionDisclaimer', 'IsShowLinkSectionDisclaimer', 'UrlOnLinkSectionDisclaimer'], 'classes': ['wide', 'extrapretty'],
                                      'description': 'This configuration is used to determine if to show the disclaimer text and URL link that is displayed in the Clinical Viewer status bar. It provides a disclaimer text followed by a link (URL), displayed in the clinical view status bar on all Clinical Viewer pages (except the PSCV).' }),
        ]
    
    
class DisclaimerTextInline(dbmBaseAdminTabularInline):
    model = DisclaimerText
    formset = DisclaimerTextFormSet
    fields = ('message', 'message_link_text', 'culture')
    extra = 1
    verbose_name_plural = model._meta.history_meta_label
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    class Meta:
        help_text = get_grid_help_text('This configuration is used to configure the disclaimer text and URL link that is displayed in the Clinical Viewer status bar. It provides a (configurable) disclaimer text followed by a link (URL), displayed in the clinical view status bar on all Clinical Viewer pages (except the PSCV). Per each culture, configure both the disclaimer text and the link text that will be presented.', 'for culture en-US: Disclaimer text: "Not all clinical data is in the HIE.". Link text: "For details click here."')
       

class WebCultureInline(dbmBaseAdminTabularInline):
    model = WebCulture
    form = WebCultureInlineForm
    formset = MinimumOneFormSet
    fields = ('culture', 'short_date_pattern', 'date_separator', 'short_time_pattern', 'long_time_pattern', 'time_separator')
    extra = 1
    verbose_name_plural = model._meta.history_meta_label
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    class Meta:
        help_text = get_grid_help_text('Determine how the date and time are displayed in both Clinical Views. Use the word "Default" for using the default format for selected culture. <a target="_blank" href="http://msdn.microsoft.com/en-us/library/system.globalization.datetimeformatinfo(v=vs.71).aspx">For more information click here.</a>', 'Culture: default; Date format: default; Date separator: default; Time format: HH:mm; PLV time format: HH:mm:ss; Time Separator: default;')


    
class ExternalApplicationsInline(dbmBaseAdminTabularInline):
    model = ExternalApplication
    formset = MinimumOneFormSet
    fields = ('name_url', 'is_active', 'uri', 'method', 'culture', 'parameters') 
    readonly_fields = ('name_url', 'is_active', 'uri', 'culture', 'method', 'parameters')
    extra = 0
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    class Meta:
        help_text = get_grid_help_text('You can configure the access to external applications from the Clinical Viewer, using the <b>External Application</b> icon and link displayed in the navigation toolbar (at the top of the screen). The link is used to access external applications.', 'The System Info page settings is configured as default. Name: dbMotionSystemInfo; Active: True; URI: /dbMotionInformationServices/dbMotionInformationPage.aspx; Method: GET; Culture: en-US; No parameters.')
        add_link = "/admin/dbmconfigapp/externalapplication/add/"

class ClinicalViewerGeneralAdmin(dbmModelAdmin):
    model = ClinicalViewerGeneralPage
    inlines = (ClinicalViewerGeneralInline, DisclaimerConfigInline, DisclaimerTextInline, VpoFacilityDisplayInline, VpoCommunicationInline, VpoCommonInline, WebCultureInline, ExternalApplicationsInline)
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'services')
    
    
####################################################################################


class ExternalApplicationParametersInline(dbmBaseAdminTabularInline):
    model = ExternalApplicationParameter
    form = ExternalApplicationParameterInlineForm
    fields = ('name', 'is_static', 'dbm_param', 'static_value')
    extra = 1
    
    
class ExternalApplicationAdmin(dbmModelAdmin):
    model = ExternalApplication
    inlines = (ExternalApplicationParametersInline,)
    fieldsets = [              
        ('External Application Properties',
            {'fields': ['name', 'culture', 'uri', 'method', 'is_active'], 'classes': ['wide', 'extrapretty'] }),
        ]
    radio_fields = {'method': admin.HORIZONTAL }
    form = ExternalApplicationAdminForm
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
   
