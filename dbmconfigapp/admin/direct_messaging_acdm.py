from django.contrib import admin

from dbmconfigapp.models.direct_messaging_acdm import DirectMessagingAcdm, DirectMessagingAcdmPage
from .dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline
from dbmconfigapp.forms import DirectMessagingAcdmInlineForm

class DirectMessagingAcdmInline(dbmBaseAdminStackedInline):
    model = DirectMessagingAcdm
    form = DirectMessagingAcdmInlineForm
    fieldsets = [              
        ('Sending/Receiving TOC via ACDM',{'fields': ['clientOid', 'acdmCommunityName']})
        ]

class DirectMessagingAcdmAdmin(dbmModelAdmin):
    model = DirectMessagingAcdmPage
    inlines = (DirectMessagingAcdmInline, )
    
    class Media:
        css = { "all" : ("admin/css/hide_admin_original.css",) }
        js = ['admin/js/direct-messaging.js'] 
    