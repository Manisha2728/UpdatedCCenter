from django.contrib import admin

from dbmconfigapp.models.document_search_bootstrap import DocumentSearchBootstrap,DocumentSearchBootstrapProperties
from .dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline

class DocumentSearchBootstrapInline(dbmBaseAdminStackedInline):
    model = DocumentSearchBootstrapProperties
    fieldsets = [              
        ('Indexing process time frame',{'fields': ['frequency_mode','start_scheduled_time','end_scheduled_time']}),
		('Systems with protected index rate',{
		'fields': ['protected_systems_rate1','protected_systems1', 'protected_systems_rate2','protected_systems2']
		}),
        ('Unprotected index rate',{
		'fields': ['unprotected_systems_rate']
		})
        ]
    

class DocumentSearchBootstrapAdmin(dbmModelAdmin):
    model = DocumentSearchBootstrap
    inlines = (DocumentSearchBootstrapInline, )
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'services')
    
    
    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
        js = ['admin/js/dbmconfigapp/document_search_bootstrap.js']
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False