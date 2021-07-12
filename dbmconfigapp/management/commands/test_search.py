from django.core.management.base import BaseCommand
from dbmconfigapp.utils.search import PAGES_INFO
import xml.etree.ElementTree as ET
import os
from configcenter import settings

class Command(BaseCommand):
    help = 'check that all the entries in the tree are in the search and vise versa'

    def handle(self, *args, **options):
        tree_view_path = os.path.join(settings.PROJECT_DIR, 'templates','admin', 'includes', 'treeview.html');
        tree = ET.parse(tree_view_path)
        root = tree.getroot()
        pages=filter(lambda page : page.attrib['href'] != "#", root.findall('.//li/a[@href]'))

        print("starting checking that all the pages that in the tree are in the search")
        for page in pages:
            tree_entry_page_in_search = False

            for k, v in PAGES_INFO.items():
                for i in v:
                    if i[1] == page.attrib['href']:
                        tree_entry_page_in_search = True
            if (tree_entry_page_in_search == False):
                print("page '{a}', (address '{b}') in tree without search".format(a=page.text, b= page.attrib['href']))
        print("finishing checking that all the pages that in the tree are in the search")

        print("starting checking that all the pages that in the search are in the tree")
        for k, v in PAGES_INFO.items():
            page_search_tree_entry = False
            for i in v:
                for page in pages:
                    if i[1] == page.attrib['href']:
                        page_search_tree_entry = True
            if (page_search_tree_entry == False):
                print("search '{a}' in search without been in tree".format(a=k))
        print("finishing checking that all the pages that in the search are in the tree")


