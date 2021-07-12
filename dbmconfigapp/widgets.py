from django.utils.html import mark_safe, format_html
from django.utils.encoding import force_text
from django.forms.widgets import HiddenInput, Input, MultiWidget, TextInput, Select, CheckboxSelectMultiple
from django.forms.utils import flatatt
from itertools import chain
from django.contrib.admin import widgets
from django.urls import reverse
from django.templatetags.static import static
from django.utils.translation import ugettext as _ 

class Sortable(Input):
    tag = "ul"
    
    def __init__(self, attrs=None, choices=(), sep='|'):
        super(Sortable, self).__init__(attrs)
        
        self.choices = list(choices)
        
    def render(self, name, value, attrs=None, renderer=None, choices=(), sep='|'):
        # convert to dictionary
        choices = dict(x for x in chain(self.choices, choices))
        sorted_list = value.split(sep) if value else []

        final_attrs = self.build_attrs(attrs)
        output = [format_html('<{0} name="sortable_{1}" class="sortable"{2}>', self.tag, name, flatatt(final_attrs))]
        # Normalize to strings
        for option_value in sorted_list:
            option_label = force_text(choices[option_value])
            output.append(format_html('<li id="{1}" class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>{0}</li>', option_label, option_value))
        output.append(format_html('</{0}>', self.tag))
        input = HiddenInput().render(name, value)
        output.append(input)
        
        script = """
        <script type="text/javascript">
            $(function(){
                $('""" + self.tag + """[name="sortable_""" + name + """"]').sortable({
                   revert       : true,
                   stop         : function(event,ui){
                       var input = $(event.target).next("input");
                       var value = $(event.target).sortable("toArray").join('""" + sep + """');
                       $(input).val(value);
                   }
                });
                $('""" + self.tag + """[name="sortable_""" + name + """"]').disableSelection();
            });
        </script>
        """
        
        output.append(script)
        
        return mark_safe('\n'.join(output))

class TextAndSelectWidget(MultiWidget):
    """
    A Widget that splits time-span in format '2|days' into two widgets: <input type="text"> and <Select/> boxes.
    """
    def __init__(self, *args,**kwargs):
        choices = kwargs.pop("choices")
        text_attrs = {'size':'4', 'style':'margin-right: 8px;'}
        text_attrs.update(kwargs)
        widgets = (TextInput(attrs=text_attrs),
                   Select(choices=choices))
        super(TextAndSelectWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            return value.split('|')
        return [None, None]


class CheckboxSelectMultipleEx(CheckboxSelectMultiple):
    def render(self, *args, **kwargs): 
        output = super(CheckboxSelectMultipleEx, self).render(*args,**kwargs) 
        return mark_safe(output.replace(u'<ul>', u'').replace(u'</ul>', u'').replace(u'<li>', u'<p>').replace(u'</li>', u'</p>'))


class RelatedFieldWidgetWrapperEx(widgets.RelatedFieldWidgetWrapper):
    def __init__(self, widget, rel, admin_site, can_add_related=None, can_change_related=None, can_delete_related=None, can_view_related=None):
        self.can_change_related = can_change_related
        super(RelatedFieldWidgetWrapperEx, self).__init__(widget, rel, admin_site, can_add_related)
        
    def render(self, name, value, *args, **kwargs):
        output = [super(RelatedFieldWidgetWrapperEx, self).render(name, value, *args, **kwargs)]
        rel_to = self.rel.related_model
        if self.can_change_related:
            related_url = '/admin/%s/%s/{0}/' % (rel_to._meta.app_label, rel_to._meta.object_name.lower())  
            # TODO: "add_id_" is hard-coded here. This should instead use the
            # correct API to determine the ID dynamically.
            output.append('<a href_base="%s" class="edit-related" id="edit_id_%s" onclick="return showEditPopup(this);"> '
                          % (related_url, name))
            output.append('<img src="%s" width="10" height="10" alt="%s"/></a>'
                          % (static('admin/img/icon_changelink.gif'), _('Edit')))
        return mark_safe(''.join(output))
        
        
widgets.RelatedFieldWidgetWrapper = RelatedFieldWidgetWrapperEx
        
class HorizontalSortable(Input):
    tag = "ul"
    
    def __init__(self, attrs=None, choices=(), sep='|'):
        super(HorizontalSortable, self).__init__(attrs)
        
        self.choices = list(choices)
        
    def render(self, name, value, attrs=None, renderer=None, choices=(), sep='|'):
        # convert to dictionary
        choices = dict(x for x in chain(self.choices, choices))
        sorted_list = value.split(sep) if value else []

        final_attrs = self.build_attrs(attrs)
        output = [format_html('<{0} name="horizontalsortable_{1}" class="sortable"{2}>', self.tag, name, flatatt(final_attrs))]
        # Normalize to strings
        for option_value in sorted_list:
            option_label = force_text(choices[option_value])
            output.append(format_html('<li id="{1}" class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>{0}</li>', option_label, option_value))
        output.append(format_html('</{0}>', self.tag))
        input = HiddenInput().render(name, value)
        output.append(input)
        
        return mark_safe('\n'.join(output))
        