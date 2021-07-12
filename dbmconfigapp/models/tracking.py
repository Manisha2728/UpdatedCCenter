from django.contrib.admin.models import LogEntry
from authccenter.models.user import CCenterUser
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import smart_text
from authccenter.utils import get_user_name, get_user_to_dispay

class ChangesHistoryManager(models.Manager):
    def log_action(self, user_id, ccenter_user_id, content_type_id, object_id, object_repr, action_flag, change_message=''):
        log_item = self.model(None, None, 
                       user_id = user_id,
                       ccenter_user_id = ccenter_user_id,
                       content_type_id = content_type_id, 
                       object_id = smart_text(object_id), 
                       object_repr = object_repr[:200], 
                       action_flag = action_flag, 
                       change_message = change_message)
        log_item.save()

class ChangesHistory(LogEntry):
    ccenter_user = models.ForeignKey(CCenterUser, on_delete=models.SET_NULL, null=True)

    def user_to_dispay(self):
        return get_user_to_dispay(self)

    def user_name(self):
        return get_user_name(self)

    objects = ChangesHistoryManager()
  
    class Meta:
        verbose_name = 'Change Action'
        help_text = 'The search is available for the following fields: Screen, Page Model Name and Action.'

ChangesHistory._meta.get_field('change_message').verbose_name = 'Action'
ChangesHistory._meta.get_field('action_time').verbose_name = 'Date/Time'
ChangesHistory._meta.get_field('content_type').verbose_name = 'Screen'

class LoginsHistoryManager(models.Manager):
    def log_action(self, user_id, ccenter_user_id, action, login_name=''):
        log_item = self.model(
                       user_id = user_id,
                       ccenter_user_id = ccenter_user_id,
                       action = action,
                       login_name = login_name)
        log_item.save()

class LoginsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ccenter_user = models.ForeignKey(CCenterUser, on_delete=models.SET_NULL, null=True)
    login_name = models.CharField(max_length=100, null=True, blank=True)
    action_time = models.DateTimeField(verbose_name='Date/Time', auto_now_add=True)
    action = models.TextField(verbose_name='Action')

    objects = LoginsHistoryManager()
  
    class Meta:
        verbose_name = 'Login/Logout Action'
