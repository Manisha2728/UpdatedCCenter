from django.conf.urls import include, url
from django.views.generic import TemplateView
from dbmconfigapp.views import *
from externalapps.views import *
from federation.views import *
from security.views import *
from django.views.generic.base import RedirectView
from django.conf.urls.static import static


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'configcenter.views.home', name='home'),
    # url(r'^configcenter/', include('configcenter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # This will redirect the "root" page to an actual page of the system.
    url(r'^$', RedirectView.as_view(url='/welcome/', permanent=True), name='index'),
    url(r'^dbmconfigapp/files/(?P<filename>.+)$', DbFiles),
    url(r'^admin/$', RedirectView.as_view(url='/welcome/', permanent=True)),
    url(r'^admin/', admin.site.urls),
    url(r'^authccenter/', include('authccenter.urls')),
    url(r'^export_db/', export_db),
    url(r'^download_export_db/', download_export_db),
    url(r'^import_db/', import_db),
    url(r'^post_import_db/', post_import_db),
    url(r'^welcome/', welcome),
    url(r'^history/', history_since_last_login),
    url(r'^search/', search_view),
    url(r'^searchresults/', search_results_view),
    url(r'^searchinit/', search_init_view),
    url(r'^passcode/', generate_passcode),
    url(r'^federation/apply/', apply_changes),
    url(r'^security/test_connection/', test_connection),
    url(r'^apply_data_access_auditing/', apply_data_access_auditing),
    url(r'^cag_apply_data_access_auditing/', cag_apply_data_access_auditing),
    url(r'^debug/', debug_view),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler500 = 'dbmconfigapp.views.handler500'
