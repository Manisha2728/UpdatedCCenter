#import django
#django.setup()

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from authccenter.signals import login_failure


from django.contrib.auth.signals import *
from django.dispatch import receiver

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    log_success_action(user, 'Login')

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    log_success_action(user, 'Logout')

@receiver(login_failure)
def user_login_failed_callback(sender, username, exception, **kwargs):
    import logging
    from dbmconfigapp.models.tracking import LoginsHistory

    LoginsHistory.objects.log_action(None,
                                     None,
                                     'Login failed',
                                     username)
    logger = logging.getLogger('django')
    logger.error("Login to CCenter failed for user '%s':\n%s" % (username, exception))

def log_success_action(user, action):
    from authccenter.models.user import CCenterUser
    from dbmconfigapp.models.tracking import LoginsHistory

    user_id = None
    ccenter_user_id = None

    if(isinstance(user, CCenterUser)):
        ccenter_user_id = user.pk
    else:
        user_id = user.pk

    LoginsHistory.objects.log_action(user_id, ccenter_user_id, action)

@receiver(post_migrate)
def define_ccenter_groups_permissions(sender, **kwargs):
    try:
        from django.contrib.auth.models import Permission
        from authccenter.models.group import CCenterGroup

        group = CCenterGroup.objects.get(name='ccenter_admins_group')
        permissions = Permission.objects.all()
        group.permissions.add(*permissions)
        group.save()
    except:
        pass

#@receiver(authccenter_signals.login_failure)
#def define_ccenter_groups_permissions(sender, username, exception, **kwargs):
#   pass


class Config(AppConfig):
    name = 'authccenter'
    verbose_name = 'Ccenter authentication'


