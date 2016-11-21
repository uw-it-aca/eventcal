import logging
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.gws_trumba import GwsToTrumba


class Command(BaseCommand):
    help = "Sync UW group members to Trumba user and permissions."

    def handle(self, *args, **options):
        synchr = GwsToTrumba()
        synchr.sync()
