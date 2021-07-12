from django.contrib import admin

from dbmconfigapp.models.document_search_general import DocumentSearchGeneral,DocumentSearchGeneralProperties
from .dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline

class DocumentSearchGeneralInline(dbmBaseAdminStackedInline):
    model = DocumentSearchGeneralProperties
    fieldsets = [ 
        ('Search of CDR clinical documents',{
		'fields': ['is_ds_of_cdr_enabled', 'content_free_systems_mode', 'content_free_systems', 'index_free_systems']
		}),
        ('Search of External clinical documents',{
		'fields': [ 'is_ds_of_external_enabled']
		})
        ]
    

class DocumentSearchGeneralAdmin(dbmModelAdmin):
    model = DocumentSearchGeneral
    inlines = (DocumentSearchGeneralInline, )
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'services')
    
    
    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
        js = ['admin/js/dbmconfigapp/document_search_general.js']
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False