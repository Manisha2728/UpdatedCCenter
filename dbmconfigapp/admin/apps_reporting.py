from django.contrib import admin

from dbmconfigapp.models.apps_reporting import *
from django.forms import ModelForm, CharField, Select
from django.forms.models import BaseInlineFormSet
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline
from dbmconfigapp.forms import AppsReportingForm, VpoReportingInlineAdminForm
from dbmconfigapp.models.vpo import Vpo

########################################################
    
class VpoInline(dbmBaseAdminStackedInline):
    model = Vpo
    form = VpoReportingInlineAdminForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ['lab_susceptibility_methods_code_type', 'lab_report_fixed_width_font'], 'classes': ['wide', 'extrapretty']
                 }),
                 ) 
    radio_fields = {'lab_susceptibility_methods_code_type': admin.VERTICAL}
    
class ReportingInline(dbmBaseAdminStackedInline):
    form = AppsReportingForm
    model = AppsReporting
    fieldsets = [
        (model._meta.history_meta_label,               {'fields': ['MrnText', 'font_size', 'header_footer_font_type', 'date_time_format'
                                         , 'show_confidentiality_disclamer', 'rtf_report_remove_reference_fields']
                              , 'classes': ['wide', 'extrapretty'],}),
        ("Logos",        {'fields': 
                          ['dbmotion_logo', 'customer_logo'],
                          'classes': ['wide', 'extrapretty'],})
    ]
    

    
    verbose_name=""
    verbose_name_plural = "Reporting Display"
    radio_fields = {'microbiology_report_layout': admin.VERTICAL}
    

class AppsReportingBaseAdmin(dbmModelAdmin):
    inlines = (ReportingInline, VpoInline)
    save_on_top = True
    
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
                     

class CVReportingAdmin(AppsReportingBaseAdmin):
    model = CVReportingPage
    
       
class PlReportingPageAdmin(AppsReportingBaseAdmin):
    model = PlReportingPage  

class PVReportingPageAdmin(AppsReportingBaseAdmin):
    model = PVReportingPage
