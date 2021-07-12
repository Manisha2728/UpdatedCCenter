import os.path

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.migrations.loader import MigrationLoader

from configcenter import settings
from dbmconfigapp.models import MigrationManager


class Command(BaseCommand):
    help = "validate all versions migrations."

    def handle(self, *args, **options):
        """
        Checking that the migrations versions recorded in CCenter migration manager are applied.
        """

        print('-' * 20)

        print ("Starting validation for the CCenter applications.")

        print('-' * 20)

        # Get the version of CCenter and the GA version.
        self.version = float(settings.VERSION)
        GA_version = float(int(self.version * 10)) / 10  # Retrieving the GA version.
        print ("Installed Version: %s" % self.version)
        print ("GA Version: %s" % GA_version)

        print('-' * 20)

        # Connecting to the DB.
        connection = connections['default']
        self.loader = MigrationLoader(connection)

        # Retrieving CCenter applications.
        print ("Retrieving CCenter applications.")
        sys_apps = set(['admin', 'sessions', 'auth', 'sites', 'contenttypes'])
        dbm_apps = self.loader.migrated_apps - sys_apps
        print ("CCenter Applications:")

        for dbm_app in dbm_apps:
            print ("\t%s" % dbm_app)

        print ("CCenter applications retrieved.")

        print('-' * 20)

        print ("Retrieving records of the applications installed versions.")
        apps = {}
        print ("Retrieving installed applications versions.")
        for mig in MigrationManager.objects.filter(version__startswith=GA_version, app_name__in=dbm_apps):
            print ("Found - application: %s, version: %s" % (mig.app_name, mig.version))
            apps[(mig.app_name, mig.version)] = mig.ga_migration

        if len(apps.keys()) == 0:
            print ("Could not retrieve CCenter applications installed versions.")
            print ("Validation failed.")
            raise Exception("Could not retrieve CCenter applications installed versions.")

        print ("Records of the applications versions retrieved.")

        print('-' * 20)

        print ("Verifying that the installed versions of CCenter applications recorded.")
        all_applications_version_exists = True
        for app in sorted(apps.keys(), key=AppSort):
            application_version_applied = (app[0], apps[app]) in self.loader.applied_migrations

            application_version_migration_path = os.path.join(settings.PROJECT_DIR, app[0], "migrations",
                                                              "{migration}.py".format(migration=apps[app]) if apps[
                                                                  app] else "")
            application_version_migration_exists = os.path.exists(application_version_migration_path)

            if (not application_version_applied):
                all_applications_version_exists = False

            if (not application_version_migration_exists):
                all_applications_version_exists = False

            print ("Application: %s \t|\t Version: %s \t|\t Migration: %s \t|\t Applied: %s \t|\t Exists:%s" % (
            app[0], app[1], apps[app], "Yes" if application_version_applied else "No",
            "Yes" if application_version_migration_exists else "No"))

        if not all_applications_version_exists:
            print ("Error: migrations of CCenter installed versions are not applied on exists.")
            print ("Validation failed.")
            raise Exception("Error: migrations of CCenter installed versions are not applied on exists.")

        print ("All CCenter applications installed versions recorded and exist.")

        print('-' * 20)

        print ("Verifying that all the current version of ccenter applications installed.")
        for dbm_app in dbm_apps:
            app_version_tuple = (dbm_app, str(self.version))
            app_version_migration = apps[app_version_tuple]
            if not apps.has_key(app_version_tuple):
                print ("Application: %s \t|\t Version: %s \t|\t Migration: %s \t|\t Applied: %s \t|\t Exists:%s" % (
                    dbm_app, self.version, "Unknown", "No", "No"))
                all_applications_version_exists = False
                continue
            application_version_applied = (dbm_app, app_version_migration) in self.loader.applied_migrations
            application_version_migration_path = os.path.join(settings.PROJECT_DIR, dbm_app, "migrations",
                                                              "{migration}.py".format(
                                                                  migration=app_version_migration) if app_version_migration else "")
            application_version_migration_exists = os.path.exists(application_version_migration_path)

            if (not application_version_applied):
                all_applications_version_exists = False

            if (not application_version_migration_exists):
                all_applications_version_exists = False

            print ("Application: %s \t|\t Version: %s \t|\t Migration: %s \t|\t Applied: %s \t|\t Exists:%s" % (
                dbm_app, self.version, app_version_migration, "Yes" if application_version_applied else "No",
                "Yes" if application_version_migration_exists else "No"))

        if not all_applications_version_exists:
            print ("Not all CCenter applications of the current version installed.")
            print ("Validation failed.")
            raise Exception("Not all CCenter applications of the current version installed.")

        print ("All CCenter applications of the current version installed.")

        print('-' * 20)

        print ("Validation pass.")

        print('-' * 20)


def AppSort(app):
    return app[1]
