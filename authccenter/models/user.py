import datetime

from django.contrib.auth.models import Permission
from django.db import models
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.utils.translation import ugettext_lazy as _

from authccenter.models.group import ADGroup


class CCenterUser(models.Model):
    USERNAME_FIELD = 'username'

    first_name = models.CharField(_('first name'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True, null=True)

    username = models.CharField(_('username'), max_length=100, blank=False, null=False)

    last_login = models.DateTimeField(_('last login'), default=timezone.now)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    session_key = models.CharField(_('session key'), max_length=100, blank=True, null=True)

    @property
    def is_active(self):

        return (self.last_login + datetime.timedelta(hours=3) > timezone.now()) \
               and (self.date_joined <= timezone.now())

    @is_active.setter
    def is_active(self, value):
        pass

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return self.get_username(),


    def is_authenticated(self):

       return self.is_active

    def get_full_name(self):
        if not self.last_name:
            return self.get_username()

        if not self.first_name:
            return self.get_username()

        return '%s, %s' % (self.last_name, self.first_name)

    def get_short_name(self):
        if not self.first_name:
            return self.get_username()

        return self.first_name

    def get_session_auth_hash(self):
        """
        Returns an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.username).hexdigest()

    @property
    def is_superuser(self):
        return False

    @is_superuser.setter
    def is_superuser(self, value):
        pass

    groups = models.ManyToManyField(ADGroup, verbose_name=_('groups'),
                                    blank=True, help_text=_('The groups this user belongs to.'),
                                    related_name="ccenter_user_set", related_query_name="ccenter_user")

    user_permissions = None

    def get_group_permissions(self, obj=None):
        self.last_login = timezone.now()
        if obj is not None:
            return set()
        if not self.is_active:
            return False
        if hasattr(self, '_group_permissions'):
            return self._group_permissions
        permissions = Permission.objects.filter(ccentergroup__adgroup__ccenter_user=self)

        perms = permissions.values_list('content_type__app_label', 'codename').order_by()
        self._group_permissions = set("%s.%s" % (ct, name) for ct, name in perms)

        return self._group_permissions

    def get_all_permissions(self, obj=None):
        self.last_login = timezone.now()
        if hasattr(self, '_permission'):
            return self._permission

        if obj is not None:
            return set()
        if not self.is_active:
            return False
        self._permission = self.get_group_permissions(obj)
        return self._permission

    def has_perm(self, perm, obj=None):
        self.last_login = timezone.now()
        if not self.is_active:
            return False

        return perm in self.get_all_permissions(obj)

    def has_perms(self, perm_list, obj=None):
        self.last_login = timezone.now()
        for perm in perm_list:
            if self.has_perm(perm, obj):
                continue
            return False
        return True

    def has_module_perms(self, app_label):
        self.last_login = timezone.now
        if not self.is_active:
            return False

        for perm in self.get_all_permissions():
            if perm[:perm.index('.')] != app_label:
                continue
            return True
        return False

    @property
    def is_staff(self):
        return self.is_active and (self.groups.count() > 0)

    @is_staff.setter
    def is_staff(self, value):
        pass


    class Meta:
        verbose_name = _('ccenter user')
        verbose_name_plural = _('ccenter users')
