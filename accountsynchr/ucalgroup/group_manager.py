# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


"""
This class provides GWS Group related methods
"""
import logging
from uw_trumba.models import TrumbaCalendar
from accountsynchr.models import (
    UwcalGroup, EDITOR, SHOWON, new_editor_group, new_showon_group)
from accountsynchr.dao.gws import Gws

logger = logging.getLogger(__name__)


class GroupManager:

    def __init__(self):
        self.gws = Gws()

        # {campus_code: {group-id: UwcalGroup}}
        self.campus_editor_groups = {}
        self.campus_showon_groups = {}

        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            result = self.gws.get_campus_groups(campus_code)

            campus_editor_groups = result[EDITOR]
            self.campus_editor_groups[campus_code] = campus_editor_groups
            self.campus_showon_groups[campus_code] = result[SHOWON]

    def get_all_editors(self):
        return self.gws.all_editors

    def get_campus_editor_groups(self, campus_code):
        """
        :return: the list of UwcalGroup object in the given campus
        """
        return self.campus_editor_groups[campus_code].values()

    def get_campus_showon_groups(self, campus_code):
        """
        :return: the list of UwcalGroup object in the given campus
        """
        return self.campus_showon_groups[campus_code].values()

    def get_editor_group(self, trumba_cal):
        """
        :return: the UwcalGroup object of the corresponding
        editor group for the given TrumbaCalendar object
        """
        return self.campus_editor_groups[trumba_cal.campus].get(
            trumba_cal.get_group_name(EDITOR))

    def get_showon_group(self, trumba_cal):
        """
        :return: the UwcalGroup object of the corresponding
        showon group for the given TrumbaCalendar object
        """
        return self.campus_showon_groups[trumba_cal.campus].get(
            trumba_cal.get_group_name(SHOWON))

    def has_editor_group(self, trumba_cal):
        """
        :param trumba_cal: a TrumbaCalendar object
        :return: True if the corresponding editor UwcalGroup exists
        """
        return self.get_editor_group(trumba_cal) is not None

    def has_showon_group(self, trumba_cal):
        """
        :param trumba_cal: a TrumbaCalendar object
        :return: True if the corresponding showon UwcalGroup exists
        """
        return self.get_showon_group(trumba_cal) is not None

    def put_editor_group(self, trumba_cal):
        """
        Create or update the editor group for the trumba calendar
        :param trumba_cal: a TrumbaCalendar object
        :return: the UwcalGroup object created, None is failed
        """
        uwcal_group = self.get_editor_group(trumba_cal)
        if uwcal_group is not None:
            if uwcal_group.same_name(trumba_cal):
                return uwcal_group
            uwcal_group.set_calendar_name(trumba_cal.name)
        else:
            uwcal_group = new_editor_group(trumba_cal)
        return self._execute_put(uwcal_group)

    def put_showon_group(self, trumba_cal):
        """
        Create or update the showon group for the trumba calendar
        :param trumba_cal: a TrumbaCalendar object
        :return: the UwcalGroup object created, None is failed
        """
        uwcal_group = self.get_showon_group(trumba_cal)
        if uwcal_group is not None:
            if uwcal_group.same_name(trumba_cal):
                return uwcal_group
            uwcal_group.set_calendar_name(trumba_cal.name)
        else:
            uwcal_group = new_showon_group(trumba_cal)
        return self._execute_put(uwcal_group)

    def _execute_put(self, uwcal_group):
        gwsgroup = self.gws.put_group(uwcal_group)
        if (gwsgroup is not None and
                gwsgroup.name == uwcal_group.get_group_name()):
            # group id match
            uwcal_group.group_ref = gwsgroup
            return uwcal_group
        return None
