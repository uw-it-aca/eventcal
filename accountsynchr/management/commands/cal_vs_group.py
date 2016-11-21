import re
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.trumba.calendar_manager import CalendarManager
from accountsynchr.trumba.permission_manager import PermissionManager


class Command(BaseCommand):
    args = "<campus_code>: sea|bot|tac"
    help = "Compare the event calendars and uw groups on a given campus."

    def add_arguments(self, parser):
        parser.add_argument('campus_code',
                            choices=['sea', 'bot', 'tac'])

    def handle(self, *args, **options):
        campus_code = options['campus_code']
        cal_m = CalendarManager()
        print "Total number of %s calendars: %d" % (campus_code,
                                                    cal_m.len(campus_code))
        gro_m = GroupManager()
        print "Total number of %s groups: %d" % (campus_code,
                                                 gro_m.len(campus_code))

        if gro_m.exists(campus_code):
            result = gro_m.get_all_groups(campus_code)
            if result is not None:
                for uwcalgroup in result:
                    calendarid = int(
                        re.sub(r'^u_eventcal_[a-z]{3}_([1-9]\d*)-[a-z]+$',
                               r'\1',
                               uwcalgroup.name))
                    if not cal_m.has_calendar(campus_code, calendarid):
                        print " %s %s has no calendar" % (
                            uwcalgroup.name, uwcalgroup.title)

        per_m = PermissionManager()
        if cal_m.exists(campus_code):
            results = cal_m.get_all_calendars(campus_code)
            if results is not None:
                for cal in results:
                    if per_m.has_editor(cal) and\
                            not gro_m.has_editor_group(cal):
                        print " %s missing editor group" % cal
                    if per_m.has_showon(cal) and\
                            not gro_m.has_showon_group(cal):
                        print " %s missing showon group" % cal
