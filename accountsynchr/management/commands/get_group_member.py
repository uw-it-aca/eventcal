from django.core.management.base import BaseCommand, CommandError
from accountsynchr.ucalgroup.member_manager import MemberManager


class Command(BaseCommand):
    help = "print editor netids of the calendar group."

    def add_arguments(self, parser):
        parser.add_argument('group-name')

    def handle(self, *args, **options):
        group_name = options['group-name']
        mem_m = MemberManager()
        result = mem_m.get_members_by_groupid(group_name)
        if result is None:
            print "%s not exists" % group_name
            return
        print "The members of %s:" % group_name
        count = 0
        for group_member in result:
            if group_member.member_type == 'uwnetid':
                print "%s@uw.edu" % group_member.name
                count = count + 1
        print "Total member uwnetids: %d" % count
