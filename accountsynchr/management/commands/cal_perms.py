from django.core.management.base import BaseCommand, CommandError
from uw_trumba.calendars import Calendars


class Command(BaseCommand):
    """
    List the permissions of each calendars on the given campus.
    """

    def add_arguments(self, parser):
        parser.add_argument('campus_code',
                            choices=['sea', 'bot', 'tac'])

    def handle(self, *args, **options):
        campus_code = options['campus_code']

        cal_list = Calendars().campus_calendars[campus_code].values()
        if cal_list is not None:
            for cal in cal_list:
                print("{0}".format(cal.name))

                for perm in sorted(cal.permissions.values()):
                    print("    {0} {1}".format(perm.uwnetid, perm.level))
