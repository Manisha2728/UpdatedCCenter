import os

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.migrations.loader import MigrationLoader

from configcenter import settings


class Command(BaseCommand):
    help = "Check all migrations applied."

    def handle(self, *args, **options):

        # Connecting to the DB.
        connection = connections['default']
        loader = MigrationLoader(connection)

        # Getting the names of the applications of CCenter.
        print ("Retrieving CCenter applications.")

        sys_apps = set(['admin', 'sessions', 'auth', 'sites', 'contenttypes'])
        dbm_apps = loader.migrated_apps - sys_apps

        print ("CCenter Applications:")
        for dbm_app in dbm_apps:
            print ("\t%s" % dbm_app)

        # Getting the unapplied migrations from substracting the migrations on the disk from the applied migrations.
        print ("Checking for unapplied migrations.")

        unapplied_migrations = set(loader.disk_migrations.keys()) - loader.applied_migrations

        # Verifying that all the migrations applied.
        if unapplied_migrations:

            print ("Unapplied migrations exists:")
            for unapplied_migration in unapplied_migrations:
                print ("\t- %s: %s" % unapplied_migration)

            raise Exception("Unapplied migrations exists.")

        print("All migrations applied.")

        # Verifying that all the applied migrations has migration file.
        print ("Verifying that the applied migration files exists.")

        migration_not_exists = False

        for migration in loader.applied_migrations:

            # Ignore django apps.
            if migration[0] not in dbm_apps:
                continue

            #Verify that the migration file exists.
            application_version_migration_path = os.path.join(settings.PROJECT_DIR, migration[0], "migrations",
                                                              "{migration}.py".format(
                                                                  migration=migration[1]) if migration else "")

            if not os.path.exists(application_version_migration_path):

                migration_not_exists = True
                print ("migration '%s' of '%s' not exists." % migration)

        if migration_not_exists:
            print ("Not all the applied migrations exists.")
            raise Exception("Not all the applied migrations exists.")

        print ("All the applied migrations exists.")
        print ("Validation pass.")
