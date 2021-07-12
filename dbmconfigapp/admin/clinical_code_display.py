from dbmconfigapp.models import *
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminTabularInline
from dbmconfigapp.forms import ClinicalCodeDisplayForm
from django.db.models import Q

class ClinicalCodeDisplayInline_Base(dbmBaseAdminTabularInline):
    aspect = ''
    model = ClinicalCodeDisplay
    fields = ('business_table', 'code_name', 'vocabulary_domain', 'display_as')
    readonly_fields = ('business_table', 'code_name', 'vocabulary_domain')
    form = ClinicalCodeDisplayForm
    ordering = ('business_table', 'code_name')
    
    def queryset(self, request):
        qs = super(ClinicalCodeDisplayInline_Base, self).queryset(request)
        qs = qs.filter(business_aspect=self.aspect)
        qs = ExcludeClinicalCodeDisplay(qs, self.aspect)
        return qs
    
    def section_name(self):
        return self.aspect

    
    verbose_name_plural = section_name

class ClinicalCodeDisplayInline_Allergies(ClinicalCodeDisplayInline_Base):
    aspect = 'AllergyIntolerance'
    class Meta:
        help_text = 'Note that the Allergies Reaction.code configuration will affect Immunization Reaction.code as well'

class ClinicalCodeDisplayInline_ClinicalDocuments(ClinicalCodeDisplayInline_Base):
    aspect = 'ClinicalDocuments'
    
class ClinicalCodeDisplayInline_Diagnosis(ClinicalCodeDisplayInline_Base):
    aspect = 'Diagnosis'
    class Meta:
        help_text = 'Note that the following configuration points must be identical : Diagnosis (ValueCode), AllergyIntolerance (ReactionCode), and Immunization (ReactionCode)'
    
class ClinicalCodeDisplayInline_Encounter(ClinicalCodeDisplayInline_Base):
    aspect = 'Encounter'
    
class ClinicalCodeDisplayInline_Imaging(ClinicalCodeDisplayInline_Base):
    aspect = 'Imaging'
    
class ClinicalCodeDisplayInline_Immunization(ClinicalCodeDisplayInline_Base):
    aspect = 'Immunization'
    class Meta:
        help_text = 'Note that the following configuration points must be identical : Diagnosis (ValueCode), AllergyIntolerance (ReactionCode), and Immunization (ReactionCode)'
    
class ClinicalCodeDisplayInline_Laboratory(ClinicalCodeDisplayInline_Base):
    aspect = 'Laboratory'
    
class ClinicalCodeDisplayInline_MeasurementsEvent(ClinicalCodeDisplayInline_Base):
    aspect = 'MeasurementsEvent'
    
class ClinicalCodeDisplayInline_Medication(ClinicalCodeDisplayInline_Base):
    aspect = 'Medication'
    
class ClinicalCodeDisplayInline_Demography(ClinicalCodeDisplayInline_Base):
    aspect = 'Demography'
    
class ClinicalCodeDisplayInline_Pathology(ClinicalCodeDisplayInline_Base):
    aspect = 'Pathology'
    
class ClinicalCodeDisplayInline_Problems(ClinicalCodeDisplayInline_Base):
    aspect = 'Problems'
    
class ClinicalCodeDisplayInline_Procedure(ClinicalCodeDisplayInline_Base):
    aspect = 'Procedure'
    
class ClinicalCodeDisplayInline_Summary(ClinicalCodeDisplayInline_Base):
    aspect = 'Summary'

class ClinicalCodeDisplayAdmin_Base(dbmModelAdmin):
    inlines = (ClinicalCodeDisplayInline_Allergies, ClinicalCodeDisplayInline_ClinicalDocuments,
                ClinicalCodeDisplayInline_Diagnosis, ClinicalCodeDisplayInline_Problems, ClinicalCodeDisplayInline_Imaging,
                ClinicalCodeDisplayInline_Immunization, ClinicalCodeDisplayInline_Laboratory, ClinicalCodeDisplayInline_Pathology, 
                ClinicalCodeDisplayInline_Medication, ClinicalCodeDisplayInline_Demography, ClinicalCodeDisplayInline_Summary, 
                ClinicalCodeDisplayInline_MeasurementsEvent, ClinicalCodeDisplayInline_Procedure, ClinicalCodeDisplayInline_Encounter) 
    exclude = ('page_help_text', 'page_name', 'services')
    def __init__(self, *args, **kwargs):
        super(ClinicalCodeDisplayAdmin_Base, self).__init__(*args, **kwargs)
        self.model.help_text_1 = "Defines the priority order for displaying the Code Designation, which defines the text that is displayed for each clinical code in Clinical Viewer, EHR Agent, Patient View and Patient List. The Code Designation Priority Order configuration provides the following options:<br><br><ul><li><b>Preferred</b> - Code Designation as configured in the preferred code translations (applied for EHR Agent and Patient View).</li><li><b>Baseline</b> - Code Designation as defined in the dbMotion Ontology.</li><li><b>Local</b> - Code Designation as received from the act's source system.</li><li><b>Text</b> - Displays the text as it was sent in the original message.</li></ul>For each field, if the first priority does not exist or is not valid, the second priority is used, and so on.<br>Change the priority order by dragging and dropping the option as required for each field.<br><br>Default priority order: Preferred, Baseline, Local, Text"


class ClinicalCodeDisplayAdmin(ClinicalCodeDisplayAdmin_Base):
    model = ClinicalCodeDisplayPage

class PlClinicalCodeDisplayAdmin(ClinicalCodeDisplayAdmin_Base):
    model = PlClinicalCodeDisplayPage

class PVClinicalCodeDisplayAdmin(ClinicalCodeDisplayAdmin_Base):
    inlines = (ClinicalCodeDisplayInline_Allergies, ClinicalCodeDisplayInline_ClinicalDocuments,ClinicalCodeDisplayInline_Diagnosis,ClinicalCodeDisplayInline_Medication)
    model = PVClinicalCodeDisplayPage

#remove Clinical Code Display PA-2520    
def ExcludeClinicalCodeDisplay(qs, aspect):
    # Encounter
    if aspect == "Encounter":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Encounter", "Encounter", "UncertaintyCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Encounter", "Encounter", "LengthOfStayQuantity_UnitCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Encounter", "Encounter", "AdmissionReferralSourceCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Encounter", "Encounter", "PriorityCode")
    
    # Medication
    if aspect == "Medication":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Medication", "MedicationRequest", "PriorityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Medication", "MedicationSupply", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Medication", "MedicationSupply", "TypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Medication", "MedicationSupply", "QuantityUnitCode")
    # Summary
    if aspect =="Summary":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "AllergyIntolerance", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "AllergyIntolerance", "UncertaintyCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "AllergyIntolerance", "Code")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "LaboratoryEvent", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Encounter", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "SubstanceAdministration", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "SubstanceAdministration", "DurationUnitCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Immunizations", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Immunizations", "DoseQuantityUnitCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "ClinicalDocuments", "DocumentCompletionCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "ClinicalDocuments", "DocumentTypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "ClinicalDocuments", "MediaTypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "ClinicalDocuments", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Conditions", "SeverityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Conditions", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Conditions", "UncertaintyCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Imaging", "Code")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Imaging", "ImagingTypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Imaging", "MoodCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Imaging", "PriorityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Imaging", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Procedures", "Code")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Procedures", "ServiceCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Summary", "Procedures", "StatusCode")
        
        
    #Immunization
    if aspect =="Immunization":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Immunization", "Immunization", "PriorityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Immunization", "Immunization", "MoodCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Immunization", "Immunization", "DoseQuantityUnitCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Immunization", "Immunization", "ApproachSiteCode")
        
    #Allergy
    if aspect =="AllergyIntolerance":    
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "AllergyIntolerance", "AllergyIntolerance", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "AllergyIntolerance", "AllergyIntolerance", "UncertaintyCode")
        
    #Pathology
    if aspect =="Pathology":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Pathology", "Pathology", "StatusCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Pathology", "Pathology", "PriorityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Pathology", "Pathology", "StructureTypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Pathology", "Pathology", "ReportMediaTypeCode")
        
    #Labs
    if aspect =="Laboratory":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Laboratory", "LaboratoryEvent", "PriorityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Laboratory", "LaboratoryEvent", "StructureTypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Laboratory", "LaboratoryEvent", "ConfidentialityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Laboratory", "LaboratoryResult", "PriorityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Laboratory", "LabTreeItem", "Code")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Laboratory", "LaboratoryResult", "Code")
        
    #Demography
    if aspect =="Demography":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Demography", "ParticipantOrganization", "TypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Demography", "PatientContacts", "PartTypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Demography", "PatientContacts", "ValueCode")
        
    #Clinical Document
    if aspect =="ClinicalDocuments":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "ClinicalDocuments", "ClinicalDocuments", "PriorityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "ClinicalDocuments", "ClinicalDocuments", "UncertaintyCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "ClinicalDocuments", "ClinicalDocuments", "MoodCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "ClinicalDocuments", "ParticipantOrganization", "Code")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "ClinicalDocuments", "ParticipantOrganization", "TypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "ClinicalDocuments", "ParticipantOrganization", "OrganizationCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "ClinicalDocuments", "ParticipantOrganization", "StatusCode")
        
    #Disagnosis
    if aspect =="Diagnosis":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Diagnosis", "Diagnosis", "ObservationStatusValueCode")
        
    #Problem
    if aspect =="Problems":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Problems", "Problems", "MethodCode")
        
    #Measurements
    if aspect =="MeasurementsEvent":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "MeasurementsEvent", "MeasurementsEvent", "Code")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "MeasurementsEvent", "MeasurementsEvent", "ClusterCode")
        
    #Imaging
    if aspect =="Imaging":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Imaging", "Imaging", "PriorityCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Imaging", "Imaging", "MoodCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Imaging", "Imaging", "UncertaintyCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Imaging", "Imaging", "TargetSiteCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Imaging", "Imaging", "MethodCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Imaging", "Imaging", "MediaTypeCode")
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Imaging", "Imaging", "InterpretationCode")
        
    #Procedure
    if aspect == "Procedure":
        qs = ExcludeClinicalCodeDisplay_Internal(qs, "Procedure", "Procedure", "UncertaintyCode")
    
        
    return qs
    
def ExcludeClinicalCodeDisplay_Internal(qs, aspect, table, codename):
    return qs.exclude(Q(business_table=table) & Q(code_name=codename))


    

    
    