from dbmconfigapp.models.base import *


class CvPatientDisplayPage(PageBaseModel):
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = "Patient Display"
        history_meta_label = "Clinical Viewer Patient Display"


