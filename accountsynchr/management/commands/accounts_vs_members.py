from django.core.management.base import BaseCommand, CommandError
from accountsynchr.dao.trumba import CalPermManager
from accountsynchr.ucalgroup.group_manager import GroupManager


class Command(BaseCommand):
    """
    Compare the Trumba accounts vs. UW group members.
    """

    def handle(self, *args, **options):

        cal_m = CalPermManager()
        account_set = cal_m.perm_loader.account_set
        print("Total users in Trumba: {0:d}".format(len(account_set)))

        grp_m = GroupManager()
        member_set = grp_m.gws.all_editor_uwnetids
        print("Total members in UW Group: {0:d}".format(len(member_set)))

        print("Trumba Accounts who are not members of any group:")
        for userid in account_set:
            if userid not in member_set:
                print("  {0}".format(userid))

        print("Group members without a Trumba account:")
        for userid in member_set:
            if userid not in account_set:
                print("  {0}".format(userid))
