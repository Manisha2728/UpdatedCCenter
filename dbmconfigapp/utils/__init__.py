from configcenter import settings
import os
import logging
import sys
from os import listdir
from os.path import isfile, join
from django.db import connection, transaction

def get_hf_file(filename, search_local=True):
    ### Searching for the file, first in Project local folder (if search_local=True)
    ### and then in shared folder.  
    ### Returns a tuple - found: True if the file is found, and the full file path (whether it is found or not)
    found = False
    if search_local:
        hf_data_file = os.path.join(settings.PROJECT_DIR, filename)
        found = os.path.isfile(hf_data_file)
        
    if not found and hasattr(settings, 'HF_DIR'):
        hf_data_file = os.path.join(settings.HF_DIR, filename)
        found = os.path.isfile(hf_data_file)
        
    return found, os.path.normpath(hf_data_file) # if found else None

def set_compatibility_level():
    print("\nUpdating SQL compatibility level")
    with connection.cursor() as cursor:
        cursor.execute("SELECT [compatibility_level] FROM sys.databases WHERE name = 'master'")
        level=cursor.fetchone()[0]

        cursor.execute("ALTER DATABASE " + settings.DATABASES['default']['NAME'] + " SET COMPATIBILITY_LEVEL = " + str(level))


@transaction.atomic
def populate_sql():
    print("\nPopulating SQL")

    # Get an instance of a logger
    logger=logging.getLogger('django')
    engine = settings.DATABASES['default']['ENGINE']
    
    # CREATE ALL VIEWS AND PROCEDURES
    files_dir = os.path.normpath(os.path.join(settings.PROJECT_DIR, 'dbmconfigapp/sql/'+engine))
        
    if not os.path.exists(files_dir):
        logger.warning("There is no sql data for engine '%s'" % engine)
        return
    
    print('  Creating/updating views and stored procedures...')
    sql_files = [ f for f in listdir(files_dir) if isfile(join(files_dir,f)) ]
    cursor = connection.cursor()

    for sql_file in sql_files:
        try:                
            path = os.path.normpath(os.path.join(files_dir,sql_file))
            logger.debug(path)
            if os.path.exists(path):
                logger.debug("Loading initial SQL data from '%s'" % path)
                f = open(path)
                sql = f.read()
                f.close()
                cursor.execute(sql)
        except Exception as e:
            sys.stderr.write("Failed to install custom SQL file '%s': %s\n" % \
                                (path, e))
            import traceback
            traceback.print_exc()
            
    print('  Finished SQL population.')
            