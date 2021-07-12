from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline
from dbmconfigapp.models.operational_manager import SSRS_COFIG_FILE, OperationalManagerPage, UsageReports, DataAccessAuditingPage, DataAccessAuditing, CAGDataAccessAuditingPage,CAGDataAccessAuditing
from dbmconfigapp.forms import OperationalManagerInlineForm, DataAccessAuditingForm
from configcenter.settings import get_param


# Usage Reports page
class UsageReportsInline(dbmBaseAdminStackedInline):
    model = UsageReports
    template = 'admin/edit_inline/stacked-operational_manager.html'
    form = OperationalManagerInlineForm
    fieldsets = (
                 (model._meta.history_meta_label, {
                 'fields': ['smtp_url', 'smtp_port', 'from_address']
                    , 'description' : "The User should have writing permissions to the following file <b>on the Reporting Server:</b> %s" % SSRS_COFIG_FILE
                 }),
                 ("HiddenSection", {
                 'fields': ['status', 'message']
                 }),
                 ) 

class OperationalManagerAdmin(dbmModelAdmin):
    model = OperationalManagerPage
    inlines = (UsageReportsInline, ) 
    exclude = ('page_help_text', 'page_name', 'services')


# Data Access Auditing page     
class DataAccessAuditingInline(dbmBaseAdminStackedInline):
    model = DataAccessAuditing
    form = DataAccessAuditingForm

    template = 'admin/edit_inline/stacked_data_access_auditing.html'

    fieldsets = (
                 ("Enable database access auditing", {
                 'fields': ['auditing_type']
                 }),
                 ("Auditing files location and maximum storage limit", {
                 'fields': ['suspected_max_storage_size']
                    , 'description' : "Auditing files are located on the disk path specified in the system parameters -\%s" % get_param("sql_server_audit_path")
                 }),
                 ("",{
                 'fields': ['authorized_max_storage_size']
                 }),
                 ("Authorired Users", {
                 'fields': ['server_principals']
                 }),
                 ) 

class CAGDataAccessAuditingInline(dbmBaseAdminStackedInline):
    model = CAGDataAccessAuditing
    form = DataAccessAuditingForm

    template = 'admin/edit_inline/stacked_data_access_auditing.html'

    fieldsets = (
                 ("Enable database access auditing", {
                 'fields': ['auditing_type']
                 }),
                 ("Auditing files location and maximum storage limit", {
                 'fields': ['suspected_max_storage_size']
                    , 'description' : "Auditing files are located on the disk path specified in the system parameters - \%s" % get_param("sql_server_audit_path")
                 }),
                 ("",{
                 'fields': ['authorized_max_storage_size']
                 }),
                 ("Authorired Users", {
                 'fields': ['server_principals']
                 }),
                 ) 

class DataAccessAuditingAdmin(dbmModelAdmin):
    model = DataAccessAuditingPage
    inlines = (DataAccessAuditingInline, ) 

    exclude = ('page_help_text', 'page_name', 'services')

    class Media:
        js = ['admin/js/dbmconfigapp/data_access_auditing.js']  


class CAGDataAccessAuditingAdmin(dbmModelAdmin):
    model = CAGDataAccessAuditingPage
    inlines = (CAGDataAccessAuditingInline, ) 

    exclude = ('page_help_text', 'page_name', 'services')

    class Media:
        js = ['admin/js/dbmconfigapp/cag_data_access_auditing.js']      
    
    
    