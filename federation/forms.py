from django import forms
from federation.models import Node, Group
from django.forms.utils import ErrorList
from dbmconfigapp.models import SystemParameters

class NodeAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NodeAdminForm, self).__init__(*args, **kwargs)
        self.fields['ppol_provider_node'].widget.can_add_related = False 
        self.fields['ppol_provider_node'].required = (Node.objects.count() > 0)
        

        self.fields['request_from'].widget.can_edit_related = True
        self.fields['response_to'].widget.can_edit_related = True
        
        self.fields['request_from'].required = False     
        self.fields['response_to'].required = False
    
    def clean(self):
        cleaned_data = super(NodeAdminForm, self).clean()
        
        if Node.objects.count() > 0:
            if not cleaned_data.get('ppol_provider_node', None):
                self._errors['ppol_provider_node'] = ErrorList([u"This field is required."])
        
        return self.cleaned_data
    
    def save(self, force_insert=False, force_update=False, commit=True):
        node = super(NodeAdminForm, self).save(commit=False)
        # If ppol provider is None it means this is a new node - set it to itself
        if not node.ppol_provider_node:
            node.save()
            node.ppol_provider_node = node
            
        return node

class GroupAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        self.fields['node'].widget.can_add_related = False
        
          
    class Meta:       
        widgets = {
                'node': forms.SelectMultiple(attrs={'size': 10})
            }
        
    