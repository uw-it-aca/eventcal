from django.core.management.base import BaseCommand, CommandError
from accountsynchr.trumba.permission_manager import PermissionManager
from accountsynchr.ucalgroup.member_manager import MemberManager


class Command(BaseCommand):
    help = "Compare the Trumba accounts vs. UW event calendar group members."

    def handle(self, *args, **options):

        per_m = PermissionManager()
        account_set = per_m.get_all_accounts()
        print "Total users in Trumba: %d" % len(account_set)

        mem_m = MemberManager()
        member_set = mem_m.get_all_members()
        print "Total members in UW Group: %d" % len(member_set)

        print "Trumba Accounts who are not members of any group:"
        for userid in account_set:
            if userid not in member_set:
                print "  %s" % userid

        print "Group members with no permission with any Trumba calednar:"
        for userid in member_set:
            if userid not in account_set:
                print "  %s" % userid
