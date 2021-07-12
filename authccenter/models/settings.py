from django.db import models
from django.utils.translation import ugettext_lazy as _


class SettingsManager(models.Manager):

    def setting(self):
        """

        :return: The settings for the app.
        :rtype: SettingsModel
        """

        query = super(SettingsManager, self).get_queryset()

        obj = query.first()

        if obj:
            return obj

        obj = SettingsModel()
        obj.save()
        return obj


class SettingsModel(models.Model):
    objects = SettingsManager()

    active_directory_mode = models.BooleanField(_('AD mode'), default=False)
