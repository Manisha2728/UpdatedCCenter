from django.contrib import admin
from dbmconfigapp.models.ehragent import *
from dbmconfigapp.models.agent_general_page import *
from .dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline, dbmBaseAdminTabularInline
from dbmconfigapp.models.culture import Culture, CurrentCulture
from dbmconfigapp.models.agentpp_hosted_app import *


class EhrAgentBaseUrlline(dbmBaseAdminStackedInline):
    model = EhrAgentBaseUrl
    section_name = 'URL Definitions'
    fieldsets = [
        (section_name, {'fields': ['base_url']}),
              ]
class CultureAdminForm(forms.ModelForm):   
    name = forms.ModelChoiceField(queryset=Culture.objects.all(),empty_label=None)
   
    def __init__(self, *args, **kwargs):
        super(CultureAdminForm, self).__init__(*args, **kwargs)
        self.fields["name"].help_text = 'Define the default language for application User Interfaces.<br/>Default: en-US.'

class CultureGeneralInline(dbmBaseAdminStackedInline):
    form = CultureAdminForm
    model = CurrentCulture
    section_name = 'User Interface Language'
    fieldsets = [
                 (section_name, {'fields': ['name'], 'classes': ['module', 'aligned', 'wide', 'extrapretty']}),
                ]

class LangsForm(forms.ModelForm):   
    name = forms.TextInput()
   
    def __init__(self, *args, **kwargs):
        super(LangsForm, self).__init__(*args, **kwargs)
        
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['name'].required = False
            self.fields['name'].widget.attrs['disabled'] = 'disabled'

class LangsInline(dbmBaseAdminTabularInline):
    form = LangsForm
    model = Culture
    fields = ('name',)
    extra = 1
    verbose_name_plural = model._meta.history_meta_label
        
    def queryset(self, request):
        return super(LangsInline, self).queryset(request).filter(readonly=0)
        
    def has_add_permission(self, request):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def get_readonly_fields(self, request, obj = None):
        return ()

class AgentHubGeneralAdmin(dbmModelAdmin):
    model = AgentHubGeneralPage
    inlines =  (EhrAgentBaseUrlline,CultureGeneralInline,LangsInline)

   

