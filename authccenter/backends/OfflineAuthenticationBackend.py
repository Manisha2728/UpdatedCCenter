from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from authccenter.models.settings import SettingsModel


class Backend(ModelBackend):

    def AuthenticateUser(self, username, password, **kwargs):
        user = super(Backend, self).authenticate(username, password, **kwargs)
        if user:
            user.django_login = True
        return user

    def authenticate(self, username=None, password=None, **kwargs):
        try:

            settings = SettingsModel.objects.setting()

            if settings.active_directory_mode:
                return None

            return self.AuthenticateUser(username, password, **kwargs)

        except:
            return self.AuthenticateUser(username, password, **kwargs)

    def get_group_permissions(self, user_obj, obj=None):
        if not isinstance(user_obj, User):
            return set()
        return super(Backend, self).get_group_permissions(user_obj, obj)

    def get_all_permissions(self, user_obj, obj=None):
        if not isinstance(user_obj, User):
            return set()
        return super(Backend, self).get_all_permissions(user_obj, obj)

    def has_perm(self, user_obj, perm, obj=None):
        if not isinstance(user_obj, User):
            return False
        return super(Backend, self).has_perm(user_obj, perm, obj)

    def has_module_perms(self, user_obj, app_label):
        if not isinstance(user_obj, User):
            return False
        return super(Backend, self).has_module_perms(user_obj, app_label)

    def get_user(self, user_id):
        user = super(Backend, self).get_user(user_id)
        if not user:
            return None
        if not user.is_active:
            return None
        if user:
            user.django_login = True
        return user
