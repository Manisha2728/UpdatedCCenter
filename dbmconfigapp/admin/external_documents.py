'''
Created on 28.12.2017
@author: Ran Tayeb
'''
from dbmconfigapp.models.external_documents import MyHRConnectivityEntity, MyHROrganizationsEntity, MyHRConnectivityPage
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline, dbmBaseAdminTabularInline
from dbmconfigapp.form.external_documents_form import ExternalDocumentMyEHRConnectivityForm
from django.contrib import admin

from imaplib import Response_code


class MyHRConnectivityInline(dbmBaseAdminStackedInline):
    model = MyHRConnectivityEntity
    fieldsets = (
        (model._meta.history_meta_label, {
            'fields': ('enable_my_hr_flow', 'my_hr_oid', 'my_hr_node_id', 'pcehr_exist_url', 'gain_access_url', 'get_document_list_url', 'get_document_url','stylesheet',), 'classes': ['wide', 'extrapretty']}),
    )
    form = ExternalDocumentMyEHRConnectivityForm
    
    
class ThumbprintTabularInline(dbmBaseAdminTabularInline):
    model = MyHROrganizationsEntity
    fieldsets = (
        (model._meta.history_meta_label, {
            'fields': ('iho_name', 'iho_thumbprint','org_name',), 'classes': ['wide', 'extrapretty']}),
    )
    extra = 1
    form = ExternalDocumentMyEHRConnectivityForm
    
class MyHRConnectivityAdmin(dbmModelAdmin):
    model = MyHRConnectivityPage
    #change_form_template = 'admin/dataloading/change_form.html'
    inlines = (MyHRConnectivityInline,ThumbprintTabularInline,)
    exclude = ('page_help_text', 'page_name', 'services', 'components')


    class Media:
        js = ['admin/js/dbmconfigapp/external_documents.js'] 
        
            
    class Meta:
        tree_id = 'external_documents_my_hr'



