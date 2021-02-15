from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from uw_trumba.models import TrumbaCalendar
from accountsynchr.dao.gws import Gws
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.util.settings import get_cronjob_sender


class Command(BaseCommand):
    """
    Find all the groups which has external group(s) as member
    """

    def handle(self, *args, **options):
        ret_list = []

        gro_m = GroupManager()
        for campus_code in (TrumbaCalendar.SEA_CAMPUS_CODE,
                            TrumbaCalendar.BOT_CAMPUS_CODE,
                            TrumbaCalendar.TAC_CAMPUS_CODE):
            for group in gro_m.get_campus_editor_groups(campus_code):
                for gm in gro_m.gws.get_members(group.name):
                    if (not gm.is_uwnetid() and
                            gm.name is not None and
                            not gm.name.startswith("u_eventcal"):
                        ret_list.append(group.name)

        sender = get_cronjob_sender()
        message = "\n".join(ret_list)
        send_mail("The Editor Groups containing external groups:",
                  message, sender, [sender])
        print(message)
