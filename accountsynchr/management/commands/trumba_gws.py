import logging
from time import strftime
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.trumba_gws import TrumbaToGws


class Command(BaseCommand):
    help = "Sync Trumba calendars and editors to UW groups and members."

    def add_arguments(self, parser):
        parser.add_argument('campus_code', nargs='?', default=None,
                            choices=['sea', 'bot', 'tac'])

    def handle(self, *args, **options):
        synchr = TrumbaToGws()
        synchr.sync(campus_code=options['campus_code'])
