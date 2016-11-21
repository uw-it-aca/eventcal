"""
This class provides GWS Group related methods
"""
import logging
from restclients.models.trumba import make_group_name, UwcalGroup,\
    TrumbaCalendar, UwcalGroup
from accountsynchr.ucalgroup import get_campus_groups, del_group, put_group


logger = logging.getLogger(__name__)


class GroupManager:

    def __init__(self):
        self.campus_uwcalgroup_dict = {}
        # {campus code: {group name: UwcalGroup}}

    def _get_dict(self, campus_code):
        """
        :return: the dictionary object of {calendarid, UwcalGroup}
        of the given campus
        """
        if campus_code not in self.campus_uwcalgroup_dict:
            self.campus_uwcalgroup_dict[campus_code] =\
                get_campus_groups(campus_code)
        return self.campus_uwcalgroup_dict[campus_code]

    def del_uwcalgroup(self, uwcal_group):
        """
        :return: True if succesful
        """
        campus_code = uwcal_group.get_campus_code()
        name = uwcal_group.name
        if self.has_group(campus_code, name) and\
                del_group(uwcal_group):
            del self._get_dict(campus_code)[name]
            return True
        return False

    def exists(self, campus_code):
        """
        :return: true if the campus has some uw calendar groups
        """
        group_dict = self._get_dict(campus_code)
        return group_dict is not None and len(group_dict) > 0

    def get_all_groups(self, campus_code):
        """
        :return: the list of UwcalGroup object in the given campus
        """
        if self.exists(campus_code):
            return self._get_dict(campus_code).values()
        return None

    def get_group_names(self, campus_code):
        """
        :return: the list of group names in the given campus uwcal groups
        """
        if self.exists(campus_code):
            return self._get_dict(campus_code).keys()
        return None

    def get_group_by_name(self, campus_code, group_name):
        """
        :return: the UwcalGroup object with the given group_name
        """
        if self.has_group_name(campus_code, group_name):
            return self._get_dict(campus_code)[group_name]
        return None

    def get_editor_group(self, trumba_cal):
        """
        :return: the UwcalGroup object of the corresponding
        editor group for the given TrumbaCalendar object
        """
        return self.get_group_by_name(
            trumba_cal.campus,
            GroupManager._make_editor_group_name(trumba_cal))

    def get_showon_group(self, trumba_cal):
        """
        :return: the UwcalGroup object of the corresponding
        showon group for the given TrumbaCalendar object
        """
        return self.get_group_by_name(
            trumba_cal.campus,
            GroupManager._make_showon_group_name(trumba_cal))

    def has_group_name(self, campus_code, group_name):
        """
        :return: true if the group_name is a key in the calendar
        group dictionary
        """
        return self.exists(campus_code) and\
            group_name in self.get_group_names(campus_code)

    def has_editor_group(self, trumba_cal):
        """
        :param trumba_cal: a TrumbaCalendar object
        :return: True if the corresponding editor UwcalGroup exists
        """
        return self.has_group_name(
            trumba_cal.campus,
            GroupManager._make_editor_group_name(trumba_cal))

    def has_showon_group(self, trumba_cal):
        """
        :param trumba_cal: a TrumbaCalendar object
        :return: True if the corresponding showon UwcalGroup exists
        """
        return self.has_group_name(
            trumba_cal.campus,
            GroupManager._make_showon_group_name(trumba_cal))

    def len(self, campus_code):
        """
        :return: the number of uw calendar groups for the given campus
        """
        if self.exists(campus_code):
            return len(self._get_dict(campus_code))
        else:
            return 0

    @staticmethod
    def _make_editor_group_name(trumba_cal):
        return make_group_name(trumba_cal.campus,
                               trumba_cal.calendarid,
                               UwcalGroup.GTYEP_EDITOR)

    @staticmethod
    def _make_showon_group_name(trumba_cal):
        return make_group_name(trumba_cal.campus,
                               trumba_cal.calendarid,
                               UwcalGroup.GTYEP_SHOWON)

    @staticmethod
    def _new_editor_group(trumba_cal):
        """
        :param trumba_cal: a TrumbaCalendar object
        Create an editor UwcalGroup object
        """
        return UwcalGroup(calendar=trumba_cal,
                          gtype=UwcalGroup.GTYEP_EDITOR)

    @staticmethod
    def _new_showon_group(trumba_cal):
        """
        :param trumba_cal: a TrumbaCalendar object
        Create a showon UwcalGroup object
        """
        return UwcalGroup(calendar=trumba_cal,
                          gtype=UwcalGroup.GTYEP_SHOWON)

    def _put_in_dict(self, uwcal_group):
        """
        Add the uwcal_group object into the dict
        :param uwcal_group: the UwcalGroup object to be added
        """
        self._get_dict(uwcal_group.get_campus_code())[uwcal_group.name] =\
            uwcal_group

    def _put_group(self, uwcal_group):
        """
        Add or update the group in GWS
        :param uwcal_group: the UwcalGroup object to be added
        :return: the UwcalGroup object with the group regid if successful;
                 None if failed
        """
        gwsgroup = put_group(uwcal_group)
        if gwsgroup is None:
            return None
        uwcal_group.uwregid = gwsgroup.uwregid
        self._put_in_dict(uwcal_group)
        return uwcal_group

    def put_editor_group(self, trumba_cal):
        """
        :param trumba_cal: a TrumbaCalendar object
        :return: the UwcalGroup object added, None is failed
        """
        if self.has_editor_group(trumba_cal):
            uwcal_group, no_change = GroupManager.upd_group_title(
                self.get_editor_group(trumba_cal),
                trumba_cal)
            if no_change:
                return uwcal_group
        else:
            uwcal_group = GroupManager._new_editor_group(trumba_cal)
        return self._put_group(uwcal_group)

    def put_showon_group(self, trumba_cal):
        """
        :param trumba_cal: a TrumbaCalendar object
        :return: the UwcalGroup object added, None is failed
        """
        if self.has_showon_group(trumba_cal):
            uwcal_group, no_change = GroupManager.upd_group_title(
                self.get_showon_group(trumba_cal),
                trumba_cal)
            if no_change:
                return uwcal_group
        else:
            uwcal_group = GroupManager._new_showon_group(trumba_cal)
        return self._put_group(uwcal_group)

    @staticmethod
    def upd_group_title(uwcal_group, trumba_cal):
        """
        :return: the UwcalGroup object with the title updated
        according to the calendar name
        """
        no_change = True
        if uwcal_group.title != trumba_cal.name:
            uwcal_group.title = trumba_cal.name
            no_change = False
        return uwcal_group, no_change
