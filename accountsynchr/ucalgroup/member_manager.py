import logging
from restclients.models.gws import GroupMember
from restclients.models.trumba import Permission, TrumbaCalendar, UwcalGroup
from accountsynchr.ucalgroup import get_members, update_members
from accountsynchr.ucalgroup.group_manager import GroupManager


logger = logging.getLogger(__name__)


class MemberManager:
    """
    The UW Event Calendar Group Member class
    """

    def __init__(self):
        self.group_member_dict = {}
        # {group_name: a list of gws.GroupMember objects}

    def get_campus_editors(self, campus_code):
        """
        :return: a set of UWNetIDs of the members of
        all the editor groups for a given campus
        """
        member_set = set()
        gro_m = GroupManager()
        campus_groups = gro_m.get_all_groups(campus_code)
        if campus_groups is not None and len(campus_groups) > 0:
            for group in campus_groups:
                if group.is_editor_group():
                    member_list = self.get_members(group)
                    if member_list is None or len(member_list) == 0:
                        continue
                    for member in member_list:
                        if member.is_uwnetid() and\
                                member.name not in member_set:
                            member_set.add(member.name)
        return sorted(member_set)

    def get_all_members(self):
        """
        :return: a set of UWNetIDs of the members of all the editor groups
        """
        member_set = set()
        for campus_code in (TrumbaCalendar.SEA_CAMPUS_CODE,
                            TrumbaCalendar.BOT_CAMPUS_CODE,
                            TrumbaCalendar.TAC_CAMPUS_CODE):
            member_set.update(self.get_campus_editors(campus_code))
        return member_set

    def get_members(self, uwcal_group):
        """
        :return: a list of GroupMember objects
                 None if error, [] if the group has no members
        """
        if uwcal_group is not None:
            return self.get_members_by_groupid(uwcal_group.name)

    def get_members_by_groupid(self, group_name):
        """
        :return: a list of GroupMember objects
                 None if the group not exists.
        """
        if group_name not in self.group_member_dict:
            self.group_member_dict[group_name] = get_members(group_name)
        return self.group_member_dict[group_name]

    def is_member(self, group_name, uwnetid):
        """
        :return: True if the uwnetid matches a GroupMember's
        """
        member_list = self.get_members_by_groupid(group_name)
        for member in member_list:
            if member.member_type == 'uwnetid' and member.name == uwnetid:
                return True
        return False

    @staticmethod
    def _convert_to_groupmember_list(perm_list):
        """
        Convert permission list into a list of GroupMember objects
        :return: a list of GroupMember
        """
        group_members = []
        for perm in perm_list:
            group_members.append(
                GroupMember(name=perm.uwnetid,
                            member_type=GroupMember.UWNETID_TYPE))
        return group_members

    @staticmethod
    def update_editor_group_members(group_name, editor_perm_list):
        """
        Update the members of the corresponding group in GWS
        :param editor_perm_list: Permission[]
        """
        return update_members(
            group_name,
            MemberManager._convert_to_groupmember_list(editor_perm_list))
