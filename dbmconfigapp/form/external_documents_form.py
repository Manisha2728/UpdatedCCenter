from django import forms
from dbmconfigapp import widgets
from django.forms.utils import ErrorList
import os.path


class ExternalDocumentMyEHRConnectivityForm(forms.ModelForm):    
    def clean(self):
        cleaned_data = super(ExternalDocumentMyEHRConnectivityForm, self).clean()
        pcehr_exist_url  = cleaned_data.get('pcehr_exist_url')
        gain_access_url  = cleaned_data.get('gain_access_url')
        get_document_list_url  = cleaned_data.get('get_document_list_url')
        get_document_url  = cleaned_data.get('get_document_url')
        my_hr_oid  = cleaned_data.get('my_hr_oid')
        enable_my_hr_flow  = cleaned_data.get('enable_my_hr_flow')
        iho_name = cleaned_data.get('iho_name')
        iho_thumbprint  = cleaned_data.get('iho_thumbprint')
        my_hr_node_id  = cleaned_data.get('my_hr_node_id')
        stylesheet  = cleaned_data.get('stylesheet')
        
        if(enable_my_hr_flow is True):
            if (pcehr_exist_url is None or pcehr_exist_url == ''):   
                self._errors['pcehr_exist_url'] = ErrorList([u'Value should not be empty.'])

            if (my_hr_node_id is None or my_hr_node_id == ''):   
                self._errors['my_hr_node_id'] = ErrorList([u'Value should not be empty.'])
                
            if (gain_access_url is None or gain_access_url == ''):   
                self._errors['gain_access_url'] = ErrorList([u'Value should not be empty.'])
                
            if (get_document_url is None or get_document_url == ''):   
                self._errors['get_document_url'] = ErrorList([u'Value should not be empty.'])
            
            if (get_document_list_url is None or get_document_list_url == ''):   
                self._errors['get_document_list_url'] = ErrorList([u'Value should not be empty.'])
                
            if (my_hr_oid is None or my_hr_oid == ''):   
                self._errors['my_hr_oid'] = ErrorList([u'Value should not be empty.'])

            if (stylesheet is None or stylesheet == ''):   
                self._errors['stylesheet'] = ErrorList([u'Value should not be empty.'])
            else:
                extension = os.path.splitext(stylesheet.name)[1]
                if (extension != '.xslt' and extension != '.xsl'):   
                    self._errors['stylesheet'] = ErrorList([u'File must be .xslt or .xsl'])                
                
        if (not(iho_name is None) and not(iho_name == '') and (iho_thumbprint is None or iho_thumbprint == '')): 
            self._errors['iho_thumbprint'] = ErrorList([u'Thumbprint value can not be empty.']) 
                           
        
        if(not(my_hr_node_id is None) and not(my_hr_node_id == '') and (my_hr_node_id>120 or my_hr_node_id < 101)):
            self._errors['my_hr_node_id'] = ErrorList([u'Node id value should be between 101-120.'])

            
        

       
        
        return cleaned_data     
        
    class Meta:
        widgets = {
            'pcehr_exist_url': forms.TextInput(attrs={'size':'90'}),
            'gain_access_url': forms.TextInput(attrs={'size':'90'}),
            'get_document_list_url': forms.TextInput(attrs={'size':'90'}),
            'get_document_url': forms.TextInput(attrs={'size':'90'}),
            'iho_thumbprint': forms.TextInput(attrs={'size':'70'}),
        }
