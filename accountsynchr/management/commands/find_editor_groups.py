import logging
from restclients.models.trumba import TrumbaCalendar
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.ucalgroup.member_manager import MemberManager


class Command(BaseCommand):
    """
    Find the membership of the given uwnetid
    """

    def add_arguments(self, parser):
        parser.add_argument('uwnetid')

    def handle(self, *args, **options):
        userid = options['uwnetid']
        mem_m = MemberManager()
        gro_m = GroupManager()
        for campus_code in (TrumbaCalendar.SEA_CAMPUS_CODE,
                            TrumbaCalendar.BOT_CAMPUS_CODE,
                            TrumbaCalendar.TAC_CAMPUS_CODE):
            all_groups = gro_m.get_all_groups(campus_code)
            for agroup in all_groups:
                result = mem_m.get_members(agroup)
                if result is not None:
                    for member in result:
                        if member.is_uwnetid() and\
                                member.name == userid:
                            print "%s %s" % (agroup.title, agroup.name)
