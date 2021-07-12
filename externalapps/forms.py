from django import forms
from django.forms.utils import ErrorList
from .models import Instance

class EhrAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EhrAdminForm, self).__init__(*args, **kwargs)
        self.fields['deployment_type'].required = False
        self.fields['position_app_corner'].required = False
        self.fields['position_agent_corner'].required = False
        
    
class InstanceAdminForm(forms.ModelForm):

    password_fld = Instance._meta.get_field('mu_reporting_password')
    mu_reporting_password = forms.CharField(required=False , label=password_fld.verbose_name,widget=forms.PasswordInput(render_value=True), help_text=password_fld.help_text)

    def __init__(self, *args, **kwargs):
        super(InstanceAdminForm, self).__init__(*args, **kwargs)
        self.fields['context_type'].required = False
        self.fields['ehr'].widget.can_add_related = False
    
    def clean(self):
        cleaned_data = super(InstanceAdminForm, self).clean()
         
        if self.changed_data:
            # If Non-CCOW is selected, then 'interceptor_type' must be provided 
            if cleaned_data.get('context_type') == 'NonCcow':
                if not cleaned_data.get('interceptor_type', None):
                    self._errors['interceptor_type'] = ErrorList([u"This field is required (when Non-CCOW is selected)."])
                    
            if cleaned_data.get('facility_root'):
                if not cleaned_data.get('facility_extension', None):
                    self._errors['facility_extension'] = ErrorList([u"This field is required (when Facility ID Root is not empty)."])
                    
            if cleaned_data.get('facility_extension'):
                if not cleaned_data.get('facility_root', None):
                    self._errors['facility_root'] = ErrorList([u"This field is required (when Facility ID Extension is not empty)."])
           
        return cleaned_data

class DirectAddressEndpointsAdminForm(forms.ModelForm):
    password_fld = Instance._meta.get_field('mu_reporting_password')
    mu_reporting_password = forms.CharField(required=False , label=password_fld.verbose_name,widget=forms.PasswordInput(render_value=True), help_text=password_fld.help_text)

class ParticpantInlineForm(forms.ModelForm):
    type = forms.HiddenInput()
    
    
class InstancePropertiesAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstancePropertiesAdminForm, self).__init__(*args, **kwargs)
        self.fields['app_id'].widget.can_edit_related = True
        self.fields['patient_assigning_Authority_for_Display'].widget =  forms.TextInput(attrs={'size':'100'})
class UserContextInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserContextInlineForm, self).__init__(*args, **kwargs)
        self.fields['user_context_type'].required = False


    