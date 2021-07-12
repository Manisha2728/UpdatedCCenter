from django.contrib.admin.options import ModelAdmin
from dbmconfigapp.models.tracking import ChangesHistory, LoginsHistory
from django.http import HttpResponse
from django.utils.encoding import smart_str
from authccenter.utils import get_user_name, get_user_to_dispay

class BaseHistoryAdmin(ModelAdmin):
    
    list_display_links = None
    list_filter = ['action_time']
    ordering = ('-action_time',)
    list_per_page = 20
    list_max_show_all = list_per_page  # should be <= list_per_page to hide "Show All" 
    actions = ['export_csv',]

    def user_to_dispay(self, obj):
        return get_user_to_dispay(obj)
    user_to_dispay.short_description = 'Domain\\UserID'

    def user_name(self, obj):
        return get_user_name(obj)
    user_name.short_description = 'User Name'

    def override_title(self, request, title, extra_context=None):
        changelist = super(BaseHistoryAdmin, self).changelist_view(request, extra_context)
        if hasattr(changelist, 'context_data'): 
            changelist.context_data['title'] = title
        return changelist

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(BaseHistoryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def export_csv(self, request, queryset):
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + self.get_export_file_name()
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        self.write_to_csv_file(writer, queryset)

        return response
    export_csv.short_description = u"Export CSV"

    def get_export_file_name(self):
        return 'history.csv'

    def format_action_time_for_export(self, action_time):
        #from django.utils.timezone import localtime

        date_format = '%b. %d, %Y, %I:%M:%S %p'
        return action_time.strftime(date_format) 

    def write_to_csv_file(self, writer, queryset):
        return

    class Meta:
        tracking = True

class ChangesHistoryAdmin(BaseHistoryAdmin):
    model = ChangesHistory

    list_display = ('content_type', 'model_name', 'action_time','user_to_dispay', 'user_name', 'change_message')
    search_fields = ('change_message', 'content_type__name', 'content_type__model')

    def changelist_view(self, request, extra_context=None):
        return self.override_title(request, 'Changes History', extra_context)

    def write_to_csv_file(self, writer, queryset):
        writer.writerow([
            smart_str(u'Screen'),
            smart_str(u'Page Model Name'),
            smart_str(u'Date/Time'),
            smart_str(u'Domain\\UserID'),
            smart_str(u'User Name'),
            smart_str(u'Action'),
        ])
        for row in queryset:
            writer.writerow([
                smart_str(row.content_type),
                smart_str(self.model_name(row)),
                smart_str(self.format_action_time_for_export(row.action_time)),
                smart_str(self.user_to_dispay(row)),
                smart_str(self.user_name(row)),
                smart_str(row.change_message),
            ])

    def get_export_file_name(self):
        return 'ChangesHistory.csv'

    def model_name(self, obj):
        if(obj.content_type == None):
            return None
        return obj.content_type.model
    model_name.short_description = 'Page Model Name'
    model_name.admin_order_field = 'content_type__model'

class LoginsHistoryAdmin(BaseHistoryAdmin):
    model = LoginsHistory
    
    list_display = ('action_time','user_to_dispay', 'user_name', 'action')

    def changelist_view(self, request, extra_context=None):
        return self.override_title(request, 'Logins/Logouts History', extra_context)

    def user_to_dispay(self, obj):
        user = super(LoginsHistoryAdmin, self).user_to_dispay(obj)
        if(user == None):
            return obj.login_name
        return user
    user_to_dispay.short_description = 'Domain\\UserID'

    def write_to_csv_file(self, writer, queryset):
        writer.writerow([
            smart_str(u'Date/Time'),
            smart_str(u'Domain\\UserID'),
            smart_str(u'User Name'),
            smart_str(u'Action'),
        ])
        for row in queryset:
            writer.writerow([
                smart_str(self.format_action_time_for_export(row.action_time)),
                smart_str(self.user_to_dispay(row)),
                smart_str(self.user_name(row)),
                smart_str(row.action),
            ])

    def get_export_file_name(self):
        return 'LoginsHistory.csv'


