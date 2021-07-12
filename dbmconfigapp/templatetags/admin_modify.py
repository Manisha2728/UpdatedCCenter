from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row
# or 
# original_submit_row = submit_row

@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_' + context["app_label"]: not ctx['is_popup'],
        'show_save': context.get('show_save', ctx['show_save']),
        'show_delete_link': context.get('show_delete_link', ctx['show_delete_link']),
        'show_save_as_new': context.get('show_save_as_new', ctx['show_save_as_new']),
        'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue']),
        })                                                                  
    return ctx 