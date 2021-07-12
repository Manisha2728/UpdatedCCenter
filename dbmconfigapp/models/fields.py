from django.db import models
from io import BytesIO
from django.core.exceptions import ValidationError
from dbmconfigapp.form import fields
from django.utils.translation import ugettext_lazy as _

class PngJpgImageField(models.ImageField):
    allowed_formats = ('PNG', 'JPEG')

    def to_python(self, data):
        f = super(PngJpgImageField, self).to_python(data)
        if f is None:
            return None

        try:
            from PIL import Image
        except ImportError:
            import Image

        # We need to get a file object for PIL. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, 'temporary_file_path'):
            file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                file = BytesIO(data.read())
            else:
                file = BytesIO(data['content'])

        try:
            im = Image.open(file)
            if im.format not in self.allowed_formats:
                raise ValidationError("Unsupported image type: " + im.format + ". Please upload a png or a jpeg image")
        except ImportError:
            # Under PyPy, it is possible to import PIL. However, the underlying
            # _imaging C module isn't available, so an ImportError will be
            # raised. Catch and re-raise.
            raise

        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f




class NumberAndChoicesField(models.Field):

    description = 'String (representing a number and a selected choice concatenated with a separator)'
    
    # Note: if we leave self.choices the field uses forms.TypedChoiceField
    choices = None
    mychoices = ()
     
    def __init__(self, max_length=50, *args, **kwargs):
        defaults = {'max_length': max_length}
        defaults.update(kwargs)
        if 'choices' in defaults:
            self.mychoices = defaults.pop('choices')
        super(NumberAndChoicesField, self).__init__(*args, **defaults)
        
    def get_internal_type(self):
        return "CharField"
         
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.NumberAndChoicesField, 
                    'choices': self.mychoices}
        defaults.update(kwargs)
        return super(NumberAndChoicesField, self).formfield(**defaults)
    
    
class TimeSpanField(NumberAndChoicesField):
    def __init__(self, min_value=-9223372036854775807, *args, **kwargs):
        self.min_value = min_value
        super(TimeSpanField, self).__init__(*args, **kwargs)
        
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value}
        defaults.update(kwargs)
        return super(TimeSpanField, self).formfield(**defaults)
    
    

class IntegerFieldEx(models.IntegerField):
    description = _("Integer with min max range")
    
    def __init__(self, min_value=-9223372036854775807, max_value=9223372036854775807, *args, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(IntegerFieldEx, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "IntegerField"

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value' : self.max_value}
        defaults.update(kwargs)
        return super(IntegerFieldEx, self).formfield(**defaults)
        

class SelectMultipleChoicesField(models.CharField):
    description = _('Comma separated field')
    
    allowed_choices = ()
    
    def __init__(self, max_length=400, *args, **kwargs):
        defaults = {'max_length': max_length}
        defaults.update(kwargs)
        if 'choices' in defaults:
            self.allowed_choices = defaults.pop('choices')
        super(SelectMultipleChoicesField, self).__init__(*args, **defaults)
        
    def get_internal_type(self):
        return "CharField"

#     def validate(self, value, model_instance):
#         return super(SelectMultipleChoicesField, value, model_instance).validate()

