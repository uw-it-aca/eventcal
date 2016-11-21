from django.core.management.base import BaseCommand, CommandError
from restclients.models.trumba import make_group_name, UwcalGroup,\
    TrumbaCalendar
from accountsynchr.trumba.permission_manager import PermissionManager
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.ucalgroup.member_manager import MemberManager


class Command(BaseCommand):
    help = "Compare calendar permissions with the group members."

    def add_arguments(self, parser):
        parser.add_argument('campus_code',
                            choices=['sea', 'bot', 'tac'])
        parser.add_argument('calendar-id')

    def handle(self, *args, **options):
        campus_code = options['campus_code']
        calendar_id = options['calendar-id']
        trumba_cal = TrumbaCalendar(calendarid=calendar_id,
                                    campus=campus_code,
                                    name='none')
        editor_group_name = make_group_name(campus_code,
                                            calendar_id,
                                            UwcalGroup.GTYEP_EDITOR)
        showon_group_name = make_group_name(campus_code,
                                            calendar_id,
                                            UwcalGroup.GTYEP_SHOWON)

        per_m = PermissionManager()
        mem_m = MemberManager()

        Command.identify_missing_members(
            editor_group_name,
            per_m.get_editor_permissions(trumba_cal),
            mem_m)
        Command.identify_missing_members(
            showon_group_name,
            per_m.get_showon_permissions(trumba_cal),
            mem_m)

        editor_group_members = mem_m.get_members_by_groupid(editor_group_name)
        if editor_group_members is not None:
            for group_member in editor_group_members:
                if group_member.member_type != 'uwnetid':
                    continue
                if not per_m.is_editor(trumba_cal, group_member.name):
                    print "%s member %s missing edit permission" % (
                        editor_group_name, group_member.name)

        showon_group_members = mem_m.get_members_by_groupid(showon_group_name)
        if showon_group_members is not None:
            for group_member in showon_group_members:
                if group_member.member_type != 'uwnetid':
                    continue
                if not per_m.is_editor(trumba_cal, group_member.name) and\
                        not per_m.is_showon(trumba_cal, group_member.name):
                    print "%s member %s missing showon permission" % (
                        showon_group_name, group_member.name)

    @staticmethod
    def identify_missing_members(group_name, perm_list, mem_m):
        if perm_list is not None:
            for perm in perm_list:
                if not mem_m.is_member(group_name, perm.uwnetid):
                    print "Missing member of %s in group: %s" % (
                        perm, group_name)
