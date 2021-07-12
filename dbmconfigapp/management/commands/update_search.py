from django.core.management.base import BaseCommand
from django.test import Client
from dbmconfigapp.utils.search import PAGES_INFO
import os
from configcenter import settings

class Command(BaseCommand):
    help = 'Update search files'

    def handle(self, *args, **options):
        c = Client()
        if not c.login(username='admin', password='123'):
            print("please add the user")
            return

        for k, v in PAGES_INFO.items():
            print("Updating page {a}".format(a=k))
            response = c.get(v[0][1])

            cleaned_html = self.clean_html(response.content)

            with open(os.path.join(settings.PROJECT_DIR, 'resources','html', k), "w") as file:
                file.write(cleaned_html)


    def clean_html(self, html_text):
        from bs4 import BeautifulSoup
        from dbmconfigapp.utils.search import clean_soup

        cleaned = clean_soup(BeautifulSoup(html_text))
        return cleaned.prettify().encode("UTF-8")