from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.dao.trumba import CalPermManager
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.util.settings import get_cronjob_sender


class Command(BaseCommand):
    """
    Compare the Trumba accounts vs. UW group members.
    """

    def handle(self, *args, **options):
        msgs = []
        cal_m = CalPermManager()
        account_set = cal_m.perm_loader.account_set
        msgs.append("Total users in Trumba: {0:d}".format(len(account_set)))

        grp_m = GroupManager()
        member_set = grp_m.gws.all_editor_uwnetids
        msgs.append("Total members in UW Group: {0:d}".format(len(member_set)))

        users = []
        for userid in account_set:
            if userid not in member_set:
                users.append(userid)
        msgs.append(
            "Trumba accounts with no membership: {}".format(
                " ".join(users)))

        users = []
        for userid in member_set:
            if userid not in account_set:
                users.append(userid)
        msgs.append("Editor group members with no Trumba account: {}".format(
                " ".join(users)))

        message = "\n".join(msgs)
        sender = "{}@uw.edu".format(get_cronjob_sender())
        send_mail("Trumba accounts vs. UW group members",
                  message, sender, [sender])
        print(message)
