import logging
from django.core.management.base import BaseCommand, CommandError
from uw_trumba.models import TrumbaCalendar
from accountsynchr.dao.trumba import CalPermManager


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Output the total number of the calendars by campus
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        cal_m = CalPermManager()
        logger.info("Total Bothell calendars: {0:d}".format(
            cal_m.total_calendars('bot')))
        logger.info("Total Seattle calendars: {0:d}".format(
            cal_m.total_calendars('sea')))
        logger.info("Total Tacoma calendars: {0:d}".format(
            cal_m.total_calendars('tac')))
        logger.info("Total editor accounts: {0:d}".format(
            cal_m.total_accounts()))

        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            logger.info("\n{0} campus".format(choice[1]))
            if cal_m.exists(campus_code):
                calendars = cal_m.get_campus_calendars(campus_code)
                for cal in calendars:
                    logger.info("{0}: {1:d} permissions".format(
                            cal.name, len(cal.permissions)))
