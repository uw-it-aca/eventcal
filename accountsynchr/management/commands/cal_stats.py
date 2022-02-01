# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from uw_trumba.models import TrumbaCalendar
from accountsynchr.dao.trumba import CalPermManager
from accountsynchr.util.settings import get_cronjob_sender


class Command(BaseCommand):
    """
    Output the total number of the calendars by campus
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        msgs = []
        cal_m = CalPermManager()
        msgs.append("Total Bothell calendars: {0:d}".format(
            cal_m.total_calendars('bot')))
        msgs.append("Total Seattle calendars: {0:d}".format(
            cal_m.total_calendars('sea')))
        msgs.append("Total Tacoma calendars: {0:d}".format(
            cal_m.total_calendars('tac')))
        msgs.append("Total editor accounts: {0:d}".format(
            cal_m.total_accounts()))

        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            campus_name = choice[1]
            msgs.append("{}:".format(campus_name))
            if cal_m.exists(campus_code):
                calendars = cal_m.get_campus_calendars(campus_code)
                for cal in calendars:
                    msgs.append("  {0}: {1:d} permissions".format(
                            cal.name, len(cal.permissions)))

        message = "\n".join(msgs)
        sender = get_cronjob_sender()
        send_mail("Calendars Stats", message, sender, [sender])
        print(message)
