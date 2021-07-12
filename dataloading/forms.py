from django import forms
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError


        
class DataLoadingPartitioningForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(DataLoadingPartitioningForm, self).clean()
        days = cleaned_data.get('history_depth')
        if days is not None:
            if days < 90:
                self._errors['history_depth'] = ErrorList([u'DELETION value must be greater than or equal to 90 days.'])
        return cleaned_data    
    
    
class BatchLoadingSchedulerForm(forms.ModelForm): 
    def clean(self):
        cleaned_data = super(BatchLoadingSchedulerForm, self).clean()
        duration_value  = cleaned_data.get('duration_value')
        duration_unit  = cleaned_data.get('duration_unit')       
        arc_folder  = cleaned_data.get('arc_folder')
        if duration_value is None or duration_value<1:   
            self._errors['duration_value'] = ErrorList([u'Value must be initialized or bigger then 0.'])
        elif (duration_value>24 and duration_unit == 'H') or (duration_value>1440 and duration_unit == 'M'):
            self._errors['duration_value'] = ErrorList([u'Value out of bounds.'])
        
        if arc_folder is None or len(arc_folder)<1:   
            self._errors['arc_folder'] = ErrorList([u'Value must be initialized.'])  
       
        return cleaned_data     
    
    class Meta:
        widgets = {
            'arc_folder': forms.TextInput(attrs={'size':'60'}),
        }
        
        
        
class BatchLoadingSchedulerInFolderForm(forms.ModelForm):        
    class Meta:
        widgets = {
            'in_folder': forms.TextInput(attrs={'size':'70'}),
        }