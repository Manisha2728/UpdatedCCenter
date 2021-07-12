# -*- coding: utf-8 -*-
from django import forms
from .models import InitiateConnection, AuthoritySystems, dbMotionSystem, InitiateMappings
from dbmconfigapp.models.base import *
from dbmconfigapp.forms import *
from .models import HMO_CHOICES
from django.forms.widgets import HiddenInput

class ViaAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ViaAdminForm, self).__init__(*args, **kwargs)
        self.fields['empi_type'].required = False
        
    def clean(self):
        cleaned_data = super(ViaAdminForm, self).clean()
        hmoid = cleaned_data.get('hmo_id', None)
        cleaned_data['hmo_name'] = dict(HMO_CHOICES)[hmoid].decode('utf-8') if hmoid else ''
              
        return cleaned_data    
class InitiateAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InitiateAdminForm, self).__init__(*args, **kwargs)
        self.fields['empi_url_address_for_patient_identity_feed_v3'].required = False
        

class DbmotionSystemsForm (BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(DbmotionSystemsForm, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['dbmotion_system_node_id'].widget.can_add_related = False
    class Meta:
        model = dbMotionSystem
        

class AuthoritySystemsForm (BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(AuthoritySystemsForm, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['dbmotion_node_id'].widget.can_add_related = False
    def clean(self):
        super(AuthoritySystemsForm, self).clean()
        
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            
            segment_name = data.get('segment_name')
            attribute_code = data.get('attribute_code')
            if form.is_valid() and segment_name != None and segment_name != "" and segment_name!="[empty value]":
                if attribute_code == None or attribute_code == "":
                    form._errors['attribute_code'] = ErrorList([u"Fill in the Attribute Code."])
                    #raise forms.ValidationError("Attribute Code is required if Segment Name is selected!")
    
    class Meta:
        model = AuthoritySystems


class MappingsForm (BaseInlineFormSet):
    def clean(self):
        super(MappingsForm, self).clean()
        
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            
            attribute_input = data.get('dbmotion_attribute_input')
            attribute_weight = data.get('dbmotion_attribute_weight')
            if form.is_valid() and attribute_input != None and attribute_input == True:
                if attribute_weight == None or attribute_weight == "":
                    form._errors['dbmotion_attribute_weight'] = ErrorList([u"dbMotion VIA Attribute Weight is required if dbMotion VIA Attribute Input is checked"])
                    #raise forms.ValidationError("Attribute Code is required if Segment Name is selected!")
    
    class Meta:
        model = InitiateMappings        
        
class InitiateConnectionForm(forms.ModelForm):
    patient_credential_password = forms.CharField(label='VIA User Credentials: Password',widget=forms.PasswordInput(render_value=True), help_text=get_help_text('VIA connections/operations with the MPI (for example, Patient Search, Match, Insert, Remove) require User credentials with a Password, which must be provided by the MPI service to replace the default value.'))
    
    class Meta:
        model = InitiateConnection
        fields = '__all__'

        widgets = {
            'initiate_url': forms.TextInput(attrs={'size':'100'}),
            'patient_credential_username': forms.TextInput(attrs={'size':'20'}),
   }