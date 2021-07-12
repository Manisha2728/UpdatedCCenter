import requests
from django.core.management.base import BaseCommand

from configcenter import settings


class Command(BaseCommand):
    help = "Check site available."

    def handle(self, *args, **options):
        server_name = settings.get_param("application_server")
        domain_name = settings.get_param("default_domain_name")
        site = "https://%s.%s:8040/" % (server_name, domain_name)

        print ("Pinging CCenter site: '%s'" % site)
        request = requests.get(site, verify=False)

        if request.status_code != 200:
            print ('CCenter site (%s) does not exist.' % site)
            raise Exception('Web site does not exist')

        print ('CCenter site (%s) exist.' % site)
        print ("Validation pass.")
