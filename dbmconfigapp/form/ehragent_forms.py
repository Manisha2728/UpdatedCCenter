from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from dbmconfigapp.models.base import get_help_text
from dbmconfigapp.models.ehragent import EhrAgentGeneral
from dbmconfigapp.models.ehragent_clinical_domains import EHRAgentBlinks, VitalsInpatientMeasurement, EHRAgentClinicalDomainsProperties, EHRAgentCVCommonClinicalDomainsProperties
from dbmconfigapp.models.agentpp_hosted_app import AgentppHostedApp, LauncherGeneralProperties
from dbmconfigapp.widgets import Sortable
from django.forms.utils import ErrorList
from dbmconfigapp.models import vpo
from django.forms.widgets import CheckboxSelectMultiple
from dbmconfigapp.models.base import SEARCH_OPTIONS_CHOICES
                                     
                   
class EHRAgentBlinksInlineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(EHRAgentBlinksInlineForm, self).__init__(*args, **kwargs)
        
        self.fields['admission_interval'].required = False
        self.fields['admission_inpatient_domains'].required = False
        
    def clean(self):
        cleaned_data = super(EHRAgentBlinksInlineForm, self).clean()
         
       
        return cleaned_data
    
    class Meta:
        model = EHRAgentBlinks
        fields = '__all__'       
           
        
class VpoEhrAgentDomainsInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VpoEhrAgentDomainsInlineForm, self).__init__(*args, **kwargs)
        
        if 'filter_type' in self.fields:
            self.fields['filter_type'].required = False
        
        if self.instance.clinical_domain_id == 18:
            # Clinical Documents
            self.fields['filter_codes'].label = 'Filter out Clinical Documents types'
            self.fields['filter_codes'].help_text = get_help_text('Defines the document types ' + vpo.CODE_SYSTEM_FORMAT_TEMPLATE + ' that are filtered out of Clinical Documents. This configuration is mainly used to exclude Collaborate-bound e-Referrals from the clinical view, but it can also be used to filter out Imaging acts.<br/>This configuration applies to Clinical Viewer, EHR Agent and Patient View.', 'empty')
        elif self.instance.clinical_domain_id == 3:
            # Diagnosis
            self.fields['filter_codes'].label = 'Filter out Diagnosis types'
            self.fields['filter_codes'].help_text = get_help_text("""
                This configuration defines the baseline code(s) (in codeSystem|Code format) for the Diagnosis Type(s) that you want to filter out of the clinical applications (in the Diagnoses view and in EHR Agent Clinical History reports). 
                The default value is used to filter out the DRG (Diagnosis-Related Group) that provides billing information, which is generally not relevant in a clinical report.<br/>
                Note: DRG is a system for classifying hospital cases into one of originally 467 groups. It does not add clinical relevance for Diagnoses. The information is however stored in the CDR to be used for analytics purposes.<br/>
                This configuration applies to Clinical Viewer, EHR Agent and Patient View.
                """, '2.16.840.1.113883.3.57.1.2.17.87|DRG')
        elif self.instance.clinical_domain_id == 6:
            # Medications
            self.fields['filter_codes'].label = 'Filter out Medications Mood codes'
            self.fields['filter_codes'].help_text = get_help_text('Defines the Mood code used to filter out (not display) Medications from the Medications clinical view, Medications Grid in the Summary Page and Medications Grid in the Diabetes clinical view ' + vpo.CODE_SYSTEM_FORMAT_TEMPLATE + '.<br/>This configuration applies to Clinical Viewer, EHR Agent and Patient View.', '2.16.840.1.113883.3.57.1.2.17.82|ADMSTRD^')
            
        elif self.instance.clinical_domain_id == 11:
            # Procedures
            self.fields['filter_codes'].label = 'Filter Procedure codes'
            self.fields['filter_codes'].help_text = get_help_text('Defines the Type code used to filter out (not display) or filter in (display only) Procedure types from the Procedures domain in EHR Agent and Patient View ' + vpo.CODE_SYSTEM_FORMAT_TEMPLATE, 'empty')        
      
class VitalsInpatientMeasurementForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(VitalsInpatientMeasurementForm, self).__init__(*args, **kwargs)
        

    def clean(self):
        cleaned_data = super(VitalsInpatientMeasurementForm, self).clean()
         
       
        return cleaned_data

    class Meta:
        model = VitalsInpatientMeasurement
        fields = '__all__'
        
class EHRAgentClinicalDomainInlineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(EHRAgentClinicalDomainInlineForm, self).__init__(*args, **kwargs)

        self.fields['attention_searching_time'].required = False

    def clean(self):
        cleaned_data = super(EHRAgentClinicalDomainInlineForm, self).clean()
        return cleaned_data

    class Meta:
        model = EHRAgentClinicalDomainsProperties
        fields = '__all__'

class EHRAgentCommonClinicalDomainInlineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(EHRAgentCommonClinicalDomainInlineForm, self).__init__(*args, **kwargs)

        self.fields['default_searching_time'].required = False
        self.fields['default_searching_option'].choices = SEARCH_OPTIONS_CHOICES

    def clean(self):
        cleaned_data = super(EHRAgentCommonClinicalDomainInlineForm, self).clean()
        return cleaned_data

    class Meta:
        model = EHRAgentCVCommonClinicalDomainsProperties
        fields = '__all__'


#######################
# Here we verify that the selected default application in neither:
# 1. Disabled (unchecked enabled)                   
# 2. Deleted (marked for deletion)
# NOTE: Since the application data is changed in another model that is processed earlier, we use the global variable _hosted_apps_formset_instance
class LauncherGeneralPropertiesForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(LauncherGeneralPropertiesForm, self).clean()

        global _hosted_apps_formset_instance

        # get the corresponding hosted app record (instead of for loop)
        def_app_data = next((f.cleaned_data for f in _hosted_apps_formset_instance.forms if f.cleaned_data['id'] == cleaned_data['default_app']), None)
        
        if def_app_data:
            if def_app_data.get('DELETE'):
                self._errors['default_app'] = ErrorList([u'The selected default application is marked for deletion. Please change the default application or uncheck the Delete checkbox.'])
            elif not def_app_data.get('enabled'):
                self._errors['default_app'] = ErrorList([u'The selected default application must be an enabled application.'])

        return cleaned_data


_hosted_apps_formset_instance = None

############################
# Here we only need to make sure the _hosted_apps_formset_instance value is set
#   so it can be checked against in LauncherGeneralPropertiesForm
class AgentppHostedAppInlineFormset(BaseInlineFormSet):

    def clean(self):
        super(AgentppHostedAppInlineFormset, self).clean()

        global _hosted_apps_formset_instance
        _hosted_apps_formset_instance = self

        
    

