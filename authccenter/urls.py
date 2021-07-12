from django.conf.urls import url

from . import views

urlpatterns = [
                       url(r'^$', views.EnableADLoginOnlyModePage, name='switch to AD login'),
                       url(r'Command/$', views.DisableCCenterLogin),

]
