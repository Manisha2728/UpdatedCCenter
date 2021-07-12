from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render

from authccenter.models.settings import SettingsModel
from security.models import ADProviders


def EnableADLoginOnlyModePage(request):
    ad_providers_exists = ADProviders.objects.count() > 0

    return render(request, 'authccenter/enableadloginonlymode.html', {'ad_providers_exists': ad_providers_exists})


def DisableCCenterLogin(request):
    settings = SettingsModel.objects.setting()
    settings.active_directory_mode = True
    settings.save()
    User.objects.update(is_active=False, is_staff=False)
    return redirect('/admin/logout/')
