# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.util.settings import get_cronjob_sender


class Command(BaseCommand):

    def handle(self, *args, **options):

        gro_m = GroupManager()
        msgs = []
        msgs.append("Total {0:d} editors".format(len(gro_m.get_all_editors())))

        msgs.append(
            "Seattle has total {0:d} editor, {1:d} showon groups".format(
                len(gro_m.get_campus_editor_groups('sea')),
                len(gro_m.get_campus_showon_groups('sea'))))

        msgs.append(
            "Bothell has total {0:d} editor, {1:d} showon groups".format(
                len(gro_m.get_campus_editor_groups('bot')),
                len(gro_m.get_campus_showon_groups('bot'))))

        msgs.append(
            "Tacoma has total {0:d} editor, {1:d} showon groups".format(
                len(gro_m.get_campus_editor_groups('tac')),
                len(gro_m.get_campus_showon_groups('tac'))))

        sender = get_cronjob_sender()
        message = "\n".join(msgs)
        send_mail("The Calendar Groups Stats", message, sender, [sender])
        print(message)
