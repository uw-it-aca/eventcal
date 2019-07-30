import logging
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.trumba_gws import TrumbaToGws


logger = logging.getLogger("eventcal.commands")


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
            logger.error(synchr.get_error_report())
