import logging
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.trumba_gws import TrumbaToGws


class Command(BaseCommand):
    """
    Sync Trumba calendars and editors to UW groups and members.
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        synchr = TrumbaToGws()
        synchr.sync()
        if synchr.has_err():
            print(synchr.get_error_report())
