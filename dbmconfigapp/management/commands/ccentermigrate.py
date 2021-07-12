import logging
import os
import shutil
from importlib import import_module

from django.apps import apps
from django.core.management import BaseCommand, CommandError, call_command
from django.core.management.sql import emit_post_migrate_signal, emit_pre_migrate_signal
from django.db import connection, models, transaction
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from django.utils.encoding import python_2_unicode_compatible
from django.utils.module_loading import module_has_submodule

from configcenter import settings
from configcenter.settings import PROJECT_DIR
from dbmconfigapp.models import MigrationManager, VersionManager

INSTALLATION_START = 0  # Pre install
INSTALL_PR = 1  # When PR installing PR
VERIFY_PR = 2  # Verify PR to uninstall.
REMOVE_PR = 3  # Removing PR migrations.
VERIFY_CU = 4  # Verify CU to remove.
REMOVE_CU = 5  # Remove CU migrations.
RUN_MIGRATE = 6  # Upgrade CCenter to new version.
POST_INSTALL = 7  # Post install
PREPARE_UPGRADE = 8  # Prepare CCenter for Upgrade.
INIT_FROM_ZERO = 9  # Initialize migrations for sparrow

MIGRATION_STAGES = (
    (INSTALLATION_START, "Start installation tasks"),
    (INSTALL_PR, "Install PR"),
    (VERIFY_PR, "Verify PR installed"),
    (REMOVE_PR, "Remove PR"),
    (VERIFY_CU, "Verify CU installed"),
    (REMOVE_CU, "Remove CU"),
    (RUN_MIGRATE, "Upgrade CCenter"),
    (POST_INSTALL, "End installation tasks"),
    (PREPARE_UPGRADE, "Prepare CCenter for Upgrade"),
    (INIT_FROM_ZERO, "Initialize CCenter for the first time"),
)

SYS_APP = {'admin', 'sessions', 'auth', 'sites', 'contenttypes'}


class MigrationProcess(object):
    def __init__(self, stdout, stderr, connection):
        self.stdout = stdout
        self.stderr = stderr
        self.executor = MigrationExecutor(connection, self.migration_progress_callback)
        self.connection = connection

    def migrate_django_apps(self):
        targets = set()

        for app in SYS_APP:
            targets = targets.union(self.executor.loader.graph.root_nodes(app))

        self.stdout.write('\n')
        self.stdout.write("Initialize Django_apps")
        self.stdout.write("-" * 30)
        self.stdout.write('\n')

        self.migrate(targets)

    def init_from_zero(self):
        if self.executor.recorder.applied_migrations():
            return

        #ccenter_apps = self.executor.loader.migrated_apps - SYS_APP
        #targets = set()

        #for app in ccenter_apps:
        #    targets = targets.union(self.executor.loader.graph.root_nodes(app))

        self.stdout.write('\n')
        self.stdout.write("Initialize CCenter for the first time.")
        self.stdout.write("-" * 30)
        self.stdout.write('\n')

        #self.migrate()
        call_command('migrate')

    def migrate(self, targets=None, fake=False):
        if not targets:
            ccenter_apps = self.executor.loader.migrated_apps - SYS_APP
            targets = set()

            for app in ccenter_apps:
                targets = targets.union(self.executor.loader.graph.leaf_nodes(app))

        self.stdout.write('\n')
        self.stdout.write("Migration Destination:")
        self.stdout.write("-" * 30)

        for app, migraiton in targets:
            self.stdout.write("- %s: %s" % (app, migraiton))

        plan = self.executor.migration_plan(targets)

        self.stdout.write('\n')
        self.stdout.write("Migrate:")
        self.stdout.write("-" * 30)

        if not plan:
            self.stdout.write("  No migrations to apply.")
            self.stdout.write('\n')
            return

        self.migration_count = len(plan)
        self.migration_changed = 0

        self.executor.migrate(targets, plan, fake)
        self.stdout.write('\n')

    def migration_progress_callback(self, action, migration, fake=False):
        if action == "apply_start":
            self.migration_changed += 1
            self.stdout.write("(%s/%s)  Applying %s..." % (self.migration_changed, self.migration_count, migration),
                              ending="")
            self.stdout.flush()
        elif action == "apply_success":
            if fake:
                self.stdout.write(" FAKED.")
            else:
                self.stdout.write(" OK.")

        elif action == "unapply_start":
            self.migration_changed += 1
            self.stdout.write("(%s/%s)  Unapplying %s..." % (self.migration_changed, self.migration_count,migration),
                              ending="")
            self.stdout.flush()
        elif action == "unapply_success":
            if fake:
                self.stdout.write(" FAKED.")
            else:
                self.stdout.write(" OK.")


class MigrationsOrganizer(object):
    migration_paths = {
        'Shared folder': os.path.join(settings.CCENTER_SHARED_FOLDER, "migrations", "%s", "%s.py"),
        'Application notapplied folder': os.path.join(PROJECT_DIR, "%s", "migrations", "notapplied", "%s.py"),
        'Application patch_backward folder': os.path.join(PROJECT_DIR, "%s", "migrations", "patch_backward", "%s.py"),
        'Application store folder': os.path.join(PROJECT_DIR, "%s", "migrations", "store", "%s.py"),

    }

    app_migration_path = os.path.join(PROJECT_DIR, "%s", "migrations", "%s.py")

    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr

    def move_migration_to(self, location, app, migration):
        """
        Move the migration to specified location from the migrations folder.
        :param location: one of the locations migration can be found.
        :param app: app of the migration.
        :param migration: the migration name.
        """
        destination_migration_path = self.migration_paths[location] % (app, migration)
        source_migration_path = self.app_migration_path % (app, migration)
        destination_migration_folder_path = os.path.dirname(destination_migration_path)
        if not os.path.exists(destination_migration_folder_path):
            os.makedirs(destination_migration_folder_path)
        self.stdout.write("Move '%s' to '%s'... " % (migration, location.lower()), ending='')
        shutil.move(source_migration_path, destination_migration_path)
        self.stdout.write("Done.")

    def copy_migration_to(self, location, app, migration):
        """
        Copy the migration to specified location from the migrations folder.
        :param location: one of the locations migration can be found.
        :param app: app of the migration.
        :param migration: the migration name.
        """
        destination_migration_path = self.migration_paths[location] % (app, migration)
        source_migration_path = self.app_migration_path % (app, migration)
        destination_migration_folder_path = os.path.dirname(destination_migration_path)
        if not os.path.exists(destination_migration_folder_path):
            os.makedirs(destination_migration_folder_path)
        self.stdout.write("Copy '%s' to '%s'... " % (migration, location.lower()), ending='')
        shutil.copy(source_migration_path, destination_migration_path)
        self.stdout.write("Done.")

    def find_migration(self, app, migration):
        """
        Search for the migrations in the specified locations,
        throw error if migration not found in any of the locations.
        :param app: The migration app.
        :param migration: The migration name.
        :return: Return The migration path.
        """
        self.stdout.write("Searching migration %s of %s application:" % (migration, app))

        # Check each of the search paths for the migration.
        for name in self.migration_paths:
            migration_path = self.migration_paths[name] % (app, migration)
            self.stdout.write("- %s: " % name, ending='')
            if os.path.exists(migration_path):
                self.stdout.write(migration_path)
                self.stdout.write("Found.")
                return migration_path
            self.stdout.write("Not found.")

        raise CommandError("migration %s of %s application not found." % (migration, app))

    def restore_migration(self, app, migration):
        """
        Find and restore the migration.
        :param app: app of the migration.
        :param migration: the migration name.
        """
        source_migration_path = self.find_migration(app, migration)
        destination_migration_path = self.app_migration_path % (app, migration)
        self.stdout.write(
            "migration %s of %s application found in %s." % (migration, app, source_migration_path))
        self.stdout.write("Restore migration '%s'... " % migration, ending='')
        shutil.copy(source_migration_path, destination_migration_path)
        self.stdout.write("Done.")


class Command(BaseCommand):
    help = " Restore all the required migrations"

    app_migration_path = os.path.join(PROJECT_DIR, "%s", "migrations", "%s.py")

    @python_2_unicode_compatible
    class CCenterMigrationManager(models.Model):

        installation_stage = models.IntegerField(default=INSTALLATION_START, choices=MIGRATION_STAGES)
        pr_installed = models.BooleanField(default=True)
        version = models.FloatField(default=0.0)
        version_new = models.FloatField(default=0.0)

        class Meta:
            app_label = "migration manager"
            db_table = "ccenter_migration_manager"

        def __str__(self):
            return "Migration %s for %s" % (self.name, self.app)

    def update_database_compatibility_level(self):
        """
        Update the compatibility level (which SQL server version the database is compatible with) of CCenter database.
        """

        self.stdout.write('\n')
        self.stdout.write("Upgrade CCenter database compatibility level")
        self.stdout.write("-" * 30)
        self.stdout.write('\n')

        self.stdout.write("Checking compatibility level:")

        # Get the sql server compatibility level.
        self.stdout.write("- SQL server: ", ending='')

        with connection.cursor() as cursor:
            cursor.execute("SELECT [compatibility_level] FROM sys.databases WHERE name = 'master'")
            record = cursor.fetchone()

        if record is None:
            self.stdout.write("Error.")
            raise CommandError('Error in updating CCenter database compatibility level')
        else:
            sql_server_level = record[0]
            self.stdout.write(str(sql_server_level))

        # Get the CCenter database compatibility level.
        self.stdout.write("- CCenter database: ", ending='')

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT [compatibility_level] FROM sys.databases WHERE name = '%s'" % settings.DATABASES['default'][
                    'NAME'])
            record = cursor.fetchone()

        if record is None:
            self.stdout.write("Error.")
            raise CommandError('Error in updating CCenter database compatibility level')
        else:
            ccenter_database_level = record[0]
            self.stdout.write(str(ccenter_database_level))

        # Update the CCenter database compatibility level.
        if ccenter_database_level == sql_server_level:
            self.stdout.write("No need to update CCenter database compatibility level.")

        else:
            self.stdout.write(
                "Updating CCenter CCenter database compatibility level from %s to %s..." % (ccenter_database_level,
                                                                                            sql_server_level))
            with connection.cursor() as cursor:
                cursor.execute(
                    "ALTER DATABASE " + settings.DATABASES['default']['NAME'] + " SET COMPATIBILITY_LEVEL = " + str(
                        sql_server_level))
            self.stdout.write('Done.')

    def migration_manager_table_exists(self):

        return MigrationManager._meta.db_table in  self.connection.introspection.get_table_list(
                self.connection.cursor())

    def get_migration_manager(self):
        """
        Load the migration manager.
        """
        # Get the migration manager data if it exists in database.
        if self.CCenterMigrationManager._meta.db_table in self.connection.introspection.get_table_list(
                self.connection.cursor()):

            migration_manager = self.CCenterMigrationManager.objects.first()

            # Create and initialize the migration manager if it not already initialized.
            if migration_manager:
                self.migration_manager = migration_manager
                if self.migration_manager.version == 0.0:
                    self.migration_manager.version = self.compute_installed_version()
                if self.migration_manager.version_new == 0.0:
                    self.migration_manager.version_new = float(settings.VERSION)
                return
        else:

            # Create the migration manager model in the database.
            with self.connection.schema_editor() as editor:
                editor.create_model(self.CCenterMigrationManager)

        # Initialize the migration manager.
        self.migration_manager = self.CCenterMigrationManager()
        self.migration_manager.version = self.compute_installed_version()
        self.migration_manager.version_new = float(settings.VERSION)
        self.migration_manager.save()

    def compute_installed_version(self):
        """
        Calculate the current version of CCenter based on the applied migrations
        :return: CCenter current version.
        """
        if(not self.migration_manager_exists):
            return 0.0

        versions = [float(m.version) for m in MigrationManager.objects.all() if
                               (m.app_name, m.ga_migration) in self.recorder.applied_migrations()]

        if versions:
            return max(versions)
        else:
            return 0.0

    def print_info(self):
        """
        Print the CCenter migration process data.
        """
        self.stdout.write('\n')
        self.stdout.write("-" * 5,ending='')
        self.stdout.write("Information", ending='')
        self.stdout.write("-" * 5)

        self.stdout.write("Installed version: %s." % self.migration_manager.version)
        self.stdout.write("New version: %s." % settings.VERSION)
        self.stdout.write("PR installed: %s." % self.migration_manager.pr_installed)
        self.stdout.write("Stage: %s." % self.migration_manager.get_installation_stage_display())

        self.stdout.write("-" * 21)
        self.stdout.write('\n')

    def is_upgrade(self):
        """
        Check if the installation is CCenter upgrade.
        :return:
        """
        return float(settings.VERSION) > self.migration_manager.version

    def update_installation_stage(self, installation_stage):
        """
        update CCenter installation stage
        :param installation_stage: CCenter new installation stage.
        """
        self.migration_manager.installation_stage = installation_stage
        self.migration_manager.save()

    def move_new_migrations(self):
        """
        Move the new migrations to the not applied folder.
        """

        version = self.migration_manager.version

        self.restore_migrations(version)

        self.find_conflict_migrations_to_go()


        self.stdout.write("Searching for the migrations of the new version.")

        # Get unapplied migrations.
        unapplied_migrations = set(self.loader.disk_migrations.keys()) - self.loader.applied_migrations
        last_version_migrations = MigrationManager.objects.filter(version=version).values_list('app_name',
                                                                                               'ga_migration')

        # Remove from the current version unapplied migrations.
        for migration_data in last_version_migrations:
            required_migrations = self.loader.graph.forwards_plan(migration_data)
            unapplied_migrations = unapplied_migrations - set(required_migrations)

        self.stdout.write("%s migrations of the new version found." % len(unapplied_migrations))

        # Backup the migrations to shared folder because it's CU installation.
        if self.is_cu():
            self.stdout.write("CU version detected, copying migrations to shared folder.")

            self.stdout.write('\n')
            self.stdout.write("Backup CU migrations.")
            self.stdout.write("-" * 30)
            self.stdout.write('\n')

            for app, migration in unapplied_migrations:
                if app in SYS_APP:
                    continue
                self.organizer.copy_migration_to('Shared folder', app, migration)

        ccenter_apps = self.loader.migrated_apps - SYS_APP
        pr_apps = {ccenter_app: 0 for ccenter_app in ccenter_apps}

        self.stdout.write('\n')
        self.stdout.write("Moving new version migrations.")
        self.stdout.write("-" * 30)
        self.stdout.write('\n')

        self.stdout.write("Moving migrations to notapplied folder.")
        for app, migration in unapplied_migrations:
            if app in SYS_APP:
                continue
            self.organizer.move_migration_to('Application notapplied folder', app, migration)

            pr_apps[app] += 1

        self.stdout.write('\n')
        self.stdout.write("-" * 30)
        for app in pr_apps:
            self.stdout.write("%s: %s migrations moved to notapplied folder." % (app, pr_apps[app]))
        self.stdout.write("-" * 30)
        self.stdout.write('\n')

    def restore_migrations(self, version):
        """
        Search and restore missing migrations.
        :param version: ccenter version.
        """

        self.stdout.write('\n')
        self.stdout.write("Restoring missing migrations.")
        self.stdout.write("-" * 30)
        self.stdout.write('\n')


        def is_missing(app, migration):
            if app in SYS_APP:
                return False

            migration_path = self.organizer.app_migration_path % (app, migration)

            return not os.path.exists(migration_path)

        # Restore migrations based on the applied migrations
        missing_migrations = set(
            [(app, migration) for app, migration in self.recorder.applied_migrations() if is_missing(app, migration)])
        if missing_migrations:
            self.stdout.write("%s missing migrations found, starting Restore." % len(missing_migrations))
            for app, migration in missing_migrations:
                try:
                    self.organizer.restore_migration(app, migration)
                except:
                    # Because it's only the CCenter alignment, CCenter alignment migrations could be recorded,
                    # So the migrations that it can't find will be ignored.
                    # We can do this because it also check when restoring using the migrations graph restore.
                    self.stdout.write("migration %s of %s application not found, skipping." % (migration, app))

            self.stdout.write("Restore finished.")

        # Restore migrations based on the migration graph.
        self.build_migration_tree()

        last_version_migrations = MigrationManager.objects.filter(version=version).values_list('app_name',
                                                                                               'ga_migration')

        # Restore the last migrations for the current version.
        for app, migration in last_version_migrations:
            if app in SYS_APP:
                continue
            migration_path = os.path.join(settings.PROJECT_DIR, app, "migrations", "%s.py" % migration)
            if os.path.exists(migration_path):
                continue
            self.organizer.restore_migration(app, migration)

        # Restore the required migrations for the version.
        self.build_migration_tree()

        self.stdout.write("Restore Done.")

    def build_migration_tree(self):
        """
        Restoring the required migrations for the migrations graph
        :return:
        """
        # try to build the migrations graph, when failed, search and restore the missing migrations,
        # Repeat until the graph is build successfully.
        while True:

            try:

                self.loader.build_graph()
                break

            # Missing migrations detected.
            except:
                graph = self.loader.graph

                def is_missing(dependency):
                    if dependency[0] in SYS_APP:
                        return False

                    if dependency in graph.nodes:
                        return False

                    return True

                # Find the missing migrations.
                missing_migrations = set(
                    dependency for migration_node in graph.nodes.values() for dependency in migration_node.dependencies
                    if is_missing(dependency))

                # Restore the missing migrations.
                self.stdout.write("%s missing migrations found, starting Restore." % len(missing_migrations))
                for app, migration in missing_migrations:
                    self.organizer.restore_migration(app, migration)
                self.stdout.write("Restore finished.")

    def is_cu(self):
        """
        Check if the new version is CU.
        :return: if the new version is CU.
        """

        new_version = float(settings.VERSION) * 10

        return int(new_version) != new_version

    def install_pr(self):
        """
        Install PR migrations.
        """

        self.restore_migrations(self.migration_manager.version)

        self.stdout.write('\n')
        self.stdout.write("Install PR")
        self.stdout.write("-" * 30)
        self.stdout.write('\n')

        pr_migrations = set(self.loader.disk_migrations.keys()) - self.loader.applied_migrations
        if not pr_migrations:
            self.stdout.write("-" * 30)
            self.stdout.write("PR migrations not found.")
            self.stdout.write("-" * 30)
            return

        # Record PR
        self.migration_manager.pr_installed = True
        self.migration_manager.save()

        ccenter_apps = self.loader.migrated_apps - SYS_APP
        pr_apps = {ccenter_app: 0 for ccenter_app in ccenter_apps}

        self.stdout.write("%s PR migrations found, copying to shared folder." % len(pr_migrations))

        for app, migration in pr_migrations:
            self.organizer.copy_migration_to('Shared folder', app, migration)
            pr_apps[app] += 1

        for app in pr_apps:
            self.stdout.write("%s: %s PR migrations copied to shared folder." % (app, pr_apps[app]))

        self.stdout.write("install PR migrations.")

        self.get_migration_process().migrate()

        self.stdout.write('\n')
        self.stdout.write("Verify PR installation")
        self.stdout.write("-" * 30)
        self.stdout.write('\n')
        call_command("CheckAllMigrationsApplied")

    def remove_pr(self):
        """
        Remove the pr migrations from CCenter.
        """

        self.stdout.write("Restoring required migrations.")

        self.restore_migrations(self.migration_manager.version)

        self.stdout.write("Required migrations restored.")

        ccenter_apps = self.loader.migrated_apps - SYS_APP

        self.stdout.write("Removing %s PR migrations." % self.migration_manager.version)

        # Remove PR.
        targets = MigrationManager.objects.filter(version=self.migration_manager.version).values_list('app_name',
                                                                                                      'ga_migration')
        self.get_migration_process().migrate(targets)

        self.loader.build_graph()

        # Moving PR migrations to patch_backward folder.
        unapplied_migrations = set(self.loader.disk_migrations.keys()) - self.loader.applied_migrations
        pr_apps = {app: 0 for app in ccenter_apps}

        self.stdout.write("Moving PR migrations to patch_backword folder.")
        for app, migration in unapplied_migrations:
            self.organizer.move_migration_to("Application patch_backward folder", app, migration)
            pr_apps[app] += 1

        for app in pr_apps:
            self.stdout.write("%s: %s migrations moved to patch_backward folder." % (app, pr_apps[app]))

        self.migration_manager.pr_installed = False
        self.migration_manager.save()

    def new_version_upgrade(self):
        """
        Check if the version is not CU of the current version.
        :return: if upgrading to GA or CU of newer version.
        """
        new_version = float(settings.VERSION) * 10
        current_version = self.migration_manager.version * 10
        return int(new_version) != int(current_version)

    def remove_cu(self):
        """
        Remove CU migrations.
        """

        self.restore_migrations(self.migration_manager.version)


        ccenter_apps = self.loader.migrated_apps - SYS_APP
        ga_version = float(int(self.migration_manager.version * 10)) / 10

        self.stdout.write('\n')
        self.stdout.write("Revert CCenter to %s" % ga_version)
        self.stdout.write("-" * 30)
        self.stdout.write('\n')

        self.stdout.write("Removing CU migrations.")
        migrated_ccenter_apps = set(
            [app for app in ccenter_apps for migrated_app, migration in self.loader.applied_migrations if
             app == migrated_app])

        targets = set()
        for app in migrated_ccenter_apps:

            destination = MigrationManager.objects.filter(app_name=app, version=ga_version).values_list('app_name',
                                                                                                        'ga_migration')
            if not destination:
                destination = self.loader.graph.root_nodes(app)
                if not destination:
                    raise CommandError("Can't migrate application '%s'." % app)
            targets = targets.union(destination)
        self.get_migration_process().migrate(targets)

        # Moving CU migrations to patch_backward folder.
        unapplied_migrations = set(self.loader.disk_migrations.keys()) - self.loader.applied_migrations
        pr_apps = {app: 0 for app in ccenter_apps}

        self.stdout.write("Moving CU migrations to patch_backword folder.")
        for app, migration in unapplied_migrations:
            self.organizer.move_migration_to("Application patch_backward folder", app, migration)
            pr_apps[app] += 1

        self.stdout.write('\n')
        self.stdout.write("-" * 30)
        for app in pr_apps:
            self.stdout.write("%s: %s migrations moved to patch_backward folder." % (app, pr_apps[app]))
        self.stdout.write("-" * 30)
        self.stdout.write('\n')

        self.migration_manager.pr_installed = False
        self.migration_manager.version = ga_version
        self.migration_manager.save()

    def migrate_ccenter(self):
        """
        Migrate CCenter to new version.
        """

        self.restore_migrations(self.migration_manager.version)

        self.stdout.write("Upgrade CCenter to '%s'." % settings.VERSION)
        self.get_migration_process().migrate()

    def prepare_upgrade(self):
        """
        Prepare CCenter for upgrade by moving the unapplied migrations to patch_backward folder and restoring
        the new version migrations from the notapplied folder
        :return:
        """
        self.stdout.write("Restoring required migrations.")

        self.restore_migrations(self.migration_manager.version)

        self.stdout.write("Required migrations restored.")
        unapplied_migrations = set(self.loader.disk_migrations.keys()) - self.loader.applied_migrations

        # Moving remaining migrations
        if unapplied_migrations:
            self.stdout.write("Moving not applied migrations to patch_backword folder.")

            for app, migration in unapplied_migrations:
                self.organizer.move_migration_to('Application patch_backward folder', app, migration)

        ccenter_apps = self.loader.migrated_apps - SYS_APP

        # Restore migrations form not applied.
        for app in ccenter_apps:

            not_applied_app_folder = os.path.join(PROJECT_DIR, app, "migrations", "notapplied")
            if not os.path.exists(not_applied_app_folder):
                continue

            for migration in os.listdir(not_applied_app_folder):
                not_applied_migration_path = os.path.join(not_applied_app_folder, migration)
                migration_path = os.path.join(settings.PROJECT_DIR, app, "migrations", migration)
                shutil.copy(not_applied_migration_path, migration_path)

        self.stdout.write("Restoring required migrations for new version.")

        self.restore_migrations(float(settings.VERSION))

        self.stdout.write("Required migrations restored.")

        for app in ccenter_apps:

            not_applied_app_folder = os.path.join(PROJECT_DIR, app, "migrations", "notapplied")
            if os.path.exists(not_applied_app_folder):
                continue

            os.rmdir(not_applied_app_folder)

    def find_conflict_migrations_to_go(self):
        """
        verifying that when upgrading CCenter to new version, there will be no conflicts.
        """

        self.restore_migrations(self.migration_manager.version)

        self.stdout.write('\n')
        self.stdout.write("Searching for conflicting in migrations")
        self.stdout.write("-" * 30)
        self.stdout.write('\n')

        self.stdout.write("Check conflicted migrations.")

        ccenter_apps = self.loader.migrated_apps - SYS_APP

        conflicted_apps = {}
        for app in ccenter_apps:
            migrations = set(self.loader.graph.leaf_nodes(app))
            conflicted_migrations = migrations - set(self.loader.applied_migrations)

            if len(conflicted_migrations) > 1:
                conflicted_apps[app] = migrations

        if conflicted_apps:
            self.stdout.write("The following apps have conflicting migrations, please remove the fix the conflicts.")

            for app in conflicted_apps:
                self.stdout.write("=====%s=====" % app)
                for migration in conflicted_apps[app]:
                    self.stdout.write(migration)

            raise CommandError("Conflicted migrations detected.")

    @transaction.atomic
    def populate_sql(self):
        self.stdout.write("Creating/updating SQL views and procedures...")

        # Get an instance of a logger
        logger = logging.getLogger('django')
        engine = settings.DATABASES['default']['ENGINE']

        files_dir = os.path.normpath(os.path.join(settings.PROJECT_DIR, 'dbmconfigapp', 'sql', engine))

        # CREATE ALL VIEWS AND PROCEDURES

        sql_files = [f for f in os.listdir(files_dir) if os.path.isfile(os.path.join(files_dir, f))]
        cursor = connection.cursor()

        for sql_file in sql_files:
            try:
                path = os.path.normpath(os.path.join(files_dir, sql_file))
                logger.debug(path)
                if os.path.exists(path):
                    logger.debug("Loading initial SQL data from '%s'" % path)
                    f = open(path)
                    sql = f.read()
                    f.close()
                    cursor.execute(sql)
            except Exception as e:
                self.stderr.write("Failed to install custom SQL file '%s': %s\n" % \
                                  (path, e))
                raise CommandError("Failed to create/update SQL views and procedures.")

        self.stdout.write('  Finished creating/updating SQL views and procedures.')

    def perform_after_installation_tasks(self):
        """
        Update CCenter version and validate installation.
        """

        self.migration_manager.version = float(settings.VERSION)
        self.migration_manager.save()

        self.loader.build_graph()
        ccenter_apps = self.loader.migrated_apps - SYS_APP
        for app in ccenter_apps:
            leaf = self.loader.graph.leaf_nodes(app)[0]
            MigrationManager.objects.get_or_create(app_name=leaf[0], version=settings.VERSION, defaults={'ga_migration': leaf[1]})

        self.stdout.write('\n')
        self.stdout.write("Verify CCenter installed")
        self.stdout.write("-" * 30)
        self.stdout.write('\n')
        call_command("CheckAllMigrationsApplied")
        call_command("CheckMigrationVersionsRecorded")


    def get_migration_process(self):
        return MigrationProcess(self.stdout, self.stderr, self.connection)

    def print_title(self, title):
        self.stdout.write('\n')
        self.stdout.write("=" * 40)
        self.stdout.write(title)
        self.stdout.write("=" * 40)
        self.stdout.write('\n')

    def update_version_manager(self, ver=settings.VERSION):

        print("Updating VersionManager table to %s" % ver)
        records = VersionManager.objects.all()
        if(records.exists()):
            rec = records[0]
            rec.version = ver;
        else:
            rec = VersionManager(version = ver);

        rec.save();


    def handle(self, *args, **options):
        self.print_title("Pre install tasks")
        self.connection = connection
        self.recorder = MigrationRecorder(self.connection)
        self.loader = MigrationLoader(self.connection, load=False)
        self.organizer = MigrationsOrganizer(self.stdout, self.stderr)
        self.update_database_compatibility_level()
        self.migration_manager_exists = self.migration_manager_table_exists()
        self.get_migration_manager()
        self.print_info()

        # Added from migrate command,
        # It's something related to pre and post migrate signals.
        for app_config in apps.get_app_configs():
            if module_has_submodule(app_config.module, "management"):
                import_module('.management', app_config.name)

        # Prevent CCenter upgrade to new version if the previous upgrade did not complete.
        if self.migration_manager.version_new != float(settings.VERSION):
            self.stdout.write("Error: multiple CCenter upgrades detected (%s,%s)." % self.migration_manager.version_new,
                              settings.VERSION)
            self.stdout.write("Upgrading CCenter to new version in the middle of installation is forbidden.")
            raise CommandError("multiple CCenter upgrades detected")

        # Start installation stage.
        if self.migration_manager.installation_stage == INSTALLATION_START:

            self.print_title(self.migration_manager.get_installation_stage_display())

            # Send pre migrate signal.
            emit_pre_migrate_signal([], 1, False, self.connection.alias)

            # Migrate django apps.
            #self.get_migration_process().migrate_django_apps()

            self.stdout.write('\n')
            self.stdout.write("Check CCenter installation type")
            self.stdout.write("-" * 30)

            # Check what type of installation needed.
            self.stdout.write("Check installation type... ", ending='')

            # PR install
            if not self.is_upgrade():
                self.stdout.write("CCenter PR installation.")

                self.update_installation_stage(INSTALL_PR)

            # Fresh install
            elif not self.recorder.applied_migrations():
                self.stdout.write("CCenter Fresh install.")

                self.update_installation_stage(INIT_FROM_ZERO)

            # Upgrade
            else:
                self.stdout.write("CCenter upgrade.")

                # Only transfer the new migrations to notapplied folder at before dealing with the ccenter migration process in upgrade.
                # this will ensure that only the migrations of the new version (the one that not applied) will be at notapplied folder.
                self.move_new_migrations()

                self.update_installation_stage(VERIFY_PR)

        else:
            self.print_title("Resume installation")

        # PR install stage.
        if self.migration_manager.installation_stage == INSTALL_PR:
            self.print_title(self.migration_manager.get_installation_stage_display())

            # Install PR.
            self.install_pr()

            self.update_installation_stage(POST_INSTALL)

        # CCenter first installation stage.
        if self.migration_manager.installation_stage == INIT_FROM_ZERO:
            self.print_title(self.migration_manager.get_installation_stage_display())

            # Doing preparation to upgrade CCenter from sparrow (or fresh installation).
            self.get_migration_process().init_from_zero()

            # Update CCenter installed version.
            self.migration_manager.pr_installed = False
            self.migration_manager.version = self.compute_installed_version()
            self.migration_manager.save()

            self.update_installation_stage(POST_INSTALL)

        # Verify installed PR migrations stage.
        if self.migration_manager.installation_stage == VERIFY_PR:
            self.print_title(self.migration_manager.get_installation_stage_display())

            # Check if PR installed.
            self.stdout.write("Checking CCenter PR... ", ending='')

            if self.migration_manager.pr_installed:
                self.stdout.write("PR migrations detected.")

                self.update_installation_stage(REMOVE_PR)
            else:
                self.stdout.write("No PR migrations detected.")

                self.update_installation_stage(VERIFY_CU)

        # Remove PR stage.
        if self.migration_manager.installation_stage == REMOVE_PR:
            self.print_title(self.migration_manager.get_installation_stage_display())

            # Remove CCenter PRs
            self.remove_pr()

            self.update_installation_stage(VERIFY_CU)

        # Verify CU installed stage.
        if self.migration_manager.installation_stage == VERIFY_CU:
            self.print_title(self.migration_manager.get_installation_stage_display())

            self.stdout.write("Checking the upgrade type... ", ending='')
            if self.new_version_upgrade():
                self.stdout.write("Upgrade to new GA.")

                self.update_installation_stage(REMOVE_CU)
            else:
                self.stdout.write("Upgrade to new CU.")

                self.update_installation_stage(PREPARE_UPGRADE)

        # Remove CU stage
        if self.migration_manager.installation_stage == REMOVE_CU:
            self.print_title(self.migration_manager.get_installation_stage_display())

            self.remove_cu()

            self.update_installation_stage(PREPARE_UPGRADE)

        # Prepare CCenter upgrade state
        if self.migration_manager.installation_stage == PREPARE_UPGRADE:
            self.print_title(self.migration_manager.get_installation_stage_display())

            self.prepare_upgrade()

            self.update_installation_stage(RUN_MIGRATE)

        # Upgrade CCenter stage
        if self.migration_manager.installation_stage == RUN_MIGRATE:
            self.print_title(self.migration_manager.get_installation_stage_display())

            self.migrate_ccenter()

            self.update_installation_stage(POST_INSTALL)

        if self.migration_manager.installation_stage == POST_INSTALL:
            self.print_title(self.migration_manager.get_installation_stage_display())

            self.populate_sql()
            self.migration_manager.version_new = 0.0

            self.migration_manager.save()
            emit_post_migrate_signal([], 1, False, self.connection.alias)

            self.update_version_manager()

            self.perform_after_installation_tasks()

            self.update_installation_stage(INSTALLATION_START)
