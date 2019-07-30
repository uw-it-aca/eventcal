import logging
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.ucalgroup.group_manager import GroupManager


logger = logging.getLogger("eventcal.commands")


class Command(BaseCommand):
    """
    List the event calendar groups of a give campus.
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        gro_m = GroupManager()

        logger.info(
            "Total {0:d} editors".format(len(gro_m.get_all_editors())))

        logger.info(
            "Seattle has total {0:d} editor, {1:d} showon groups".format(
                len(gro_m.get_campus_editor_groups('sea')),
                len(gro_m.get_campus_showon_groups('sea'))))

        logger.info(
            "Bothell has total {0:d} editor, {1:d} showon groups".format(
                len(gro_m.get_campus_editor_groups('bot')),
                len(gro_m.get_campus_showon_groups('bot'))))

        logger.info(
            "Tacoma has total {0:d} editor, {1:d} showon groups".format(
                len(gro_m.get_campus_editor_groups('tac')),
                len(gro_m.get_campus_showon_groups('tac'))))
