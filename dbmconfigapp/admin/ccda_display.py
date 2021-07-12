from dbmconfigapp.models.ccda_display import CCDADisplay, CVCCDADisplayPage, DataExportCCDADisplayPage
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline
from dbmconfigapp.forms import CCDADisplayInlineForm
from django.contrib import admin

class CCDADisplayInline(dbmBaseAdminStackedInline):
    model = CCDADisplay
    form = CCDADisplayInlineForm
    fieldsets = [              
        ('CCDA Display and Report Settings',{'fields': ['display_mode',]}),
        ('CCDA Configuration',{'fields': ['transformation_cloud_service', 'transformation_service_subscription', 'cve_renew_certificate', 'source_system', 'customer_name',
                                                            'retrieval_key_cloud_service',
                                                            'Cve_document_conversion',
                                                            'Pdf_document_conversion',
                                                            'vaas_document_conversion'
                                                            ], 
                                      'description' : 'Note: The configuration enables connections between dbMotion and Allscripts Common Component Services such as Clinical Viewer Engine (CVE), PDF Converter, and Validation as a Service (VaaS).<br>Refer to the IHE Implementation Guide for more detail.'}),
       
        ]
    radio_fields = {'display_mode': admin.VERTICAL,'service_location': admin.VERTICAL} 



class DataExportCCDADisplayInline(dbmBaseAdminStackedInline):
    model = CCDADisplay
    form = CCDADisplayInlineForm
    fieldsets = [              
        ('Allscripts Cloud Services',{'fields': ['cve_renew_certificate', 'source_system'], 
                                      'description' : 'The configuration enables connections between dbMotion and Allscripts Common Component Services such as Clinical Viewer Engine (CVE), PDF Converter, and Validation as a Service (VaaS).<br>Refer to the IHE Implementation Guide for more detail.'}),
        ]
class CCDADisplayAdmin_Base(dbmModelAdmin):
    inlines = (CCDADisplayInline,) 
   
    def __init__(self, *args, **kwargs):
        super(CCDADisplayAdmin_Base, self).__init__(*args, **kwargs)


class CVCCDADisplayAdmin(CCDADisplayAdmin_Base):
    model = CVCCDADisplayPage

class DataExportCCDADisplayAdmin(dbmModelAdmin):
    model = DataExportCCDADisplayPage
    inlines = (DataExportCCDADisplayInline,)
    
    def __init__(self, *args, **kwargs):
        super(DataExportCCDADisplayAdmin, self).__init__(*args, **kwargs)

