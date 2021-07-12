from django.core.exceptions import ValidationError
import re
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
# from django.utils import six


def validate_not_empty_string(value):
    if value.strip():
        raise ValidationError('This field is required and should not be empty string!')

def validate_integer_is_more_than_0(value):
    if (value <= 0):
        raise ValidationError('The value should be more than 0')

class ExcludeRegexValidator(object):
    regex = ''
    message = _('Enter a valid value.')
    code = 'invalid'

    def __init__(self, regex=None, message=None, code=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

        # Compile the regex if it was not passed pre-compiled.
        # if isinstance(self.regex, six.string_types):
            # self.regex = re.compile(self.regex)

    def __call__(self, value):
        """
        Validates that the input matches the regular expression.
        """
        if self.regex.search(force_text(value)):
            raise ValidationError(self.message, code=self.code)


ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
validate_not_ipv4_address = ExcludeRegexValidator(ipv4_re, _('Value Can Not Be IPv4 address.'), 'invalid')

def validate_not_ipv4(value):
    try:
        validate_not_ipv4_address(value)
    except (ValueError, TypeError):
        raise ValidationError('Value Can Not Be IPv4 address.')

