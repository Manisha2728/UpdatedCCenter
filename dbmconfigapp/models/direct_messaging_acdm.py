'''
Created on Oct 2, 2014

@author: okalush
'''
from django.db import models
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel

GATEWAY_URL_CHOICES = (
    ('https://directuat.allscriptsclient.com:443/gateway/xdr.svc', 'URL for Testing (https://directuat.allscriptsclient.com:443/gateway/xdr.svc)'),
    ('https://gateway.acdm.allscriptscloud.com/gateway/xdr.svc', 'URL for Production (https://gateway.acdm.allscriptscloud.com/gateway/xdr.svc)')
    )

class DirectMessagingAcdmPage(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "ACDM"
        
class DirectMessagingAcdm(ConfigurationEntityBaseModel):
    parent                          = models.ForeignKey('DirectMessagingAcdmPage', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    enableSendingViaAcdm            = models.BooleanField(verbose_name='Enable sending TOC via ACDM', default=True, help_text='Determines whether sending TOC via ACDM is enabled.<br/>If True, the following parameters are mandatory.<br/>If False, Sending TOC assumes direct MedAllies connectivity.<br/>Note: For a detailed description of TOC implementation see "IHE Integration Implementation Guide".<br/><i>Default: False</i>')
    gatewayUrl                      = models.CharField(verbose_name='ACDM Gateway Url', choices=GATEWAY_URL_CHOICES, blank=False, max_length=100, default='', help_text="Defines the ACDM Gateway URL.<br/><i>Default: URL for Testing (https://directuat.allscriptsclient.com:443/gateway/xdr.svc)</i>")
    clientOid                       = models.CharField(verbose_name='ACDM Client OID', blank=True, max_length=500, default="", help_text='Defines the Client OID that was configured in the Allscripts Community Manager.')
    clientCertificateThumbprint     = models.CharField(verbose_name='ACDM Client Certificate Thumbprint', blank=True, max_length=500, default="", help_text='Defines the thumbprint of the ACDM Client Certificate that was previously obtained.<br/>For more details see "IHE Integration Implementation Guide".')    
    acdmCommunityName               = models.CharField(verbose_name='ACDM Community Name', blank=True, max_length=500, default="", help_text='Defines whether to work with a production HISP (e.g. Allscripts Community Direct Messaging) or a staging/testing HISP (e.g. Test Allscripts Community Direct Messaging).')        
    
    def __unicode__(self):
        return ''    
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Direct Messaging ACDM"
        history_meta_label = "ACDM"