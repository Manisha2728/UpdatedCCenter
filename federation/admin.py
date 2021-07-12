from django.contrib import admin, messages
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdminSaveOnly, dbmBaseModelAdmin, ServicesToRestart, dbmBaseAdminTabularInline, dbmModelAdmin, dbmBaseAdminStackedInline
from .models import *
from .forms import *
from configcenter.settings import get_param
import xml.etree.ElementTree as ET
from datetime import datetime

from django.core.exceptions import PermissionDenied, ValidationError

class NodeAdmin(dbmModelAdminSaveOnly):
    model = Node
    list_display = ('uid', 'name', 'application_server', 'request_from', 'response_to', 'ppol_provider_node', 'pl_active', 'pas_option_remote', 'is_local')
    
    list_display_links = ('uid', 'name')
    #list_editable = ('enabled',)
    form = NodeAdminForm
    ordering = ('uid',)
    actions = ['delete_nodes']
    fieldsets = (
        ('Node Details', {
            'fields': ('uid', 'name', 'application_server', 'request_from', 'response_to', 'pl_active', 'ppol_provider_node','node_confidentiality_level', 'is_available_during_document_search'), 'classes': ['wide', 'extrapretty']}),
        ('Patient Authorization', {
            'fields': ('pas_option_remote',), 'classes': ['wide', 'extrapretty']}),
    )
    radio_fields = {'pas_option_remote': admin.VERTICAL}
       
    def has_add_permission(self, request, obj=None):
        return True
    
    def get_actions(self, request):
        actions = super(NodeAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_nodes(self, request, queryset):
        for node in queryset:
            allow_delete, msg = node.can_delete()
            if allow_delete:
                node.delete()
                self.log_deletion(request, node, None)
                self.message_user(request, node.name + ' was deleted successfully.', messages.SUCCESS)
            else:
                self.message_user(request, msg, messages.ERROR)

    delete_nodes.short_description = "Delete Federation Node"
            
    class Meta:
        tree_id = 'federation_app_node'
    class Media:
        js = ['admin/js/federation/node.js']
        

       
    
class GroupAdmin(dbmBaseModelAdmin):
    model = Group
    form = GroupAdminForm
    fieldsets = [(model._meta.history_meta_label, 
                 {'fields': ('name', 'node'), 'classes': ['wide', ]}),]
       
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = ('_popup' in request.GET)
        extra_context['show_delete_link'] = False
        extra_context['show_save_as_new'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(dbmBaseModelAdmin, self).add_view(request, form_url, extra_context=extra_context)

admin.site.register(Node, NodeAdmin)
admin.site.register(Group, GroupAdmin)