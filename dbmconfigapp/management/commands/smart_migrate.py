import os, re, shutil, sys
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db.migrations.loader import MigrationLoader
from django.db import connections
from dbmconfigapp import utils
from dbmconfigapp.models import MigrationManager, VersionManager
from django.db.migrations.writer import MigrationWriter
from django.db.migrations import writer
from configcenter import settings

"""
Version: 19.2
Update: added fix to run authccenter first before removing 17.1 content types (eran mazuz Apr 30, 2019)

Version: 18.1
Update: support --forward (quick mode) and --dry-run (tbener Sep 6, 2017)

Version: 17.1 CU2
Update (3/2018): support backward to last CU.
        --backward-to-ga switch still does as it says - backward to GA. 
        but in case of upgrade we compute the backward destination, which can be either GA or CU.
        Note that we're using settings.VERSION rather than get_param(version) to support CUs - 18.11 means 18.1 CU1
        PR is not indicated but if mig_helper.is_upgrade = False then it is a PR (or in dev, but anyway no backward involved)
Update: add nodebug support. Call "smart_migrate nodebug" to simulate real environment during dev (tbener Feb 4, 2018).
        Fix is_upgrade to be True only for Major versions (tbener Feb 4, 2018).
Update: (17.1 CU1) support --forward (quick mode) and --dry-run (tbener Sep 6, 2017)
"""

#############################
# Migrate.py file path:
# C:\Python27-11\Lib\site-packages\django\core\management\commands\migrate.py
# (For call_command investigations)
#############################

"""
For shell:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from dbmconfigapp.management.commands.smart_migrate import MigrationHelper
mh = MigrationHelper()
"""

regex_mig = r'^\d{4}_'

from django.contrib.contenttypes.models import ContentType
def remove_stale_models(from_ver=0, to_ver=0):
    # 17.1 CU1 adds the below modules.
    # When backward, we need to remove them from ContenType table manually (Django doesn't do that)
    if float(from_ver)>=17.11 and float(to_ver)<17.11:
        call_command('migrate','authccenter',  interactive=settings.DEBUG)

        #remove_content_type('dbmconfigapp', 'ehragentbaseurl')
        #remove_content_type('externalapps', 'installationprofile')
        #remove_content_type('dbmconfigapp', 'versionmanager')

def remove_content_type(appName, modelName):
    content_type = ContentType.objects.filter(app_label=appName, model=modelName)
    print("Removing ContentType: {0} - {1}".format(appName, modelName))
    if content_type.exists():
        content_type.delete()

class Command(BaseCommand):
    option_list = BaseCommand.stealth_options + (
        make_option('--no-sql-create', action='store_false', dest='no_sql_create', default=False,
            help="Do not populate views and procedures in the end of the process."),
        make_option('--empty', action='store_true', dest='empty', default=False,
            help="Create an empty migration."),
        make_option('--backward-to-ga', action='store_true', dest='backward_to_ga', default=False,
            help="Migrate back to GA (used for uninstall patches)."),
        make_option('--dry-run', action='store_true', dest='dry_run', default=False,
            help="Don't perform actual migrations and files modifications."),
        make_option('--status', action='store_true', dest='status', default=False,
            help="Display the migration status of every application."),
        # if DEBUG and not dry-run, smart_migrate will run in quick mode                                     
        make_option('--quick', action='store_true', dest='quick_mode', default=False,
            help="Quick mode - default migration (avoid version and backward detection)."),
    )
    
    """
    Options notes:
    --backward-to-ga and --status disable quick_mode
    Debug Mode (of the Django project) sets quick_mode=True, unless --dry-run
    """
    
    help = 'Perform CCenter migrations'
    usage_str = "Usage: ./manage.py smart_migrate [nodebug] [app1, app2...] | [[--empty] | [--backward-to-ga] | [--no-sql-create] | [--quick] | [--status] | [--dry-run]]"


    def handle(self, *app_labels, **options):
        self.no_sql_create = options.pop('no_sql_create', False)
        self.empty = options.pop('empty', False)
        self.backward_to_ga = options.pop('backward_to_ga', False)
        self.dry_run = options.pop('dry_run', False)
        self.status = options.pop('status', False)
        self.quick_mode = options.pop('quick_mode', False) 
                
        if self.empty:
            writer.MigrationWriter = EmptyMigrationWriter
            call_command("makemigrations", empty=True, *app_labels, **options)
            return
        
        if self.backward_to_ga or self.status:
            if self.quick_mode:
                self.quick_mode = False
                print("Quick Mode is disabled if --backward-to-ga or --status is on.")
        else:
            if settings.DEBUG:
                # if debug - set quick_mode unless 'nodebug' sent
                if 'nodebug' in app_labels:
                    # nodebug must be first
                    app_labels = app_labels[1:]
                elif not self.dry_run:
                    self.quick_mode = True

        if self.quick_mode:
            print("Quick Mode enabled. Skipping migrations analyzing.")
            
        if not self.quick_mode:
            mig_helper = MigrationHelper(dry_run=self.dry_run)
        
            if self.status:
                mig_helper.show_status()
                return
            
            if not self.no_sql_create and settings.IS_MAJOR:
                utils.set_compatibility_level()
                
            if not mig_helper.init_from_sparrow():
                if self.backward_to_ga:
                    # Specific command to backward to GA
                    mig_helper.retain_backward_migrations = True
                    mig_helper.backward_to_ga()
                    # If backward to GA was requested  then exit now
                    return
                
                elif mig_helper.is_upgrade:
                    # Compute the backward destination version automatically (CU ot GA)
                    mig_helper.backward_migration()
        
        ###############################
        # MAIN MIGRATION
        print("Starting forward migration...")                        
        if self.quick_mode:
            call_command('migrate', interactive=settings.DEBUG, *app_labels, **options)
        else:
            mig_helper.migrate(*app_labels, **options)
        ###############################
            
        if not self.quick_mode:
            if mig_helper.is_upgrade:
                print("")
                # This is a new version - update the MigrationManager table.
                mig_helper.update_migration_manager_table()
            
            if not settings.IS_MAJOR:
                # This is NOT a Major version - we need to copy all patch migrations to the shared folder. 
                mig_helper.copy_files_to_shared_folder()

            mig_helper.update_version_manager()

        if not self.no_sql_create and not self.dry_run:
            utils.populate_sql()



class EmptyMigrationWriter(MigrationWriter):
    def as_string(self):
        writer.MIGRATION_TEMPLATE = EMPTY_MIGRATION_TEMPLATE
        s = MigrationWriter.as_string(self)
        s = s.replace("APP_LABEL", self.migration.app_label)
        return s.replace('## VER ##', "VERSION = '%s'" % settings.VERSION)
    
    @property
    def filename(self):
        return "%s.py" % self.migration.name


EMPTY_MIGRATION_TEMPLATE = """\
# -*- coding: utf-8 -*-
# Auto generated using CCenter command smart_migrate
from __future__ import unicode_literals

from django.db import migrations
%(imports)s
## VER ##

def forward(apps, schema_editor):
    # ModelName = apps.get_model("APP_LABEL", "ModelName")
    pass

def backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):
%(replaces_str)s
    dependencies = [
%(dependencies)s\
    ]

    operations = [
        migrations.RunPython(forward, backward),
%(operations)s\
    ]
"""


# apps_info = {}
#    'app_name': AppInfo

class AppInfo:
    
    def __init__(self, name="", ga_migration=""):
        self.name = name                        # dbm app name
        self.ga_migration = ga_migration        # a string representing the GA migration name
        self.applied_migrations = []            # a list of applied migrations, including patch migrations
        self.disk_migrations = []               # a list of migrations that found on disk BUT WERE NOT APPLIED
        self.patch_migrations = []              # a list of applied migrations after GA - patch means SP\CU and HF\PR 
        self.needs_backward = False              # if True - special handling is required to un-apply patch migrations and move forward
        self.migrations_to_backward = []         # a list. if needed, those will be the migrations to backward
        
    def migrations_path(self, migration=None):
        return os.path.join(settings.PROJECT_DIR, self.name, "migrations", "{mig}.py".format(mig=migration) if migration else "")
    
    def shared_folder_path(self):
        return os.path.join(settings.CCENTER_SHARED_FOLDER, "migrations", self.name)
    
    def search_folders(self):
        # return list of tuples (folder name, folder path)
        return [
            ("Shared folder", os.path.join(settings.CCENTER_SHARED_FOLDER, "migrations", self.name)),
            ("Store", os.path.join(settings.PROJECT_DIR, self.name, "migrations", "store"))
            ]



class MigrationHelper:
    """
    Takes care of migrations before and after GA for upgrade purposes.
              
    When initializing, it reads all migrations and identifies the following for every App:
    1. Applied migrations
    2. Unapplied migrations
    3. GA migration
    4. Post GA migrations (named: Patch migrations)
    
    Calling backward_migration() or backward_to_ga() takes care of:
    1. Getting the missing files from the shared folder or from the store if needed
    2. Backward migration
    3. Deleting the reverted migrations from disk (required for continuing the migration on upgrade)   
    """
    

    
    def __init__(self, dry_run=False):
        self.is_upgrade = False
        self.is_synced = False      # indicate whether the migration lists is updated. used in update_migrations_info which takes time.
                                    # need to explicitly set if an external migration command ran
        self.apps_info = {}         # key: app name, value: AppInfo class
        self.dry_run = dry_run

        self.init_loader()

        self.installed_ga = 7.0
        self.installed_cu = 0.0
        
        self.compute_installed_version()            # initiate installed_ga and installed_cu
        
        self.last_installed_version = self.installed_cu or self.installed_ga
        
        self.update_migrations_info()
        
        print("\nInstalled version: %s" % self.last_installed_version)
        print("New version: %s\n" % settings.VERSION)
        
        # is_upgrade means it's a different version with backward involved.
        self.is_upgrade = (float(settings.VERSION) > self.last_installed_version) 
                        
    
    def init_loader(self):
        connection = connections['default']
        self.loader = MigrationLoader(connection)
    
    def show_status(self):
        
        template = "{0:13} | {1:40} | {2:40} | {3:4}"
        print (template.format("\nApplication", "GA Migration", "Last Applied", "Has new"))
        print("-" * 110)

        for app in self.apps_info.values():
            print (template.format(app.name, app.ga_migration[:40], app.applied_migrations[0][:40], "Yes" if app.disk_migrations else "No"))
    
    
    def migrate(self, *app_labels, **options):
        if not self.dry_run:
            call_command('migrate', interactive=settings.DEBUG, *app_labels, **options)
        self.is_synced = False
    
    # for every app:
    # 1. fill applied_migrations
    #         sort it desc
    # 2. fill patch_migrations
    # 3. fill disk_migrations
    # IMPORTANT: This method needs to be called every time a migration is run, before using the relevant data!
    def update_migrations_info(self):
        if self.is_synced:
            return
        
        print("Updating applied migrations index")
        
        self.init_loader()
                
        sys_apps = set(['admin', 'sessions', 'auth', 'sites', 'contenttypes'])
        dbm_apps = self.loader.migrated_apps - sys_apps
        
        # get all dbm apps
        for app in dbm_apps:
            self.apps_info[app] = AppInfo(app)
        
        # set ga_migration for every app
        for mig in MigrationManager.objects.filter(version=self.installed_ga):
            self.apps_info[mig.app_name].ga_migration=mig.ga_migration
            
        
        # assign applied migrations by app
        for app, mig in self.loader.applied_migrations:
            if app in self.apps_info:
                self.apps_info[app].applied_migrations.append(mig)
                
        # sort (reversed) the applied_migrations
        [app_info.applied_migrations.sort(reverse=True) for app_info in self.apps_info.values()]

        for app_info in self.apps_info.values():
            if app_info.ga_migration in app_info.applied_migrations:
                for mig in app_info.applied_migrations:
                    if mig > app_info.ga_migration:
                        app_info.patch_migrations.append(mig)
                
        disk_migrations = set(self.loader.disk_migrations.keys()) - self.loader.applied_migrations
    
        # list unapplied migrations by app
        for app, mig in disk_migrations:
            if self.apps_info.has_key(app):
                self.apps_info[app].disk_migrations.append(mig)
    
        self.is_synced = True
    
            
    # Run the fake migrations if needed.
    # Return True if it did. False if it didn't.
    def init_from_sparrow(self):
        if self.loader.applied_migrations:
            return False
        
        print("Initialize database")
        # apps to run fake init migration
        cc_apps = ['dbmconfigapp','federation', 'security', 'externalapps', 'via','dataloading']
        
        if self.dry_run:
            print("Run fake migrations for %s" % ", ".join(cc_apps))
        else:
            for app_name in cc_apps:
                call_command('migrate', app_name, "0001", fake=True, interactive=False)
        
        return True

    def is_model_exists(self, model_class):
        connection = connections["default"]
        return model_class._meta.db_table in connection.introspection.table_names()

    def is_major(self, version):
        try:
            version = 10*float(version)
            return int(version) == float(version)
        
        except:
            pass
        
        return False
    
    def compute_installed_version(self):
        dbmconfigapp_version_list = [float(m.version) for m in MigrationManager.objects.filter(app_name='dbmconfigapp') if (m.app_name, m.ga_migration) in self.loader.applied_migrations]
        dbmconfigapp_version_list.sort(reverse=True)

        for ver in dbmconfigapp_version_list:
            if self.is_major(ver):
                self.installed_ga = ver
                return
            elif not self.installed_cu:
                self.installed_cu = ver
            
    def get_installed_cu(self):
        # compute current GA according to the maximum version with applied GA migration
        return max([float(m.version) for m in MigrationManager.objects.filter(app_name='dbmconfigapp') if (m.app_name, m.ga_migration) in self.loader.applied_migrations] or [7.0])

    def get_installed_ga(self):
        # compute current GA according to the maximum version with applied GA migration
        return max([float(m.version) for m in MigrationManager.objects.filter(app_name='dbmconfigapp') if (m.app_name, m.ga_migration) in self.loader.applied_migrations] or [7.0])

    def update_version_manager(self, ver=settings.VERSION):

        print("Updating VersionManager table to %s" % ver)
        records = VersionManager.objects.all()
        if(records.exists()):
            rec = records[0]
            rec.version = ver;
        else:
            rec = VersionManager(version = ver);

        rec.save();
               
    def update_migration_manager_table(self):
        print("Updating MigrationManager table for %s" % settings.VERSION)
        self.update_migrations_info()
        
        if not self.dry_run:
            for app_info in self.apps_info.values():
                MigrationManager.objects.update_or_create(app_name=app_info.name, version=settings.VERSION, defaults={'ga_migration': app_info.applied_migrations[0]})

    
    # delete migration files that are before last applied migrations and NOT in db
    def delete_orphan_files(self, app_info, delete_after_ga=True):
        print('\tLooking for orphan files...')
        
        if not app_info.applied_migrations:
            print('\tNo orphan files.')
            return
    
        # get files before last applied which are not applied
        del_files = [f for f in os.listdir('%s/migrations' % app_info.name) 
                     if re.match(regex_mig, f)
                     and os.path.splitext(f)[0] < app_info.applied_migrations[0] 
                     and os.path.splitext(f)[0] in app_info.disk_migrations]
        
        if delete_after_ga:
            if app_info.ga_migration:
                # get files after ga
                del_files += [f for f in os.listdir('%s/migrations' % app_info.name) 
                     if re.match(regex_mig, f)
                     and os.path.splitext(f)[0] in app_info.patch_migrations]
        
        if del_files:
            for f in del_files:
                print('\tDeleting %s' % f)
                if not self.dry_run:
                    os.remove('%s/migrations/%s' % (app_info.name, f))
        else:
            print('\tNo orphan files.')
            
            
            
    def copy_files_to_shared_folder(self):
        
        print("Copying files to shared folder")
        print(os.path.join(settings.CCENTER_SHARED_FOLDER, 'migrations'))
        
        self.update_migrations_info()

        for app_info in self.apps_info.values():
            if app_info.patch_migrations:
                print("{0}: Copy {1:d} patch migrations to shared folder".format(app_info.name, len(app_info.patch_migrations)))
                if not self.dry_run:
                    if not os.path.exists(app_info.shared_folder_path()):
                        print("Creating folder: %s" % app_info.shared_folder_path())
                        os.makedirs(app_info.shared_folder_path())

                    for mig in app_info.patch_migrations:
                        mig_file = mig + ".py"
                        shutil.copy(os.path.join(app_info.migrations_path(), mig_file), os.path.join(app_info.shared_folder_path(), mig_file))
            else:
                print("{0}: No patch migrations to copy".format(app_info.name)) 
                
    
    def move_migrations(self, app, mig_list, folder, restore=False):
        if mig_list:
            src = os.path.join(settings.PROJECT_DIR, app, "migrations")
            dst = os.path.join(src, folder)
            # if restore - swap src and dst
            if restore:
                src, dst = dst, src
            # if dst path doesn't exist, create it (relevant only when restore = False)
            elif not os.path.exists(dst):
                print("Creating folder: %s" % dst)
                if not self.dry_run:
                    os.makedirs(dst)
            
            if restore:
                print("Restoring files from {0}".format(src))
            else:
                print("Moving files to {0}".format(dst))
                
            # MOVE the files
            for mig in mig_list:
                mig_file = mig + ".py"
                print("\t" + mig_file)
                if not self.dry_run:
                    shutil.move(os.path.join(src, mig_file), os.path.join(dst, mig_file))
                    mig_file = mig + ".pyc"
                    if os.path.isfile(os.path.join(src, mig_file)): os.remove(os.path.join(src, mig_file))
            # if restore - delete the folder
            if restore:
                if os.path.exists(src):
                    if os.listdir(src) == []:
                        print("Deleting empty folder: {0}".format(src))
                        if not self.dry_run:
                            os.rmdir(src)
                    else:
                        print("\nThe folder:\n{0}\n IS NOT EMPTY!!! This might indicate a problem. Please check.")
    
    
    def prepare_backward_migration_files(self, app_info):
        
        #self.delete_orphan_files(app_info, self.dry_run, False)
        
        print("Preparing backward migration files for: %s" % app_info.name)
                
        files_not_found = 0
        for mig in app_info.migrations_to_backward:
            if os.path.isfile(app_info.migrations_path(mig)):
                # this is the original location. this is ok, move on to the next file.
                break
            
            print('Migration does not exist: %s.\nLooking in the search folders...' % mig)
            
            # migration not found in original location - search in other folders
            found = False
            for (name, folder) in app_info.search_folders():
                backup_file = os.path.join(folder, "{0}.py".format(mig))
                print("Looking in {name} ({file})".format(name=name, file=backup_file))
                if os.path.isfile(backup_file):
                    print('Found. Copying...')
                    found = True
                    if not self.dry_run:
                        shutil.copy(backup_file, app_info.migrations_path())
                    break
                else:
                    print("Not found")
            
            if not found:
                files_not_found+=1
                print('*** Migration file %s.py is not found neither in local folder nor in any of the search folders\n' % mig)
        
        if files_not_found:
            # print('\nERROR: Migration files are missing. Any migration command will fail until the files above are restored.')
            raise CommandError('Migration files are missing. Any migration command will fail until the files above are restored.')


    def _backward_to_version(self, version):
        
        # set backward_destination for every app
        for mm in MigrationManager.objects.filter(version=version):
            self.apps_info[mm.app_name].backward_destination = mm.ga_migration # NOTE: ga_migration is just the field name in MigrationManager. It stands for the last migration for any version, inck CU
        
        # set migrations_to_backward for every app     
        for app_info in self.apps_info.values():
            app_info.migrations_to_backward = []
            for mig in app_info.applied_migrations:
                if mig > app_info.backward_destination:
                    app_info.migrations_to_backward.append(mig)
                else:
                    # since the list is sorted, we can break here
                    break
        
        # get only the apps that need backward
        apps = [app for app in self.apps_info.values() if app.migrations_to_backward]
        if not apps:
            print("No application needs backward migration.")
            return
        
        # Get the migrations files in place
        # and move unapplied migration as they can cause conflicts
        for app_info in apps:
            self.move_migrations(app_info.name, app_info.disk_migrations, "notapplied")
            self.prepare_backward_migration_files(app_info)
        
        print("Running backward migrations...\n")
        for app_info in apps:
            if not self.dry_run:
                call_command('migrate', app_info.name, app_info.backward_destination, interactive=False)
        
        print('\nDone. Moving patch migrations and restoring new migrations...')
        
        # Remove patch migrations
        # Restore disk migrations
        for app_info in apps:
            # move backward migrations (which supposed to be un-applied now)
            if not getattr(self, "retain_backward_migrations", False):
                self.move_migrations(app_info.name, app_info.migrations_to_backward, "patch_backward")
            # Restore disk migrations
            self.move_migrations(app_info.name, app_info.disk_migrations, "notapplied", restore=True)
        
        remove_stale_models(from_ver=self.last_installed_version, to_ver=version)
        self.is_synced = False
            
    
    def backward_to_ga(self):
        self._backward_to_version(self.installed_ga)
        
    
    # Automatically figure the version we need to backward to
    # rules are:
    # If upgrading to GA
    #    backward to installed GA
    # Else
    #    backward to installed CU
    def backward_migration(self):
        backward_to_ver = 0
        print("\nComputing backward version...")
        if self.is_major(settings.VERSION):
            print("Version {0} is major.".format(settings.VERSION))
            # upgrading to major
            # need backward to GA
            backward_to_ver = self.installed_ga
        else:
            print("Version {0} is not major.".format(settings.VERSION))
            # upgrading to CU
            # backward to installed CU or GA, whatever is installed
            backward_to_ver = self.last_installed_version
        
        print("Should backward to {0}\n".format(backward_to_ver))
        if backward_to_ver:
            self._backward_to_version(backward_to_ver)

        
        
        
        