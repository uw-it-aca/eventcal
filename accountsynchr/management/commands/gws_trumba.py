import logging
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.gws_trumba import GwsToTrumba


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
            print(synchr.get_error_report())
