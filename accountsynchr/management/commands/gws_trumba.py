import logging
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.gws_trumba import GwsToTrumba


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Sync UW group members to Trumba user and permissions.
    """
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        synchr = GwsToTrumba()
        synchr.sync()
        if synchr.has_err():
            logger.error(synchr.get_error_report())
