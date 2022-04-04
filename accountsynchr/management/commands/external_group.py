# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


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
                for gm in gro_m.gws.get_members(group.get_group_id()):
                    if gm.is_group() and not gm.name.startswith("u_eventcal"):
                        if group.get_group_id() not in ret_list:
                            ret_list.append(group.get_group_id())

        sender = get_cronjob_sender()
        message = "\n".join(ret_list)
        send_mail("The Editor Groups containing external groups:",
                  message, sender, [sender])
        print(message)
