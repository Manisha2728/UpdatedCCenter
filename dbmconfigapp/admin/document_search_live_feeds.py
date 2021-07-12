from django.contrib import admin

from dbmconfigapp.models.document_search_live_feeds import DocumentSearchLiveFeeds,DocumentSearchLiveFeedsProperties
from .dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline

class DocumentSearchLiveFeedsInline(dbmBaseAdminStackedInline):
    model = DocumentSearchLiveFeedsProperties
    fieldsets = [              
        ('Indexing process time frame',{
		'fields': ['frequency_mode','start_scheduled_time','end_scheduled_time']
		}),
        ('Systems with protected index rate',{
		'fields': ['protected_systems_rate1','protected_systems1', 'protected_systems_rate2','protected_systems2']
		}),
        ('Systems with standard index rate',{
		'fields': ['unprotected_systems_rate']
		})
        ]
    

class DocumentSearchLiveFeedsAdmin(dbmModelAdmin):
    model = DocumentSearchLiveFeeds
    inlines = (DocumentSearchLiveFeedsInline, )
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'services')
    
    
    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
        js = ['admin/js/dbmconfigapp/document_search_live_feeds.js']
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False