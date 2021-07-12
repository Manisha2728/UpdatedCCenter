'''
Created on Apr 6, 2015

@author: AReznikov
'''
from django.core.management.base import BaseCommand, CommandError
import os.path
from os import listdir
from dbmconfigapp import export_logic

class Command(BaseCommand):
    args = 'import_files_path'
    help = 'Imports data from all files in the import_files_path directory to CCenter database'

    def handle(self, *args, **options):        
        try:
            import_files_path = args[0]
            if os.path.exists(import_files_path):
                for file_name in listdir(import_files_path): 
                    import_file_path = os.path.join(import_files_path,file_name)
                    if os.path.isfile(import_file_path) and os.path.splitext(import_file_path)[1].lower() == '.json':
                        import_file = open(import_file_path, 'r')
                        export_logic.import_db_from_file(import_file, None)
                        self.stdout.write('Successfully imported file "{0}"'.format(import_file_path))
            else:
                self.stdout.write('Directory "{0}" does not exist'.format(import_files_path))
                
        except Exception as e:
            raise CommandError('Import files from "{0}" failed with error: {1}'.format(import_files_path, e))

