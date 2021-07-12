from django import forms
from dbmconfigapp import widgets

class NumberAndChoicesField(forms.MultiValueField):
    
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        fields = (
            forms.IntegerField(**kwargs),
            forms.ChoiceField(choices=choices),
                  )
        if 'min_value' in kwargs: kwargs.pop('min_value')
        super(NumberAndChoicesField, self).__init__(fields=fields, *args, **kwargs)
        
        self.widget = widgets.TextAndSelectWidget(choices=choices)
        
    def compress(self, data_list):
        if data_list:
            return '|'.join(str(x) for x in data_list)
          
        return None
    
    
