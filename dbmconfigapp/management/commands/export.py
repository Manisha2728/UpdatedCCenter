'''
Created on Mar 3, 2016

@author: TBENER
'''
from django.core.management import BaseCommand
from optparse import make_option
import sys
import os
from os import path
import xml.dom.minidom as dom
from django.db import connections, DEFAULT_DB_ALIAS
#from django.utils import simplejson
import json

#CCenter imports
from dbmconfigapp.export_logic import get_export_db_data, get_objects_table
from dbmconfigapp.models.base import Service


class Command(BaseCommand):
    option_list = BaseCommand.stealth_options + (
#         make_option("--file", dest = "filename",  action="store",       
#                     help = "specify export file"),
        make_option('--no-time-stamp', action='store_false', dest='time_stamp', default=True,
                    help='Export without time-stamp (for comparison / testing). The default behavior puts time stamp in the file header.'),
    )
    
    help = "Exports all data to a file in json format."
    args = "path_to_file [--no_time_stamp]"
        
    def handle(self, filename, *keys, **options):
        try:
            time_stamp = options.get('time_stamp', False)
            
            result = export_to_file(filename, list(keys), time_stamp)
             
            if result is False:
                sys.exit(1) # Operation failed, so the command fails.
        except Exception:
            exc_class, exc, tb = sys.exc_info()
            print(exc or exc_class)
            sys.exit(1) # O
            
        print('Export command finished successfully.')
    


def export_to_file(filename, keys, time_stamp):
    print('\nExporting to: %s' % filename)
    
    if not path.exists(path.dirname(filename)):
        os.makedirs(path.dirname(filename))
    
    json_data = json.loads(get_export_db_data(get_objects_table.keys(), time_stamp))
    with open(filename, 'w') as f:
        f.write(json.dumps(json_data, indent=4, separators=(',', ': ')))
        
    return True




def get_services_data_to_xml(_dir):
    print('\nSaving to: %s' % _dir.split('/')[-1])
    
    if not path.exists(_dir):
        os.makedirs(_dir)
        
    con = connections[DEFAULT_DB_ALIAS]
        
    for service in Service.objects.all():
        try:
            print('Getting data: %s' % service.code_name)
            cur = con.cursor()
            try:
                cur.cursor.callproc('adm_GetServiceConfigurations', [service.code_name])
            except:
                continue
            answer = cur.cursor.fetchall()
            if (answer):
                print('Saving %s.xml' % service.code_name)
                doc = dom.parseString(answer[0][0])
                with open(os.path.join(_dir,service.code_name + ".xml" ), 'w') as f:
                    f.write(doc.toprettyxml())
        finally:
            cur.close()