# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin
from django.utils.encoding import force_text
from dbmconfigapp.models import vpo, cvtables, clinical_viewer_general, apps_reporting, collaborate_patient_search,\
    apps_patient_display, cv_patient_display,\
    ehragent_clinical_domains, ehragent, PageBaseModel
from django.db.models.query import QuerySet
from django.forms.models import ModelMultipleChoiceField, ModelChoiceField
from django.contrib import admin

from django import forms
from django.db import models
import inspect
from dbmconfigapp.models.base import ConfigurationEntityBaseModel, ModelDescriptor
from django.contrib.admin.options import InlineModelAdmin, get_content_type_for_model
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from dbmconfigapp.utils.modelsqueries import *
from django.forms import fields
from dbmconfigapp import form
from django.http import Http404, HttpResponse
from django.utils.html import escape, escapejs
from dbmconfigapp.models import DbFiles
from django.utils.translation import ugettext as _

HELP_TEXT_FOR_GRID_FORMAT = '%s<br/>%s'
HELP_TEXT_FOR_GRID_FORMAT_DEFAULT = '<br/><i>Default: %s</i>'

import dbmconfigapp

def get_grid_help_text(text, default=""):
    if default:
        default = HELP_TEXT_FOR_GRID_FORMAT_DEFAULT % default
    
    return HELP_TEXT_FOR_GRID_FORMAT % (text, default)


def get_choice_value(choices, value):
    # Returns the value that presented to the user, according to the selected value that is saved in the database.
    # Use this method for choices that don't have standard index (0, 1, 2, 3...)
    return choices[[x[0] for x in choices].index(value)][1].decode('utf-8')  

class ServicesToRestart:
    # Enables the "Services to restart" button in the section title 
    def get_db_model_descriptor(self):
        _model = self.model
        base_index = 0
        if ConfigurationEntityBaseModel in inspect.getmro(_model):
            base_index = inspect.getmro(_model).index(ConfigurationEntityBaseModel, ) - 1
            if inspect.getmro(_model)[base_index]._meta.abstract:
                base_index-=1
            
        return inspect.getmro(_model)[base_index]._meta.db_table
    
    def get_services_to_restart_html(self):
        service_list = list(service.verbose_name for service in self.get_services_to_restart())
        return '<ul><li>' + '<li>'.join(service_list) + '</ul>'
    
    def get_services_to_restart(self):
        return ModelDescriptor.objects.get(model_name=self.get_db_model_descriptor()).services.filter(need_restart=True)
    
    

class dbmBaseModelAdmin(ModelAdmin):
    # This Base ModelAdmin class should apply to all CCenter project applications.
    # dbmconfigapp application uses dbmModelAdmin that inherits from dbmBaseModelAdmin
    save_on_top = True
    exclude = ('page_help_text', 'page_name', 'services', 'components', 'tree_id')

    def get_old_values_list_ids(self, form, field):        
        values = [form.fields[field].queryset.get(id=currId).__unicode__() for currId in form.initial[field]]
        return ",".join(values)
    
    def get_new_values_list_ids(self, form, field):        
        values = [c.__unicode__()  for c in list(form.cleaned_data[field])]
        return ",".join(values)
    
    def define_new_value_of_change_message(self, form, field):
        value = ''
        if form.cleaned_data[field] is not None and type(form.cleaned_data[field]) is QuerySet:
            value = self.get_new_values_list_ids(form, field);
        else:
            value = form.cleaned_data[field]
        if value == None or value == "":
            return ''   # '[empty value]'
        else:
            return str(value)
    
    def define_old_value_of_change_message(self, form, field):
        value = ''
        if form.initial[field] is not None and hasattr(form.fields[field], 'queryset'):
            if isinstance(form.fields[field], ModelMultipleChoiceField):
                value = self.get_old_values_list_ids(form, field)
            else:
                if form.fields[field].queryset.filter(id=form.initial[field]).exists():
                    value = form.fields[field].queryset.get(id=form.initial[field]).__unicode__()
                else:
                    value = "id=%s (deleted)" % form.initial[field]
        else:
            value = form.initial[field]  
        if value == None or value == "":
            return '[empty value]'
        else:
            return str(value)
    def get_changed_property(self, data):
        if data:
            return 'for ' + data
        return ''
    
    def get_changed_object(self, data):
        if data:
            return 'in ' + data
        return ''
    
    
    def get_field_displayed_value(self, field_class, value):
        
        if value != None and value != "" and value != "[empty value]":
            if form.fields.NumberAndChoicesField in inspect.getmro(type(field_class)):
                num, unit = (value.split('|'))
                unit = get_choice_value(field_class.fields[1].choices, int(unit))
                return '%s %s' % (num, unit)
                    
            if not type(field_class) == ModelMultipleChoiceField and not type(field_class) == ModelChoiceField and fields.ChoiceField in inspect.getmro(type(field_class)):
                return get_choice_value(field_class.choices, field_class.coerce(value)) 
        
        return value
    
    def compose_change_message(self, msg_list, form, field, old_value, new_value):
        '''
        TODO: Hebrew! Seems like it falls here if old_value or new_value has Hebrew chars. 
        '''
        field_title = form[field].label or field
        field_class = form[field].field
        if new_value is not None:
            return (u"{0}[{1}] field from \"{2}\" to \"{3}\", ").format(msg_list, field_title, self.get_field_displayed_value(field_class, old_value),
                                                                            self.get_field_displayed_value(field_class, new_value))
        if old_value is None:
            return (u"{0}field [{1}] , ").format(msg_list, field_title)
            
        return (u"{0}field [{1}] from \"{2}\", ").format(msg_list, field_title, old_value)
    
    def create_message_on_added(self, change_message, formset):        
        for added_object in formset.new_objects:
            if ('on_added_change_message' in dir(added_object)):
                change_message.append(('Added [%(name)s] %(object)s.')
                                  % {'name': force_text(added_object._meta.verbose_name),
                                  'object': force_text(added_object.on_added_change_message())})
            else:
                change_message.append(('Added [%(name)s] "%(object)s".')
                                      % {'name': force_text(added_object._meta.verbose_name),
                                      'object': force_text(added_object)})
    
    def create_message_on_changed(self, change_message, formset):       
        for changed_object, changed_fields in formset.changed_objects :
            change_object_name = force_text(changed_object._meta.verbose_name)
            if 'history_meta_label' in dir(changed_object._meta) and changed_object._meta.history_meta_label:
                change_object_name = changed_object._meta.history_meta_label
            for form in formset.initial_forms:
                if form.instance != changed_object:
                    continue                            
                for field in changed_fields:
                    if field == '_info': # in DataElements grids, the col '_info' is used for manipulations
                        continue
                    if field in ['patient_credential_password', 'mu_reporting_password']:
                        msg_list = u''
                        msg_list = self.compose_change_message(msg_list, form, field, None, None)                    
                        change_message.append(u'Changed {list} {object} {name}.'.format(
                                        list = msg_list[:-2],
                                        name =  self.get_changed_property(force_text(changed_object)),
                                        object = self.get_changed_object(change_object_name)))
                        continue
                    msg_list = u''  
                    new_value = self.define_new_value_of_change_message(form, field)
                    old_value = self.define_old_value_of_change_message(form, field)
                    msg_list = self.compose_change_message(msg_list, form, field, old_value, new_value)                    
                
                    change_message.append(u'Changed {list} {object} {name}.'.format(
                                        list = msg_list[:-2],
                                        name =  self.get_changed_property(force_text(changed_object)),
                                        object = self.get_changed_object(change_object_name))) 
            change_message.append(' {0}.'.format(str(changed_fields)))
            
               
    
    def create_message_on_deleted(self, change_message, formset):       
        for deleted_object in formset.deleted_objects:
            if ('on_deleted_change_message' in dir(deleted_object)):
                change_message.append(('Deleted [%(name)s] %(object)s.')
                                  % {'name': force_text(deleted_object._meta.verbose_name),
                                  'object': force_text(deleted_object.on_deleted_change_message())})
            else:
                change_message.append(('Deleted [%(name)s] "%(object)s".')
                                          % {'name': force_text(deleted_object._meta.verbose_name),
                                          'object': force_text(deleted_object)})       
    
    
    def construct_change_message(self, request, form, formsets):
        change_message = []
        if form.changed_data:
            msg_list = u''
            for field in form.changed_data:
                if field in ['untrusted_ad_user_password', 'mu_reporting_password']:
                    msg_list = self.compose_change_message(msg_list, form, field, None, None)                    
                    continue
                
                new_value = self.define_new_value_of_change_message(form, field)
                old_value = self.define_old_value_of_change_message(form, field)
                msg_list = self.compose_change_message(msg_list, form, field, old_value, new_value)                    
            
            change_message.append(u'Changed {list} {object}.'.format(
                                    list = msg_list[:-2],
                                    object = self.get_changed_object(force_text(form.instance))))
            
            change_message.append(' {0}.'.format(str(form.changed_data)))
            
        if formsets:
            for formset in formsets:
                self.create_message_on_added(change_message, formset)
                self.create_message_on_changed(change_message, formset)
                self.create_message_on_deleted(change_message, formset)
            # tbener Jan 2017 - fix bug - ST-2059 CCenter history is not saved properly for some objects
            # This handles a case when an inline formset is changed and the main model wasn't.
            if change_message and not form.changed_data:
                # We do that only if the main model is not of page type
                if not PageBaseModel in inspect.getmro(form._meta.model):
                    change_message.insert(0, u'For {object}:'.format(object=force_text(form.instance)))
        change_message = ' '.join(change_message)
        return change_message or ('No fields changed.')
            
    def log_addition(self, request, object):
        message = 'Added "%s"' % force_text(object)
        try:
            message = 'Added [%s] "%s"' % (object._meta.verbose_name, force_text(object))
        except:
            pass
        from django.contrib.admin.models import ADDITION
        self.execute_log_action(request, object, ADDITION, message)
        
    def log_change(self, request, object, message):
        # TODO: if log_object != object: message.append(" in [%s] %s" % (force_text(object), object.name))
        # because it doesn't say in which object (which might be in a popup window)
        from django.contrib.admin.models import CHANGE
        self.execute_log_action(request, object, CHANGE, message)
             
    def log_deletion(self, request, object, object_repr):
        """
        Log that an object will be deleted. Note that this method is called
        before the deletion.

        The default implementation creates an admin LogEntry object.
        """
        message = 'Deleted "%s"' % force_text(object)
        try:
            message = 'Deleted [%s] "%s"' % (object._meta.verbose_name, force_text(object))
        except:
            pass
        from django.contrib.admin.models import DELETION
        self.execute_log_action(request, object, DELETION, message)

    
    def execute_log_action(self, request, object, action_flag, message):    #dbMotion
        log_object = self.get_object_for_log(object, message)

        from authccenter.utils import get_request_user_ids
        from dbmconfigapp.models.tracking import ChangesHistory

        user_id, ccenter_user_id = get_request_user_ids(request)
        
        if type(log_object) is list: #when update of one page impacts others
            for item in log_object:
                ChangesHistory.objects.log_action(
                    user_id         = user_id,
                    ccenter_user_id = ccenter_user_id,
                    content_type_id = ContentType.objects.get_for_model(item).pk,
                    object_id       = item.pk,
                    object_repr     = force_text(item),
                    action_flag     = action_flag,
                    change_message  = message
                )
        else:
            ChangesHistory.objects.log_action(
                user_id         = user_id,
                ccenter_user_id = ccenter_user_id,
                content_type_id = ContentType.objects.get_for_model(log_object).pk,
                object_id       = log_object.pk,
                object_repr     = force_text(log_object),
                action_flag     = action_flag,
                change_message  = message
            )
    
    def get_object_for_log(self, object, message):
        # This method is designed to be overridden 
        return object
    
    def response_change(self, request, obj):
        # tbener: to enable edit an object in a popup window we call dismissEditPopup (in dbm_common.js) when submitting, similar to adding behavior.
        if "_popupex" in request.GET: # and not "_continue" in request.POST:
            pk_value = obj._get_pk_val()
            return HttpResponse(
                '<!DOCTYPE html><html><head><title></title></head><body>'
                '<script type="text/javascript">opener.dismissEditPopup(window, "%s", "%s");</script></body></html>' % \
                # escape() calls force_text.
                (escape(pk_value), escapejs(obj)))
        return super(dbmBaseModelAdmin, self).response_change(request, obj)
    
    def response_add(self, request, obj, post_url_continue=None):
        if "_popupex" in request.GET: # and not "_continue" in request.POST:
            pk_value = obj._get_pk_val()
            return HttpResponse(
                '<!DOCTYPE html><html><head><title></title></head><body>'
                '<script type="text/javascript">opener.dismissEditPopup(window, "%s", "%s");</script></body></html>' % \
                # escape() calls force_text.
                (escape(pk_value), escapejs(obj)))
        return super(dbmBaseModelAdmin, self).response_add(request, obj, post_url_continue)
    
    def save_formset(self, request, form, formset, change):
        # tbener 4\2016 - http://dbm-jira:8080/browse/ST-2004
        # wrapping around file saving functionality
        # standard operation doesn't delete files from table - ever.
        # NOTE: this logic assumes every ImageField has a different storage path across all project 
        lst_old = []
        
        # check if model has ImageField fields
        if getattr(formset.model, 'contains_file_fields', False)():
            for img_fld in formset.model.file_fields:
                # get all file names currently stored for current model
                lst_old += [getattr(record, img_fld.name).name for record in formset.model.objects.all()]
        lst_old = filter(None, lst_old)
        
        # Call default function
        ModelAdmin.save_formset(self, request, form, formset, change)
        
        if lst_old:
            lst_new = []
            for img_fld in formset.model.file_fields:
                # get all file names stored for current model - after the save
                lst_new += [getattr(record, img_fld.name).name for record in formset.model.objects.all()]
                
            # we will delete only files from the first list, that do not exist in the new list
            lst_to_del = [f for f in lst_old if f not in lst_new]
            if lst_to_del:
                DbFiles.objects.filter(filename__in = lst_to_del).delete()

    # override base method to show custom History view
    def history_view(self, request, object_id, extra_context=None):
        from dbmconfigapp.models.tracking import ChangesHistory
        from django.shortcuts import render, get_object_or_404

        model = self.model
        obj = get_object_or_404(self.get_queryset(request), pk=object_id)

        action_list = ChangesHistory.objects.filter(object_id=object_id, content_type=get_content_type_for_model(model))

        return render(request, 'admin/page_changes_history.html', {
            'page_title': _('Change History: %s') % force_text(obj),
            'action_list': action_list,
            })
                
    class Media:
        js = ['admin/js/dbm_common.js'] 
        


class dbmModelAdminSaveOnly(dbmBaseModelAdmin):
    
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] =  ('_popup' in request.GET)
        extra_context['show_delete_link'] = False
        extra_context['show_save_as_new'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(dbmModelAdminSaveOnly, self).change_view(request, object_id, form_url, extra_context=extra_context)
        
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = ('_popup' in request.GET)
        extra_context['show_delete_link'] = False
        extra_context['show_save_as_new'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(dbmModelAdminSaveOnly, self).add_view(request, form_url, extra_context=extra_context)


from dbmconfigapp.forms import BaseModelAdminForm
from dbmconfigapp import models as appmodels

class dbmModelAdmin(dbmModelAdminSaveOnly): 
    # Used in dbmconfigapp for every "page" model admin
    
    form = BaseModelAdminForm
    
    # NOTE: It is better to override this method in your admin than add entries to this method.
    # see example in ehragent_categories.EHRAgentCategoriesTooltipsPopupAdmin
    def get_object_for_log(self, object, message):
        '''
        Used for popup windows, so the history activity will be associated with the parent page.
        '''
        if type(object) is appmodels.cvtables.ImagingPacs:
            return appmodels.ClinicalDomainImaging.objects.all()[0]
        
        if type(object) is clinical_viewer_general.ExternalApplication:
            return appmodels.clinical_viewer_general.ClinicalViewerGeneralPage.objects.all()[0]
        
        '''
        For duplicate pages the history activity will be saved for every page.
        '''
        if type(object) in (collaborate_patient_search.CvPatientSearch,) :
            return [collaborate_patient_search.CvPatientSearch.objects.all()[0],]

        if type(object) in (apps_reporting.CVReportingPage, apps_reporting.PVReportingPage) :
            if message.find('lab_susceptibility_methods_code_type') != -1:
                return [apps_reporting.CVReportingPage.objects.all()[0],
                        apps_reporting.PVReportingPage.objects.all()[0],
                        cvtables.ClinicalDomainLabResults.objects.all()[0]]
            else:
                return [apps_reporting.CVReportingPage.objects.all()[0],
                        apps_reporting.PVReportingPage.objects.all()[0]]

        if type(object) is cvtables.ClinicalDomainLabResults and message.find('lab_susceptibility_methods_code_type') != -1:
            return [apps_reporting.CVReportingPage.objects.all()[0],
                    apps_reporting.PVReportingPage.objects.all()[0],
                    cvtables.ClinicalDomainLabResults.objects.all()[0]]           
                            
        if type(object) in (cv_patient_display.CvPatientDisplayPage,
                            apps_patient_display.PlPatientDisplayPage) :
            return [cv_patient_display.CvPatientDisplayPage.objects.all()[0],
                    apps_patient_display.PlPatientDisplayPage.objects.all()[0]]
        
        if type(object) in (clinical_viewer_general.ClinicalViewerGeneralPage,):
            if  message.find('[Calculation of the Facility field]') != -1 or message.find('is_encounter_conf_inheritance') != -1:
                return [clinical_viewer_general.ClinicalViewerGeneralPage.objects.all()[0],]
                      
        return object
        
    class Media:
        css = { "all" : ("admin/css/dbmconfigapp/hide_admin_original.css",) }
        js = ['admin/js/dbmconfigapp/custom-ui.js'] 



class dbmBaseInline(InlineModelAdmin, ServicesToRestart):
    # override this in admin inline to get the Add and Delete permissions automatically
    extra = 0
    
    
    
    def has_add_permission(self, request, obj=None):
        return self.extra
    def has_delete_permission(self, request, obj=None):
        return self.extra

class dbmBaseAdminStackedInline_Simple(dbmBaseInline):
    template = 'admin/edit_inline/stacked.html'
    
    formfield_overrides = {
         models.NullBooleanField: {'widget': forms.CheckboxInput()},
         models.TextField: {'widget': forms.Textarea(attrs={'rows':4, 'cols':100})},
         }
    

# with sections
class dbmBaseAdminStackedInline(dbmBaseAdminStackedInline_Simple):
    template = 'admin/edit_inline/stacked_no_header.html'
    section_name = '' 
    
    def __init__(self, *args, **kwargs):
        super(dbmBaseAdminStackedInline, self).__init__(*args, **kwargs)
        if self.section_name:
            self.model._meta.history_meta_label = self.section_name

class dbmBaseAdminTabularInline(admin.TabularInline, dbmBaseInline):
    pass

class dbmBaseAdminTabularSimple(admin.TabularInline, dbmBaseInline):
    template = 'admin/edit_inline/tabular_no_header.html'
    
    
    
    