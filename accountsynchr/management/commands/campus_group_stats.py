from django.core.management.base import BaseCommand, CommandError
from accountsynchr.ucalgroup.group_manager import GroupManager


class Command(BaseCommand):
    """
    List the event calendar groups of a give campus.
    """

    def add_arguments(self, parser):
        parser.add_argument('campus_code',
                            choices=['sea', 'bot', 'tac'])

    def handle(self, *args, **options):
        campus_code = options['campus_code']
        gro_m = GroupManager()

        print("Total {1:d} editors".format(gro_m.get_all_editors))
        print("{0} campus has total {1:d} editor, {2:d} showon groups".format(
                campus_code,
                gro_m.get_campus_editor_groups(),
                gro_m.get_campus_showon_groups()))
