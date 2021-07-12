from django.core import validators
from dbmconfigapp.models.base import ConfigurationEntityBaseModel
from dbmconfigapp.models.cvtables import ClinicalDomainLaboratory

from django.db import models

CHART_FORMAT_CHOICES = (
        (0, 'Chart in Line format'),
        (1, 'Chart in Column format'),
    )

RANGE_VALUES_CHOICES = (
        (0, 'Calculated by the Front End'),
        (1, 'Retrieved from the business functionality'),
    )

ABNORMAL_VALUES_CHOICES = (
        (0, 'Calculated using the business logic'),
        (1, 'Calculated based on the value of the range calculation parameter (above)'),
    )

DATE_FORMAT_CHOICES = (
        (0, 'The date is displayed in the DateTime format'),
        (1, 'The date is displayed as a string'),
    )



class LabChartDisplayOptions(ConfigurationEntityBaseModel):
    parent                  = models.ForeignKey(ClinicalDomainLaboratory, on_delete=models.SET_NULL, null=True, default=16)
    chart_format            = models.IntegerField(choices=CHART_FORMAT_CHOICES, default=0, verbose_name='Chart type', help_text='Determines whether the Lab Chart display is in line or column format<br><i>Default: Line</i>')
    range_values            = models.IntegerField(choices=RANGE_VALUES_CHOICES, default=1, verbose_name='Range values high/low calculation', help_text="Determines whether the range values high/low are retrieved from the business functionality or calculated by the Front End<br><i>Default: Retrieved from the business functionality</i>")
    abnormal_values         = models.IntegerField(choices=ABNORMAL_VALUES_CHOICES, default=1, verbose_name='Abnormal values calculation', help_text="Determines how the Abnormal values displayed in the chart are calculated.<br><i>Default: Based on the value of the range calculation parameter (above)</i>")
    date_format             = models.IntegerField(choices=DATE_FORMAT_CHOICES, default=0, verbose_name='Date display', help_text="Determines whether the date is displayed in the DateTime format or as a string.<br><i>Default: DateTime</i>")
    display_range_values    = models.BooleanField(default=False, verbose_name='The chart displays the range of values.', help_text="Determines whether the chart displays the range of values.<br><i>Default: False</i>")
    display_abnormal_in_color = models.BooleanField(default=False, verbose_name='The chart displays Abnormal values in color (red).', help_text="Determines whether the chart displays Abnormal values in color (red).<br><i>Default: False</i>")
    report_max_rows_in_regular_col = models.IntegerField(default=20, validators=[validators.MinValueValidator(1),], verbose_name='The maximum number of rows in the regular grid column', help_text='Defines the maximum number of rows in the regular grid column.<Br>This parameter is used to determine if the text can be displayed in the regular grid column.<Br><i>Default: 20</i>')
    report_max_chars_in_remark_col = models.IntegerField(default=600, validators=[validators.MinValueValidator(1),],verbose_name='The total maximum number of characters in the Remarks column', help_text='Defines the total maximum number of characters in the Remarks column of the Lab Results Report.<br>This parameter is used to determine if the text can be displayed in the regular grid Remarks column.<br><i>Default: 600</i>')
    report_max_rows_in_long_row_cell = models.IntegerField(default=33, validators=[validators.MinValueValidator(1),],verbose_name='The maximum number of rows in a Long Row cell', help_text='Defines the maximum number of rows in a Long Row cell.<br>This parameter is used to determine if the text can be displayed in the Long Row.<br><i>Default: 33</i>')
    
    def __unicode__(self):
        return 'Lab Chart Display Options'

    class Meta:
        app_label = "dbmconfigapp"
        verbose_name = 'Lab Chart Display Options'
        history_meta_label = 'Lab Chart Display Options'




