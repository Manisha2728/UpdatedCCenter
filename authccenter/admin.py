from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from authccenter.utils import FAKE_DJANGO_USER_NAME

class OfflineUserAdmin(UserAdmin):

    def get_queryset(self, request):

        qs = super(OfflineUserAdmin, self).get_queryset(request)

        return qs.exclude(username = FAKE_DJANGO_USER_NAME)

admin.site.unregister(User)
admin.site.register(User, OfflineUserAdmin)


