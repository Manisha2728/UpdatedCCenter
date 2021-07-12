from dbmconfigapp.models.base import *
from django.core.exceptions import ValidationError

CAPSULE_TYPES_OPTIONS_CHOICES = (
    (1, 'Hospital To HMO'),
    (2, 'HMO To HMO')
    )

class CapsulePage(PageBaseModel):
    
    def page_title(self):
        return super(CapsulePage, self).page_title() + " (For Israeli market only)"
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Capsule Service"


class CapsuleService(ConfigurationEntityBaseModel):
    capsule_page                        = models.ForeignKey(CapsulePage, on_delete=models.CASCADE)
    scheduled_time                      = models.TimeField(verbose_name="Start Time (for Daily)")
    end_scheduled_time                  = models.TimeField(verbose_name="End Time (for Daily)", blank = True, default = None, null = True, help_text='Note: The EndTime setting enables working time frame control of the capsule service. This time frame controls the working time of the capsule service when processing a large number of capsule generation requests, as expected in the quarterly process.<br/><i>Default: Empty</i>')
    local_folder                        = models.CharField(verbose_name='Set the archive / local folder for the auto generated Capsules', max_length=255, default="C:\Capsules")
    vault_folder                        = models.CharField(verbose_name='Set the destination folder for auto generated Capsules', max_length=255, default="C:\Capsules")
    on_demand_local_folder              = models.CharField(verbose_name='Set the local folder for the On Demand Capsules', max_length=255, default="C:\Capsules\OnDemand\CCD_LOCAL")
    on_demand_vault_folder              = models.CharField(verbose_name='Set the archive / destination folder for the On Demand Capsules', max_length=255, default="C:\Capsules\OnDemand\CCD_DEST")
    num_of_days_to_delete_capsules      = models.PositiveIntegerField(verbose_name='Set number of days to delete archive from local folder', default=30)
    capsules_paging_size                = models.PositiveIntegerField(verbose_name='Set how many capsules can be generated at the same time', default=10)
    confidentiality_filter              = models.BooleanField(verbose_name='Enable Confidentiality filter to filter confidential data', default=False)
    capsule_type                        = models.IntegerField(verbose_name='Capsule Types', choices=CAPSULE_TYPES_OPTIONS_CHOICES, default=1, help_text='Defines the Capsule Type.<br/>Possible types:<br/>1) Hospital To HMO<br/>2) HMO to HMO<br/><i>Default: Hospital To HMO.</i>')
    outbound_csv_vault_folder           = models.CharField(verbose_name='Set the HMO outbound csv folder', max_length=255, blank=True, null=True, default=None)
    inbound_csv_vault_folder            = models.CharField(verbose_name='Set the HMO inbound csv folder', max_length=255, blank=True, null=True, default=None)

    def clean(self):
        if (self.scheduled_time == self.end_scheduled_time):
            raise ValidationError('Start time and End time should be different.')
    class Meta:
        app_label = "dbmconfigapp"   
        history_meta_label = 'Capsule Service'    

