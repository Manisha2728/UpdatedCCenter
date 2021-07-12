from django.contrib.auth.models import Permission
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _


class CCenterGroup(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'), blank=True)

    class Meta:
        verbose_name = _('ccenter group')
        verbose_name_plural = _('ccenter groups')

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name,


class ADGroup(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    ccneter_group = models.ForeignKey(CCenterGroup, on_delete=CASCADE)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name,

    class Meta:
        verbose_name = _('ad group')
        verbose_name_plural = _('ad groups')
