from django.core.management.base import BaseCommand, CommandError
from accountsynchr.trumba.permission_manager import PermissionManager
from accountsynchr.trumba.calendar_manager import CalendarManager


class Command(BaseCommand):
    help = "List the permissions of each calendars on the given campus."

    def add_arguments(self, parser):
        parser.add_argument('campus_code',
                            choices=['sea', 'bot', 'tac'])

    def handle(self, *args, **options):
        campus_code = options['campus_code']

        cal_list = CalendarManager().get_all_calendars(campus_code)
        pm = PermissionManager()
        if cal_list is not None:
            print "%s;%s;%s;%s;%s" % ("Calendar",
                                      "Total editors",
                                      "Editor uwnetids",
                                      "Total showons",
                                      "Showon uwnetids")
            for cal in cal_list:
                vstr = "%s;" % cal.name

                perm_list = pm.get_editor_permissions(cal)
                if perm_list is None or len(perm_list) == 0:
                    vstr = vstr + " 0; n/a"
                else:
                    vstr = vstr + (" %d;" % len(perm_list))
                    for e in perm_list:
                        vstr = vstr + " " + e.uwnetid

                perm_list = pm.get_showon_permissions(cal)
                if perm_list is None or len(perm_list) == 0:
                    vstr = vstr + "; 0; n/a"
                else:
                    vstr = vstr + ("; %d;" % len(perm_list))
                    for e in perm_list:
                        vstr = vstr + " " + e.uwnetid
                print vstr
