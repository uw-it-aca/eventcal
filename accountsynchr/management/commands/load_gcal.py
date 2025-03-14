# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import logging
from django.core.management.base import BaseCommand
from uw_trumba.calendars import Calendars
from uw_trumba.models import TrumbaCalendar
from accountsynchr.models.gcalendar import GCalendar

trumba_cals = Calendars()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Initial load of gcalendar table
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        GCalendar.objects.all().delete()
        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            cals = trumba_cals.get_campus_calendars(campus_code)
            logger.info("Total {} {} calendars".format(
                len(cals), campus_code))
            if cals:
                loaded_count = 0
                for trumba_calendar in cals:
                    try:
                        obj = GCalendar.create(trumba_calendar)
                        loaded_count += 1
                    except Exception as ex:
                        logger.error("Failed to add {}\n".format(
                            {'calendarid': trumba_calendar.calendarid,
                             'campus': trumba_calendar.campus,
                             'name': trumba_calendar.name,
                             'err': ex}))
                logger.info("Loaded {} entries".format(loaded_count))
