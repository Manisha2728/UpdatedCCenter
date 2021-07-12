import sys
from django.db import models
from via.models import *
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel,\
    get_help_text
from django.core import validators

PARSED_DATE_TIME_FORMAT_CHOICES = (
    ('yyyy-MM-dd', 'yyyy-MM-dd'),
    ('yyyy-MM-dd HH:mm', 'yyyy-MM-dd HH:mm')
    )

PCP_RELATION_OPTIONS_CHOICES = (
    (0, 'CDR aligned PCP relation strategy'),
    (1, 'Last Updated PCP relation strategy')
    )
        
class PpolGeneral(ConfigurationEntityBaseModel):
    parent_empi_id                  = models.ForeignKey(EmpiPpolGeneralPage, on_delete=models.SET_NULL, null=True, default=1, editable=False)
    PatientDefaultCacheTolerance    = models.IntegerField( verbose_name='Patient Default Cache Tolerance (Seconds)', validators=[validators.MinValueValidator(-1), validators.MaxValueValidator(sys.maxsize)], default=-1, help_text=get_help_text("""
                Patient information is imported from the VIA service. To improve the Provider Registry service performance, the patient information is cached in the Provider Registry service.<br/>
                Each cached patient stores its last refreshed Date and Time. Patient retrieval service calls may specify the maximum period of time that they accept cached patient information to be used.<br/>
                For example, if a consumer accepts cached patient up to a week, and the actual patient was last refreshed 6 days ago, the Provider Registry will communicate to VIA to import updated data.<br/>
                In addition, the Provider Registry service may eagerly import patient information from VIA when the cached information is close to expiration.<br/>
                This configuration defines the default patient cache tolerance value in seconds.<br/>
                If a service call does not specify a cache tolerance, the service does not refresh the patient information.<br/>
                If you set a shorter period of time may lower the service response time.<br/>
                The default is that service calls shouldn't trigger a patient refresh, due to the 'CDR Auto Discovery' mechanism of ProviderRegistry, where loaded messages to CDR triggers a patient refresh.<br/>
                Possible Values: -1 (no refresh), 604800 (Week).
                """, '-1 (no refresh)'))
    ParsedDateTimeFormat            = models.CharField(verbose_name='Parsed Date Time Format', choices=PARSED_DATE_TIME_FORMAT_CHOICES, blank=False, max_length=20, default='yyyy-MM-dd HH:mm', help_text="Defines the DateTime format in the Provider Registry.<br/>In cases where Initiate will change to support the full date time (which might not be supported for all customers), the value should be changed to yyyy-MM-dd HH:mm.<br/>Relevant the following: <br/>- patient's birth date (and new-born age display)<br/>- patient's death time<br/>-  JoinHinMode (Consent) creation & update date<br/><i>Default: yyyy-MM-dd HH:mm</i>")
    PcpRelationStrategy             = models.IntegerField(verbose_name='PCP relation strategies', choices=PCP_RELATION_OPTIONS_CHOICES, default=0, help_text='Defines the PCP relation strategy.<br/>CDR aligned - This strategy enables a single patient cluster to have more than one PCP relation<br/>Last Updated - This strategy enables a single patient cluster to have only one PCP relation<br/><i>Default: CDR aligned PCP relation strategy.</i>')
    CdrDiscovery                     = models.BooleanField( verbose_name='Enable CDR discovery', default=True, help_text='Determines whether Provider Registry should sync both CDR patients and their PCP relations into Provider Registry DB. Used for CAG, Collaborate and PH.<br/><span style="font-style:italic">Default: True</span>')    
    MedicalStaffSync                = models.BooleanField( verbose_name='Enable medical-staff sync', default=True, help_text='Determines whether Provider Registry should sync CDR medical-staff into Provider Registry DB. Used for CAG, Collaborate.<br/><span style="font-style:italic">Default: True</span>')
    MaximumAttemptsNumber           = models.IntegerField( verbose_name='Maximum attempts number', validators=[validators.MinValueValidator(0), validators.MaxValueValidator(sys.maxsize)], default=3, help_text='Maximum number of attempts to try resolving either patients or relations in case of failure<br/><span style="font-style:italic">Default: 3.</span><br/>')
    PatientResetWorker              = models.IntegerField( verbose_name='Time duration until patient status reset', validators=[validators.MinValueValidator(0), validators.MaxValueValidator(sys.maxsize)], default=20, help_text='The time duration between failed patient and process status reset.<br/><span style="font-style:italic">Default: 20.</span><br/><span style="font-style:italic">Units: Minutes.</span><br/>')
    RelationSourceResetWorker       = models.IntegerField( verbose_name='Time duration until relation source status reset', validators=[validators.MinValueValidator(0), validators.MaxValueValidator(sys.maxsize)], default=20, help_text='The time duration between failed relation source and process status reset.<br/><span style="font-style:italic">Default: 20.</span><br/><span style="font-style:italic">Units: Minutes.</span><br/>')
    RelationTargetResetWorker       = models.IntegerField( verbose_name='Time duration until relation target status reset', validators=[validators.MinValueValidator(0), validators.MaxValueValidator(sys.maxsize)], default=20, help_text='The time duration between failed relation target and process status reset.<br/><span style="font-style:italic">Default: 20.</span><br/><span style="font-style:italic">Units: Minutes.</span><br/>')
    GeneralResetWorker              = models.IntegerField( verbose_name='Time duration until unexpected status reset', validators=[validators.MinValueValidator(0), validators.MaxValueValidator(sys.maxsize)], default=720, help_text='The time duration between unexpected failed item and process status reset.<br/><span style="font-style:italic">Default: 720.</span><br/><span style="font-style:italic">Units: Minutes.</span><br/>')
    MedicalStaffSyncTracing         = models.BooleanField( verbose_name='Enable medical-staff sync tracing files generation', default=False, help_text='Determines whether Provider Registry should generate trace files during CDR medical-staff synchronization.<br/><span style="font-style:italic">Default: False</span>')
    
    def __unicode__(self):
        return ''    
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "PPOL General"
        history_meta_label = "Provider Registry"