'''
Created on 28.12.2017
@author: Ran Tayeb
'''
from dbmconfigapp.models.base import *
from django.template.defaultfilters import default
from .database_storage import DatabaseStorage

# Interopability Page model For Partitioning
class MyHRConnectivityPage(PageBaseModel):
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "MyHR Connectivity"


class MyHRConnectivityEntity(ConfigurationEntityBaseModel):
    page                = models.ForeignKey('MyHRConnectivityPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    enable_my_hr_flow   = models.BooleanField(verbose_name='Enable MyHR Connectivity', default=False, help_text=get_help_text('Enables MyHR Connectivity for Australian projects.','Disable'))
    my_hr_oid           = models.CharField(verbose_name='IHI source system OID', blank=True, max_length=260, help_text=get_help_text('Defines the Australian virtual source system used to retrieve the patient IHI. This OID must be identical to the OID of this virtual source system as configured in EMPI -> Authority Systems.','Empty'))
    pcehr_exist_url     = models.CharField(verbose_name='Does PCEHR exists URI',null = True, blank=True, max_length=260, help_text=get_help_text('Defines doesPCEHRexists URI to MyHR','Empty'))
    my_hr_node_id       = models.PositiveIntegerField(verbose_name='MyHR Node ID', null = True, blank=True, help_text=get_help_text('Defines MyHR Node id, node value should be between 101-120','Empty'))
    gain_access_url     = models.CharField(verbose_name='Gain PCEHR access URI',null = True, blank=True, max_length=260, help_text=get_help_text('Defines gainPCEHRAccess URI to MyHR','Empty'))
    get_document_list_url    = models.CharField(verbose_name='Get Document List URI',null = True, blank=True, max_length=260, help_text=get_help_text('Defines getDocumentList URI MyHR','Empty'))
    get_document_url    = models.CharField(verbose_name='Get Document URI',null = True, blank=True, max_length=260, help_text=get_help_text('Defines getDocument URI MyHR','Empty'))
    stylesheet          = models.FileField(null=True, blank=False, upload_to='MyHR/Stylesheet', storage=DatabaseStorage(settings.DBS_OPTIONS), verbose_name='CDA Stylesheet', help_text=get_help_text('Defines the stylesheet that will be used to display CDAs retrieved from the MyHR node. The file extension must be .xslt or .xsl for the system to function properly. The stylesheet should contain all styling as part of the xslt and should be XSLT 1.0.','DH_Generic_CDA_Stylesheet-1.3.0.xsl'))    
    
    
    def __unicode__(self):
        return self.name
           
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'MyHR Connectivity'
        history_meta_label = verbose_name
        
        
class MyHROrganizationsEntity(ConfigurationEntityBaseModel):
    page                = models.ForeignKey('MyHRConnectivityPage', on_delete=models.CASCADE, default=1)    
    iho_thumbprint      = models.CharField(verbose_name='IHO Thumbprint', max_length=260, help_text=get_help_text('Defines the thumbprint of IHO','Empty'))
    iho_name            = models.CharField(verbose_name='IHO Name', unique=True, max_length=260, help_text=get_help_text('Defines the IHO name','Empty'))
    org_name            = models.CharField(verbose_name='Organization Name', blank=True, max_length=260, help_text=get_help_text('Defines the Organization Name of the IHO','Empty'))
            
    def __unicode__(self):
        return self.name
           
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'MyHR Organization'
        history_meta_label = verbose_name
                
        


