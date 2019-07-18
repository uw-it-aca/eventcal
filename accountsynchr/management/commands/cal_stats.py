import logging
from django.core.management.base import BaseCommand, CommandError
from uw_trumba.calendars import Calendars


class Command(BaseCommand):
    """
    Output the total number of the calendars by campus
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        cals = Calendars()
        print("Total Bothell calendars: {0:d}".format(
            cals.total_calendars('bot')))
        print("Total Seattle calendars: {0:d}".format(
            cals.total_calendars('sea')))
        print("Total Tacoma calendars: {0:d}".format(
            cals.total_calendars('tac')))
