from dbmconfigapp.models.base import *
from django.template.defaultfilters import default


class CVCCDADisplayPage(PageBaseModel):
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "CCDA Display, Report and Data Export"

class DataExportCCDADisplayPage(PageBaseModel):
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "CCDA Display and Data Export"
        
CCDA_DISPLAY_MODE_CHOICES = (
    (0,'PDF'),
    (1, 'CVE'),
    )

ENVIRONMENT_CHOICES = (
    (0, 'Testing'),
    (1, 'Production')
    )

CCDA_URL_MODE_CHOICES = (
    (0,'Cloud'),
    (1, 'On premise'),
    )

class CCDADisplay(ConfigurationEntityBaseModel):
    cv_parent               = models.ForeignKey('CVCCDADisplayPage', on_delete=models.SET_NULL, default=1, null=True, editable=False)
    pv_parent         = models.ForeignKey('PVCCDADisplayPage', on_delete=models.SET_NULL, default=1, null=True, editable=False)
    dataexport_parent         = models.ForeignKey('DataExportCCDADisplayPage', on_delete=models.SET_NULL, default=1, null=True, editable=False)
    display_mode             = models.IntegerField(verbose_name='CCDA Display Mode', blank=False, choices=CCDA_DISPLAY_MODE_CHOICES, default=0, help_text=get_help_text('Determines in which Mode the CCDA is displayed when it is opened in the CV, CVA and PV.<br>PDF: Displayed as a PDF using the Allscripts PDF Converter Web API<br>CVE: CCDA is opened with the Interactive CVE (CVE is Allscripts Clinical View Engine)','PDF'))
    cve_renew_certificate          = models.CharField(verbose_name='Certificate', blank=True, max_length=500, help_text='Defines the Certificate Thumbprint for the Retrieval Key. The Certificate must be downloaded from the Allscripts Community Configuration Manager (CCM) and installed on the Application server.')
    environment                     = models.IntegerField(verbose_name='Environment', choices=ENVIRONMENT_CHOICES, blank=False, default=1, help_text=get_help_text('Defines the community library environments.', 'Testing'))
    source_system                    = models.CharField(verbose_name='Source System', blank=True, max_length=500, default="", help_text='Defines the dbMotion project OID.')
    service_location             = models.IntegerField(verbose_name='Service location', blank=False, choices=CCDA_URL_MODE_CHOICES, default=0, help_text=get_help_text('Determines the type of service that will be used.<br>Cloud: Allscripts remote cloud service<br>On premise: Customer local service','Cloud'))
    
    retrieval_key_cloud_service = models.CharField(verbose_name='Retrieval key for Cloud service', blank=False, max_length=500, default="", help_text='URL for retrieval key for Cloud service')
    CCDA_export_continuity_of_care_document = models.CharField(verbose_name='CCDA export Continuity of Care Document', blank=False, max_length=500, default="https://taas1000-prod-us.csg.az.allscriptscloud.com/transform/CCDA_R21_ContinuityOfCareDocument/", help_text='URL for CCDA export Continuity of Care Document')
    CCDA_export_discharge_summary = models.CharField(verbose_name='CCDA export Discharge Summary', blank=False, max_length=500, default="https://taas1000-prod-us.csg.az.allscriptscloud.com/transform/CCDA_R21_DischargeSummary/", help_text='URL for CCDA export Discharge Summary')
    CCDA_export_referral_notes = models.CharField(verbose_name='CCDA export Referral Notes', blank=False, max_length=500, default="https://taas1000-prod-us.csg.az.allscriptscloud.com/transform/CCDA_R21_ReferralNote/", help_text='URL for CCDA export Referral Notes')
    CCDA_export_unstructured_document = models.CharField(verbose_name='CCDA export Unstructured Document', blank=False, max_length=500, default="https://taas1000-prod-us.csg.az.allscriptscloud.com/transform/CCDA_R21_UnstructuredDocument/", help_text='URL for CCDA export Unstructured Document')
    Cve_document_conversion = models.CharField(verbose_name='CVE document conversion', blank=False, max_length=500, default="https://viewer-prod-us.csg.az.allscriptscloud.com", help_text='URL for CVE document conversion')
    Pdf_document_conversion = models.CharField(verbose_name='PDF document conversion', blank=False, max_length=500, default="https://cdatopdf-prod-us.csg.az.allscriptscloud.com/api/convert", help_text='URL for PDF document conversion')
    vaas_document_conversion = models.CharField(verbose_name='VAAS document conversion', blank=False, max_length=500, default="", help_text='URL for VAAS document conversion. This service is only supported for the Cloud and will work via Cloud regardless if On premise option is selected.')
    transformation_cloud_service = models.CharField(verbose_name='Transformation cloud service', blank=True, max_length=500, default="", help_text='URL for dbMotion transformation cloud service')
    transformation_service_subscription = models.CharField(verbose_name='Transformation service subscription', blank= True, max_length=500, default="",help_text='Subscription key for dbMotion transformation cloud service')
    customer_name = models.CharField(verbose_name= 'Customer Name', blank=False, max_length=500, default="dbMotion",help_text='Defines the dbMotion customer name.')

    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = 'CCDA Display and Report'

        