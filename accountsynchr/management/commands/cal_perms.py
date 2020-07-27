from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from uw_trumba.calendars import Calendars
from accountsynchr.util.settings import get_cronjob_sender


class Command(BaseCommand):
    """
    List the permissions of each calendars on the given campus.
    """

    def add_arguments(self, parser):
        parser.add_argument('campus_code',
                            choices=['sea', 'bot', 'tac'])

    def handle(self, *args, **options):
        campus_code = options['campus_code']
        msgs = []
        cal_list = Calendars().campus_calendars[campus_code].values()
        if cal_list is not None:
            for cal in cal_list:
                msgs.append(cal.name)
                for perm in sorted(cal.permissions.values()):
                    msgs.append("    {0} {1}".format(perm.uwnetid, perm.level))

            message = "\n".join(msgs)
            sender = "{}@uw.edu".format(get_cronjob_sender())
            send_mail("Permissions of {} Calendars".format(campus_code),
                      message, sender, [sender])
            print(message)
