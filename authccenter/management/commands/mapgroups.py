from optparse import make_option

from django.core.management import call_command
from django.core.management.base import BaseCommand

from authccenter.models.group import ADGroup, CCenterGroup


class Command(BaseCommand):
    help = "Map AD groups to ccenter groups"

    option_list = BaseCommand.stealth_options + (
        make_option('--adminsgroup',
                    action='store',
                    dest='admins',
                    type="string",
                    default='',
                    help='Map to admins group of ccenter',
                    ),
        make_option('--guestsgroup',
                    action='store',
                    dest='guests',
                    default='',
                    type="string",
                    help='Map to guests group of ccenter')
    )

    def handle(self, *args, **options):
        #call_command('smart_migrate', 'authccenter')
        guests_group_name = options.pop('guests', '')
        admins_group_name = options.pop('admins', '')

        if admins_group_name:
            ccneter_admins_group, _ = CCenterGroup.objects.get_or_create(name='ccenter_admins_group')
            ccneter_admins_group.adgroup_set.all().delete()
            ccneter_admins_group.adgroup_set.create(name=admins_group_name)

        if guests_group_name and guests_group_name != admins_group_name:
            ccenter_guests_group, _ = CCenterGroup.objects.get_or_create(name='ccenter_guests_group')
            ccenter_guests_group.adgroup_set.all().delete()
            ccenter_guests_group.adgroup_set.create(name=guests_group_name)