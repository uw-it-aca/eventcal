import logging
from django.core.management.base import BaseCommand, CommandError
from uw_trumba.models import TrumbaCalendar
from uw_trumba.account import delete_editor
from accountsynchr.dao.trumba import (
    CalPermManager, get_permission, remove_permission)


class Command(BaseCommand):
    """
    Close an account on Trumba.
    """

    def add_arguments(self, parser):
        parser.add_argument('uwnetid')

    def handle(self, *args, **options):
        userid = options['uwnetid']

        cal_m = CalPermManager()
        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            if cal_m.exists(campus_code):
                for cal in cal_m.get_campus_calendars(campus_code):
                    if get_permission(cal, userid) is None:
                        continue
                    if not remove_permission(cal, userid):
                        print("Failed to remove permission from {0}".format(
                                cal.name))

        print("Delete account({0}) ==> {1}".format(
            userid, delete_editor(userid)))
