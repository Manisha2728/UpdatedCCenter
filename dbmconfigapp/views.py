import mimetypes
from django.views.decorators.csrf import csrf_exempt
from dbmconfigapp.models.database_storage import DatabaseStorage
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from configcenter import settings
import time
import logging

from dbmconfigapp.models.tracking import ChangesHistory
from dbmconfigapp.utils import search
from dbmconfigapp.export_logic import get_export_db_data, import_db_from_file
from dbmconfigapp.forms import ImportFileAdminForm
from django.contrib.auth.decorators import login_required

"""
Override the error 500 page.
The original view is: django.views.defaults.server_error
"""
def handler500(request):
    request.session['url_back'] = 'javascript:history.back();'
    response = render(request, 'admin/500.html', {}, RequestContext(request))
    response.status_code = 500
    return response


def DbFiles (request, filename):
    # Read file from database
    storage = DatabaseStorage(settings.DBS_OPTIONS)
    image_file = storage.open(filename, 'rb')
    if not image_file:
        raise Http404
    file_content = image_file.read()

    # Prepare response
    content_type, content_encoding = mimetypes.guess_type(filename)
    response = HttpResponse(content=file_content, content_type=content_type)
    response['Content-Disposition'] = 'inline; filename=%s' % filename
    if content_encoding:
        response['Content-Encoding'] = content_encoding
    return response


# List of all the models we'd like to export.
@login_required()
def export_db(request):
    return render(request, 'admin/dbmconfigapp/export.html')



@csrf_exempt
def download_export_db(request):

    
    data = {}
    try:
        pages_list = request.POST['pages'].split(',')
    except:
        pages_list = []
        
    
        
    try:
        data = get_export_db_data(pages_list)
    except:
        request.session['error'] = 'An error occurred during the export process.'
        raise
    
    # This code returns a "file download" as the response.
    response = HttpResponse(data, 
                            content_type="application/json")
 
    filename = request.POST['file'] if 'file' in request.POST else time.strftime("%Y%m%d_%H%M_ccenter.json")        
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response




@login_required()
def welcome(request):
    # 'admin/index.html' is the default page. any requests such as admin/?next=page1 - will fall into this page
    # you can indicate a different page for Welcome and for fall-back.
    
# Uncomment the following rows for more debugging information
#     try: 
#         print(locals())
#         print(request.META['HTTP_REFERER'])
#     except:
#         print('no HTTP_REFERER')
    
    return render(request, 'admin/index.html', locals())

@login_required()
def post_import_db(request):
    import_error = not request.session['import_succeeded']

    if import_error:
        import_error_msg = str(request.session['import_error'])

    return render(request, 'admin/dbmconfigapp/post_import_db.html', locals())

@login_required()
def import_db(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ImportFileAdminForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            file = request.FILES['file']

            request.session['import_succeeded'] = True
            try:
                import_db_from_file(file, request)
            except Exception as e:
                request.session['import_succeeded'] = False
                request.session['import_error'] = e

            return HttpResponseRedirect('/post_import_db/') # Redirect after POST
    else:
        form = ImportFileAdminForm() # An unbound form

    return render(request, 'admin/dbmconfigapp/import.html', {
        'form': form,
    })

@login_required()
def history_since_last_login(request):
    last_login_date = request.user.last_login
    action_list = ChangesHistory.objects.filter(action_time__gte=last_login_date)

    return render(request, 'admin/changes_history.html', {
        'action_list': action_list,
        })

@login_required()
def history_per_page(request, object_id):
    action_list = ChangesHistory.objects.filter(object_id=object_id)

    return render(request, 'admin/changes_history.html', {
        'action_list': action_list,
        })
    
def search_init_view(request):
    
    search.save_pages_to_files(request.get_host())
    return HttpResponse('Search engine initialized successfully')


search_results = []

@login_required()
def search_results_view(request):
    global search_results
    
    return render(request, 'admin/search_results.html', {
        'page_list': search_results, 'search_string': request.session['search_string'], 'debug': settings.DEBUG
        })

    
    
@login_required()
def search_view(request):
    global search_results
    search_string = ''
    
    
    if 'search_string' in request.POST:
        search_string = request.POST['search_string']
        request.session['search_string'] = search_string
        search_results, errors = search.go(search_string)
        
        # TODO: sort results + handle errors                          
        #search_results.sort(cmp=None, key='name', reverse=False)
        
    return HttpResponseRedirect('/searchresults/') # Redirect after POST


from dbmconfigapp.management.commands.smart_migrate import MigrationHelper

def debug_view(request):
    general_info = {'version' : settings.VERSION, 'debug': settings.DEBUG, 'database': '%s.%s' % (settings.DATABASES['default']['HOST'], settings.DATABASES['default']['NAME'])}
    
    mh = MigrationHelper()
    
    return render(request, 'admin/debug.html', {
                
                'general_info' : general_info,
                'app_migrations': mh.apps_info.values(), 
        })
    
@login_required()
def apply_data_access_auditing(request):
    from dbmconfigapp.models.operational_manager import DataAccessAuditing
    from django.db import connections, connection, DatabaseError

    logger = logging.getLogger('django')
    err_msg_to_log = 'Exception occured when applying Data Access Auditing settings for CDR Instance'
    err_msg_sql = 'Could not Apply configuration. SQL server error occured. See dbMotion CCenter event log for details.'
    err_msg = 'Could not Apply configuration. See dbMotion CCenter event log for details.'

    try:
        auditing_row = DataAccessAuditing.objects.all()[0];
        with connections['default'].cursor() as cursor:
            cursor.callproc("ApplyDataAccessAuditingSettings", [auditing_row.auditing_type, auditing_row.suspected_max_storage_size, auditing_row.authorized_max_storage_size, auditing_row.server_principals])

        return HttpResponse('<span class="successmessage">The configuration was applied successfully.</span>')

    except DatabaseError as de:
        logger.error("{0}:\n{1}".format(err_msg_to_log, de))
        return HttpResponse('<span class="errormessage">%s</span>' % err_msg_sql)
    except Exception as e:
        logger.error("{0}:\n{1}".format(err_msg_to_log, e))
        return HttpResponse('<span class="errormessage">%s</span>' % err_msg)

    
@login_required()
def cag_apply_data_access_auditing(request):
    from dbmconfigapp.models.operational_manager import CAGDataAccessAuditing
    from django.db import connections, connection, DatabaseError

    logger = logging.getLogger('django')
    err_msg_to_log = 'Exception occured when applying Data Access Auditing settings for CAG Instance'
    err_msg_sql = 'Could not Apply configuration. SQL server error occured. See dbMotion CCenter event log for details.'
    err_msg = 'Could not Apply configuration. See dbMotion CCenter event log for details.'

    try:
        auditing_row = CAGDataAccessAuditing.objects.all()[0];
        with connections['cag_db'].cursor() as cursor:
                cursor.callproc("ApplyDataAccessAuditingSettings", [auditing_row.auditing_type, auditing_row.suspected_max_storage_size, auditing_row.authorized_max_storage_size, auditing_row.server_principals])

        return HttpResponse('<span class="successmessage">The configuration was applied successfully.</span>')

    except DatabaseError as de:
        logger.error("{0}:\n{1}".format(err_msg_to_log, de))
        return HttpResponse('<span class="errormessage">%s</span>' % err_msg_sql)
    except Exception as e:
        logger.error("{0}:\n{1}".format(err_msg_to_log, e))
        return HttpResponse('<span class="errormessage">%s</span>' % err_msg)
    