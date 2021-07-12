from dbmconfigapp.models.capsule import *
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdmin, dbmBaseAdminStackedInline



class CapsuleServiceInline(dbmBaseAdminStackedInline):
    model = CapsuleService    
    fieldsets = (
                ('Capsule Type', {
                 'fields': ['capsule_type'], 'classes': ['wide', 'extrapretty']
                 }),
                 (model._meta.history_meta_label, {
                 'fields': ['scheduled_time', 'end_scheduled_time', 'local_folder', 
                            'vault_folder', 'on_demand_local_folder', 'on_demand_vault_folder', 'outbound_csv_vault_folder', 'inbound_csv_vault_folder', 'num_of_days_to_delete_capsules', 'capsules_paging_size', 'confidentiality_filter'], 'classes': ['wide', 'extrapretty']
                 }),
                 ) 


class CapsuleAdmin(dbmModelAdmin):
    model = CapsulePage
    inlines = (CapsuleServiceInline,)
    class Media:        
        js = ['admin/js/dbmconfigapp/capsule.js']
    def __init__(self, *args, **kwargs):
        super(CapsuleAdmin, self).__init__(*args, **kwargs)    