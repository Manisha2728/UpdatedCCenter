#-------------------------------------------------------------------------------
# Name:        migration_upgrade.py
# Purpose:    Handle CCenter migrations, whether it is a new installation or a major update
#
# Author:      TBener
#
# Created:     23/09/2014
#-------------------------------------------------------------------------------

# List of all applications
all_apps = ['dbmconfigapp','federation', 'security', 'externalapps', 'via','dataloading']

import os, glob
import sys
import re
import shutil
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'configcenter.settings'

from south.models import MigrationHistory
from django.core.management import call_command
from django.db import connections, DEFAULT_DB_ALIAS

from configcenter import settings
from dbmconfigapp.models.version_manager import MigrationManager
from dbmconfigapp import utils

regex_mig_py = r'^\d{4}_(.*)\.(py)$' 
regex_mig = r'^\d{4}_'

import django
django.setup()


def model_exist(model_class):
    connection = connections[DEFAULT_DB_ALIAS]
    return model_class._meta.db_table in connection.introspection.table_names()

def get_last_migration(app_name):
    list_migrations = list(m.migration for m in MigrationHistory.objects.filter(app_name = app_name))
    if not list_migrations:
        return None, None
    return list(list_migrations)[-1], list_migrations 

def get_migration_list(app_name):
    return list(m.migration for m in MigrationHistory.objects.filter(app_name = app_name))

def get_migrations_info(app_name):
    ga_migration = get_ga_migration(app_name)
    list_migrations = list(m.migration for m in MigrationHistory.objects.filter(app_name = app_name))
    ga_index = list_migrations.index(ga_migration)
    ga_migration_list = list_migrations[:ga_index]
    hf_migration_list = list_migrations[ga_index+1:]
    return ga_migration, ga_migration_list, hf_migration_list

def update_ga_migration(app_name):
    vm = MigrationManager.objects.filter(app_name=app_name)
    if vm:
        vm = vm[0]
    else:
        vm = MigrationManager()
        vm.app_name = app_name
    vm.ga_migration = get_last_migration(app_name)[0]
    vm.version = settings.VERSION
    vm.save()

def need_syncdb():
    print('Checking if syncdb required...')
    connection = connections[DEFAULT_DB_ALIAS]
    return bool(not connection.introspection.table_names())

def is_db_ready():
    print('Checking if CCenter database is ready...')
    try:
        connection = connections[DEFAULT_DB_ALIAS]
        return bool(MigrationHistory.objects.count())
    except:
        return False

# delete migration files that are before last applied migrations and NOT in db
# AND files that are after GA migration and IN the db (for the case of upgrading a non-CCenter role server before CCenter role)
def delete_orphan_files(app_name, debug=False, delete_after_ga=True):
    print('\tLooking for orphan files...')
    last_applied_migration, list_migrations = get_last_migration(app_name)
    if not list_migrations:
        print('\tNo orphan files.')
        return
    
    del_files = [f for f in os.listdir('%s/migrations' % app_name) 
                 if re.match(regex_mig, f)
                 and os.path.splitext(f)[0] < last_applied_migration 
                 and os.path.splitext(f)[0] not in list_migrations]
    
    if delete_after_ga:
        ga_migration = get_ga_migration(app_name)
        if ga_migration:
            del_files += [f for f in os.listdir('%s/migrations' % app_name) 
                     if re.match(regex_mig, f)
                     and os.path.splitext(f)[0] > ga_migration 
                     and os.path.splitext(f)[0] in list_migrations]

    if del_files:                 
        for f in del_files:
            print('\tDeleting %s' % f)
            if not debug:
                os.remove('%s/migrations/%s' % (app_name, f))
    else:
        print('\tNo orphan files.')
        
def get_ga_migration(app_name):
    if model_exist(MigrationManager):
        vm = MigrationManager.objects.filter(app_name=app_name)
        if vm:
            return vm[0].ga_migration
    elif app_name=='dbmconfigapp':
        print('Version Management is not yet supported in the database. GA Migration will be derived hard-coded')
        last_applied_migration, list_migrations = get_last_migration(app_name)
        if not list_migrations:
            return None
        last_num = int(last_applied_migration[:4])
        if last_num >= 146:
            print('\tEagle installation detected')
            return '0146_load_vpoppol_data__and_model_descriptor'
        if last_num >= 50:
            print('\tFalcon installation detected')
            return '0050_auto__add_field_labchartdisplayoptions_report_max_rows_in_regular_col_'
        
    return None

def copy_files_to_shared_folder(app_name):
    # Copy migration files that are above GA
    ga_migration = get_ga_migration(app_name)
    hf_files = [f for f in os.listdir('%s/migrations' % app_name) 
                 if re.match(regex_mig_py, f)
                 and os.path.splitext(f)[0] > ga_migration]
    if hf_files: 
        target_folder = os.path.join(settings.CCENTER_SHARED_FOLDER, 'migrations/%s' % app_name)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        print('Destination: %s' % target_folder)
        for f in hf_files:
            print('Copy %s' % f)
            shutil.copy(os.path.join('%s/migrations/%s' % (app_name, f)), target_folder)
    else:
        print('No files to copy')
    


def prepare_backward_migration(app_name, debug=False):
    global APP_INFO
    
    delete_orphan_files(app_name, debug, False)
    
    if not APP_INFO[app_name].last_ga_migration:
        # this is not an error - could be new app
        print('\tNo record found for last GA migration of %s' % app_name)
        return 
    
    last_applied_migration, list_migrations = get_last_migration(app_name)

    template = "{0:13} {1:10}"
    print (template.format('Last applied:', last_applied_migration))
    print (template.format('GA:', APP_INFO[app_name].last_ga_migration))

    if last_applied_migration == APP_INFO[app_name].last_ga_migration:
        print('\tNo SP/HF seems to be installed')
        return
    
    APP_INFO[app_name].need_backward_migration = True
    
    # get list of HF migrations
    i_ga = list_migrations.index(APP_INFO[app_name].last_ga_migration)
    APP_INFO[app_name].hf_migrations = list_migrations[i_ga+1:]     # returns all migration after GA
    # another way of getting hf migrations
    #hf_migrations = [mig.migration for mig in MigrationHistory.objects.filter(app_name=app_name, migration__gt=last_ga_migration)]
    
    backup_folder = os.path.join(settings.CCENTER_SHARED_FOLDER, 'migrations/%s' % app_name)
    files_not_found = 0
    for mig in APP_INFO[app_name].hf_migrations:
        # search for the file in local folder
        if not os.path.isfile('%s/migrations/%s.py' % (app_name, mig)):
            print('Migration does not exist: %s.\nLooking in shared folder...' % mig)
            backup_file = '%s/%s.py' % (backup_folder, mig)
            if os.path.isfile(backup_file):
                print('Found. Copying...')
                if not debug:
                    shutil.copy(backup_file, '%s/migrations' % app_name)
            else:
                files_not_found+=1
                print('*** Migration file %s.py is not found neither in local folder nor in shared folder\n' % mig)
                
    if files_not_found:
        print('\nERROR: Migration files are missing. Any migration command will fail until the files above are restored.')
        print('The files are expected to be either in %s or in shared folder: %s' % ('migrations/%s' % app_name, backup_folder))
        if not debug:
            sys.exit(1)
    

def backward_migration(debug_mode=False):
    global APP_INFO
    init_apps_info()
    
    # Copy all missing files before running any migration
    for app_name in all_apps:
        print('\nApp: %s' % app_name)
        prepare_backward_migration(app_name, debug=debug_mode)
    
    # Run migrations for all applications before deleting any files
    for app_name, app_info in APP_INFO.items():
        if app_info.need_backward_migration:
            print('\tRunning migration...')
            if not debug_mode:
                call_command('migrate', interactive = False, app=app_name, target=app_info.last_ga_migration)
    
    print('\tDone.\n\tRemoving all SP/HF migration files...')
    
    # Remove the SP/HF files
    for app_name, app_info in APP_INFO.items():
        for mig in app_info.hf_migrations:
            print('\tDeleting %s' % ('%s/migrations/%s.py' % (app_name, mig)))
            if not debug_mode:
                # delete the file
                os.remove('%s/migrations/%s.py' % (app_name, mig))
                # delete the pyc if exists
                if os.path.isfile('%s/migrations/%s.pyc' % (app_name, mig)): os.remove('%s/migrations/%s.pyc' % (app_name, mig))
    
    print('\nBackward migration completed.')

APP_INFO = {}

class AppInfo:
    last_ga_migration = None
    hf_migrations = []
    need_backward_migration = False
    
def init_apps_info():
    global APP_INFO
    
    for app_name in all_apps:
        app_info = AppInfo()
        app_info.last_ga_migration = get_ga_migration(app_name)
        APP_INFO[app_name] = app_info
        

def main():
    apps = all_apps
    
    backward_to_ga = False             # if True: will check for GA version and migrate backward if needed
    syncdb = False              # if True: will check and perform Syncdb if needed
    version_update = False   # if True: will not update the last migration as GA version (use for dev and HF migration)
    collect_static = False
    clean_files = False
    check_db = False
    create_sql_views = True

    # debug_mode: If True - no real operation is done. No migrations, no file renaming etc.
    debug_mode = False
        
    for arg in sys.argv:
        if arg.lower() == 'debug': debug_mode = True
        elif arg.lower() == 'backward_to_ga': backward_to_ga = True
        elif arg.lower() == 'syncdb': syncdb = True
        elif arg.lower() == 'version_update': version_update = True
        elif arg.lower() == 'collect_static': collect_static = True
        elif arg.lower() == 'clean': clean_files = True
        elif arg.lower() == 'check_db': check_db = True
        elif arg.lower() == 'no_sql_create': create_sql_views = False

    if debug_mode:
        print('\n**\nRUNNING DEBUG MODE (No real migrations and file systems operations)\n**\n')
    
    if check_db and not is_db_ready(): 
        print('The argument check_db is on. Database is not ready. Exiting...')
        return
    
    if syncdb:
        if need_syncdb():
            collect_static = True
            if debug_mode:
                print('Syncdb...')
            else:
                call_command('syncdb', interactive=False)
    elif backward_to_ga:
        backward_migration(debug_mode)
        # We need to finish here. Otherwise next migration won't work properly due to some cache
        # saved by south.
        # To continue call the script again
        return

    if clean_files:
        print("Deleting migration files that are not part of the GA release...")
        for app_name in apps:
            delete_orphan_files(app_name, debug_mode)
        return

    if debug_mode:
        print('Run migration...')
    else:
        for app_name in apps:
            call_command('migrate', interactive = False, app=app_name)

    if not version_update:
        print('Copy migrations to shared folder')
        if not debug_mode:
            for app_name in apps:
                copy_files_to_shared_folder(app_name)
            
    else:
        for app_name in apps:
            print('Writing version details for %s' % app_name)
            if not debug_mode:
                update_ga_migration(app_name)
                
    if create_sql_views:
        print('(Re)creating SQL views and procedures')
        if not debug_mode:
            utils.populate_sql()

    if collect_static:
        print("Run collect static")
        call_command('collectstatic', interactive=False)


if __name__ == '__main__':
    
    main()
