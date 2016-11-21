from django.core.management.base import BaseCommand, CommandError
from accountsynchr.ucalgroup.group_manager import GroupManager


class Command(BaseCommand):
    help = "List the event calendar groups of a give campus."

    def add_arguments(self, parser):
        parser.add_argument('campus_code',
                            choices=['sea', 'bot', 'tac'])

    def handle(self, *args, **options):
        campus_code = options['campus_code']
        gro_m = GroupManager()
        print "Total number of %s groups: %d" % (campus_code,
                                                 gro_m.len(campus_code))
        if gro_m.exists(campus_code):
            result = gro_m.get_all_groups(campus_code)
            if result is not None:
                for uwcalgroup in result:
                    print " %s %s" % (uwcalgroup.name, uwcalgroup.title)
