'''
Created on Jan 19, 2014

@author: EBliacher
'''

def getCVClinicalDomainById(clinical_domain_id):
    from dbmconfigapp.models import cvtables
    if clinical_domain_id==1:
        return cvtables.ClinicalDomainAllergies.objects.all()[0]
    elif clinical_domain_id==2:
        return cvtables.ClinicalDomainProblems.objects.all()[0]
    elif clinical_domain_id==3:
        return cvtables.ClinicalDomainDiagnoses.objects.all()[0]
    elif clinical_domain_id==4:
        return cvtables.ClinicalDomainImmunizations.objects.all()[0]
    elif clinical_domain_id==5:
        return cvtables.ClinicalDomainPathologies.objects.all()[0]
    elif clinical_domain_id==6:
        return cvtables.ClinicalDomainMedications.objects.all()[0]
    elif clinical_domain_id==7:
        return cvtables.ClinicalDomainEncounters.objects.all()[0]
    elif clinical_domain_id==9:
        return cvtables.ClinicalDomainPlv.objects.all()[0]
    elif clinical_domain_id==11:
        return cvtables.ClinicalDomainProcedures.objects.all()[0]
    elif clinical_domain_id==13:
        return cvtables.ClinicalDomainVitals.objects.all()[0]
    elif clinical_domain_id==15:
        return cvtables.ClinicalDomainLabResultsHistory.objects.all()[0]
    elif clinical_domain_id==16:
        return cvtables.ClinicalDomainLaboratory.objects.all()[0]
    elif clinical_domain_id==17:
        return cvtables.ClinicalDomainImaging.objects.all()[0]
    elif clinical_domain_id==18:
        return cvtables.ClinicalDomainDocuments.objects.all()[0]
