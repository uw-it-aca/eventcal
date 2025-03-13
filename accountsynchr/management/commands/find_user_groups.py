# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from uw_trumba.models import TrumbaCalendar
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.util.settings import get_cronjob_sender


class Command(BaseCommand):
    """
    Find all the groups the given uwnetid is in
    """

    def add_arguments(self, parser):
        parser.add_argument('uwnetid')

    def handle(self, *args, **options):
        userid = options['uwnetid']
        msgs = []
        gro_m = GroupManager()
        for campus_code in (TrumbaCalendar.SEA_CAMPUS_CODE,
                            TrumbaCalendar.BOT_CAMPUS_CODE,
                            TrumbaCalendar.TAC_CAMPUS_CODE):
            for group in gro_m.get_campus_editor_groups(campus_code):
                for member in group.members:
                    if member.name == userid:
                        msgs.append(group.group_ref.name)

            for group in gro_m.get_campus_showon_groups(campus_code):
                for member in group.members:
                    if member.name == userid:
                        msgs.append(group.group_ref.name)

        sender = get_cronjob_sender()
        message = "\n".join(msgs)
        send_mail("The Groups of the User {}".format(userid),
                  message, sender, [sender])
        print(message)
