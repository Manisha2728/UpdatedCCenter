from dbmconfigapp.models.ehragent_measurements import EHRAgentSemanticGroup, EHRAgentMeasurementProperties
from dbmconfigapp.admin.dbm_ModelAdmin import get_grid_help_text, dbmBaseAdminTabularInline, ServicesToRestart, dbmModelAdmin

class MeasurmentInline(dbmBaseAdminTabularInline):
    model = EHRAgentMeasurementProperties
    ordering = ('order','domain_id',)
    fields = ('domain_id', 'order', 'hide_uom')
    extra = 1
    
    class Meta:
            help_text = get_grid_help_text("Add each of the new Measurements you want to display in this semantic group, by defining the following attributes: <br><b>Vocabulary Domain</b> = ID of the vocabulary domain. <br><b>Display Name</b> = Acronym for the measurement that you want to display. It will be displayed to the left of the measurement number. <br>If there is a Measurement result with at least one ID from this configured list, the MeasurementEvent will be displayed as a row of this semantic group.")

class EhrAgentSemanticGroupAdmin(dbmModelAdmin, ServicesToRestart):
    model = EHRAgentSemanticGroup
    list_display = ('display_name', 'order', 'measurements',)
    list_editable = ('order',)
    ordering = ('order',)
    inlines = (MeasurmentInline, )
    fieldsets = [(model._meta.history_meta_label, 
                 {'fields': ('display_name', 'order',), 'description': 'This configuration enables you to configure the semantic grouping in the Measurements category.<br><b>Group Display Name:</b> Defines the name of the new semantic group under Measurements.<br><br><b>Note:</b> The order of the Semantic Groups determines the order that the groups will be displayed in the Measurement category. <br>For example, the default configuration displays <b>Vital Signs</b> as the first group and <b>Height, Weight, & BMI</b> as the second group.', 'classes': ['wide', ]}), ]
    change_form_template = 'admin/change_form_default.html'
    
    def has_add_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    
    def changelist_view(self, request, extra_context=None):
        cl = super(EhrAgentSemanticGroupAdmin, self).changelist_view(request, extra_context)
        if hasattr(cl, 'context_data'): cl.context_data['title'] = 'Configuring Semantic Grouping of Measurements'
        return cl

    class Media:
        js = ['admin/js/dbmconfigapp/patient_search.js']

    class Meta:
        tree_id = 'ehragent_measurements'

