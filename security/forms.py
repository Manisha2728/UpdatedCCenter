from django import forms
from .models import *
from dbmconfigapp.models.base import *
from dbmconfigapp.forms import *

class ADProvidersForm(forms.ModelForm):
    ad_pass_fld = ADProviders._meta.get_field('untrusted_ad_user_password')
    untrusted_ad_user_password = forms.CharField(required=False , label=ad_pass_fld.verbose_name,widget=forms.PasswordInput(render_value=True), help_text=ad_pass_fld.help_text)
    def clean(self):
        super(ADProvidersForm, self).clean()
        if not hasattr(self, 'cleaned_data'):
            return
        data = self.cleaned_data
        if hasattr(self,'changed_data'):
            if 'domain_id' in self.changed_data:
                if data.get('domain_id') != self.instance.domain_id:
                    allow_delete = self.instance.has_constraints()
                    if (allow_delete != "can_delete"):
                        self._errors['domain_id'] = ErrorList([u'ID: %d has users assigned and can not be changed, please delete all assigned users to this active directory in "dbMotion Security Management" in order to change the ID' %(self.instance.domain_id)])
                
                if data.get('domain_id') > 255 or data.get('domain_id') < 1:
                    self._errors['domain_id'] = ErrorList([u'Value must be within the range: "1-255"'])
            
        attribute_untrusted_ad = data.get('untrusted_ad')
        attribute_user = data.get('untrusted_ad_user_name')
        attribute_password = data.get('untrusted_ad_user_password')
        if self.is_valid() and attribute_untrusted_ad != None and attribute_untrusted_ad == True:
            if attribute_user == None or attribute_user == "":
                self._errors['untrusted_ad_user_name'] = ErrorList([u"Untrusted AD User Name is required if Untrusted Active Directory is checked"])
            if attribute_password == None or attribute_password == "":
                self._errors['untrusted_ad_user_password'] = ErrorList([u"Untrusted AD User Password is required if Untrusted Active Directory is checked"])
                
        return data
    
    class Meta:
        model = ADProviders
        fields = '__all__'

class RoleMappingForm (BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RoleMappingForm, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['internal_role_name'].widget.can_add_related = True
    class Meta:
        model = RoleMapping        
        