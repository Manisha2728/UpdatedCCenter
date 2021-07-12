from dbmconfigapp.models.pl_general import PlGeneralPage
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline, get_grid_help_text, dbmBaseAdminTabularInline
from dbmconfigapp.models.pl_general import EncounterDiagnosisRelationship
from federation.models import Node

from dbmconfigapp.admin.clinical_viewer_general import VpoFacilityDisplayInline

field_description = 'This configuration determines the values used for Primary and Admitting Diagnoses in the encounter-condition act-relationship (Field name: PriorityNumber).<br>The values are used as part of the logic that determines the display of the Encounter Diagnosis (or Encounter Reason) in the dbMotion clinical applications (for example, the data displayed in Discharge Diagnosis or the Admitted Reason fields).<br>The configuration is required since different values may be used depending on the customer location (for example, in the American market the values are Admitting=0 and Primary=1 while in the Israeli market the values are Primary=1, 6 and Other=0, while there is no value for Admitting) and on the specific field in the application.<br>This configuration affects Clinical Viewer Agent, Patient List and Patient View. For a detailed description of the business logic, see the Functional Specification documentation.'
class EncounterDiagnosisRelationshipInline(dbmBaseAdminStackedInline):
    model = EncounterDiagnosisRelationship
    fieldsets = [
                 (model._meta.history_meta_label, {'fields': ['primary_diagnosis', 'admitted_diagnosis'], 'description' : field_description, 'classes': ['wide', 'extrapretty']}),
                 ]    
       
    
    verbose_name_plural = model._meta.history_meta_label
      
    class Meta:
        help_text = get_grid_help_text('Help goes here and can be formatted to whatever we want')
           
                      
class PlGeneralAdmin(dbmModelAdmin):
    model = PlGeneralPage
    inlines = (VpoFacilityDisplayInline, EncounterDiagnosisRelationshipInline)
    exclude = ('page_help_text', 'page_name', 'services')
