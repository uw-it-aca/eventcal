from django.core.management.base import BaseCommand, CommandError
from accountsynchr.ucalgroup.group_manager import GroupManager


class Command(BaseCommand):
    """
    List the event calendar groups of a give campus.
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        gro_m = GroupManager()

        print("Total {0:d} editors".format(len(gro_m.get_all_editors())))

        print("Seattle has total {0:d} editor, {1:d} showon groups".format(
                len(gro_m.get_campus_editor_groups('sea')),
                len(gro_m.get_campus_showon_groups('sea'))))

        print("Bothell has total {0:d} editor, {1:d} showon groups".format(
                len(gro_m.get_campus_editor_groups('bot')),
                len(gro_m.get_campus_showon_groups('bot'))))

        print("Tacoma has total {0:d} editor, {1:d} showon groups".format(
                len(gro_m.get_campus_editor_groups('tac')),
                len(gro_m.get_campus_showon_groups('tac'))))
