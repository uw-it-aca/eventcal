import logging
from django.core.management.base import BaseCommand, CommandError
from uw_trumba.models import TrumbaCalendar
from accountsynchr.ucalgroup.group_manager import GroupManager


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Find all the groups the given uwnetid is in
    """

    def add_arguments(self, parser):
        parser.add_argument('uwnetid')

    def handle(self, *args, **options):
        userid = options['uwnetid']

        gro_m = GroupManager()
        for campus_code in (TrumbaCalendar.SEA_CAMPUS_CODE,
                            TrumbaCalendar.BOT_CAMPUS_CODE,
                            TrumbaCalendar.TAC_CAMPUS_CODE):
            for group in gro_m.get_campus_editor_groups(campus_code):
                for member in group.members:
                    if member.name == userid:
                        logger.info("{0}".format(group.group_ref.name))

            for group in gro_m.get_campus_showon_groups(campus_code):
                for member in group.members:
                    if member.name == userid:
                        logger.info("{0}".format(group.group_ref.name))
