from django.contrib import admin, messages
from dbmconfigapp.admin.dbm_ModelAdmin import dbmModelAdminSaveOnly, dbmBaseAdminStackedInline , get_grid_help_text, dbmBaseAdminTabularInline
from .models import *
from .forms import *
from imaplib import Response_code


            ##### Partitioning #####
            
            
            ##### Partitioning Inlines #####

class PartitioningInline(dbmBaseAdminStackedInline):
    model = Partitioning
    fieldsets = (
        (model._meta.history_meta_label, {
            'fields': ('history_depth',), 'classes': ['wide', 'extrapretty']}),
    )
    form = DataLoadingPartitioningForm

    
    
            #### Partitioning Page ####

class PartitioningAdmin(dbmModelAdminSaveOnly):
    model = PartitioningPage
    change_form_template = 'admin/dataloading/change_form.html'
    inlines = (PartitioningInline,)
    exclude = ('page_help_text', 'page_name', 'services', 'components')
    
    
    class Meta:
        show_partition_warning = True
        tree_id = 'data_loading_app'
    





            ##### Batch Loading #####
            
            ##### Batch Loading Inlines #####           
class BatchLoadingSchedulerInline(dbmBaseAdminStackedInline):
    model = BatchLoadingScheduler
    fieldsets = [
                  ("Batch Loading Scheduler Settings", {'fields': ('enable', ('start_boundary_time', 'duration_value', 'duration_unit'), 'interval_value', 'arc_folder')}),
                  ]
    # fields          = ('enable', ('start_boundary_time', 'duration_value', 'duration_unit'), 'interval_value', 'arc_folder')
    form = BatchLoadingSchedulerForm
    
    
class BatchLoadingSchedulerInPathInline(dbmBaseAdminTabularInline):
    model = BatchLoadingSchedulerInPath
    verbose_name_plural = 'Folder(s) from which the CSV files are loaded'
    # formset  = DbmotionSystemsForm
    fields = ('in_folder',)
    extra = 1
    form = BatchLoadingSchedulerInFolderForm
       

    

            #### BatchLoading Page ####

class BatchLoadingAdmin(dbmModelAdminSaveOnly):
    model = BatchLoadingPage
    change_form_template = 'admin/dataloading/change_form.html'
    inlines = (BatchLoadingSchedulerInline, BatchLoadingSchedulerInPathInline,)
    exclude = ('page_help_text', 'page_name', 'services', 'components')
    
    
    class Meta:
        show_batch_loading_note = True
        tree_id = 'data_loading_batch'
    

    
    
    
        
admin.site.register(PartitioningPage, PartitioningAdmin)
admin.site.register(BatchLoadingPage, BatchLoadingAdmin)

