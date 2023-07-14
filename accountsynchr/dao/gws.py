# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


"""
The functions here interact with uw_gws
"""

import logging
import re
import traceback
from uw_gws import GWS
from uw_gws.models import Group, GroupEntity, GroupMember
from uw_trumba.models import (
    is_valid_campus_code, EDITOR, SHOWON, TrumbaCalendar)
from accountsynchr.dao import DataFailureException
from accountsynchr.models import UwcalGroup, get_cal_name
from accountsynchr.util.log import log_resp_time, Timer, log_exception


logger = logging.getLogger(__name__)
GROUP_NAME = re.compile(r'^u_eventcal_([a-z]{3})_([1-9]\d*)-([es][a-z]{5})$')


class Gws(GWS):

    def __init__(self):
        super(Gws, self).__init__()
        self.all_editors = []  # GroupMember objects
        self.all_editor_uwnetids = set()

    def get_campus_groups(self, campus_code):
        """
        Search campus specific trumba calendar groups
        :param campus_code: a string of format: {bot,sea,tac}
        :return: a dict of {'editor': {group-id, UwcalGroup},
                            'showon': {group-id, UwcalGroup}}
        :except: DataFailureException
        """
        action = "search {0} groups".format(campus_code)
        timer = Timer()
        if is_valid_campus_code(campus_code):
            try:
                return self._load_dicts(
                    self.search_groups(
                        stem="u_eventcal_{0}".format(campus_code), name=""))
            finally:
                log_resp_time(logger, action, timer)
        return None

    def _get_group_members(self, group_id):
        """
        :param group_id: the name or uwregid of the uw group
        :return: a list of GroupMember objects
                 [] if the group has no members,
        except: DataFailureException
        """
        ret_list = []
        action = "get_effective_members('{0}')".format(group_id)
        for gm in self.get_effective_members(group_id):
            if (gm.is_uwnetid() and
                    gm.name is not None and len(gm.name) > 0):
                ret_list.append(gm)
        return ret_list

    def _load_dicts(self, group_refs):
        """
        :param group_refs: an array of GroupReference objects
        :return: a dict of {'editor': {group-id, UwcalGroup},
                            'showon': {group-id, UwcalGroup}}
        """
        campus_editor_groups = {}
        campus_showon_groups = {}
        if group_refs is not None and len(group_refs) > 0:
            for gr in group_refs:
                if re.match(r'^u_eventcal_[a-z]{3}$', gr.name):
                    # skip parent group
                    continue
                calgr = None
                calgr = _convert_to_uwcalgroup(gr)
                if calgr is not None:
                    group_id = calgr.get_group_id()
                    calgr.members = self._get_group_members(group_id)

                    if calgr.is_editor_group():
                        campus_editor_groups[group_id] = calgr
                        self._record_editors(calgr.members)

                    if calgr.is_showon_group():
                        campus_showon_groups[group_id] = calgr

        return {EDITOR: campus_editor_groups,
                SHOWON: campus_showon_groups}

    def _record_editors(self, editor_group_members):
        if len(editor_group_members) == 0:
            return
        for gmember in editor_group_members:
            if gmember.name not in self.all_editor_uwnetids:
                self.all_editor_uwnetids.add(gmember.name)
                self.all_editors.append(gmember)

    def is_existing_editor(self, uwnetid):
        return uwnetid in self.all_editor_uwnetids

    def put_group(self, uwcalgroup):
        """
        Create or update the UW Group
        :return: an uw_gws Group object if successful, None otherwise
        """
        timer = Timer()
        gwsgroup = _convert_to_gwsgroup(uwcalgroup)
        is_update = gwsgroup.has_regid()

        action = "{0} group {1}".format(
            "Update" if is_update else "Create", gwsgroup.name)
        try:
            if is_update:
                return self.update_group(gwsgroup)
            return self.create_group(gwsgroup)
        except DataFailureException:
            log_exception(logger, action, traceback.format_exc(chain=False))
        finally:
            log_resp_time(logger, action, timer)
        return None

    def get_uw_group(self, trumba_calendar, type):
        """
        Returns a restclients.gws Group object
        """
        group_id = trumba_calendar.get_group_name(type)
        action = "get_{}_group {}".format(type, group_id)
        try:
            return self.get_group_by_id(group_id)
        except DataFailureException:
            log_exception(logger, action, traceback.format_exc(chain=False))
        return None


def _convert_to_uwcalgroup(group_ref):
    m = GROUP_NAME.match(group_ref.name)
    if m is not None and len(m.groups()) == 3:
        campus = m.group(1)
        calendarid = int(m.group(2))
        gtype = m.group(3)
    else:
        logger.warning(
            "Skip it due to invalid group name: {0}".format(group_ref.name))
        return None

    cal = TrumbaCalendar(calendarid=calendarid,
                         campus=campus,
                         name=get_cal_name(group_ref.display_name))
    calgr = UwcalGroup(calendar=cal,
                       gtype=gtype,
                       group_ref=group_ref)
    return calgr


def _convert_to_gwsgroup(uwcalgroup):
    """
    :param uwcalgroup: an UwcalGroup object
    :return: a uw_gws.models.Group object
    Convert/map the given UwcalGroup object into a Group object
    """
    group = Group(uwregid=uwcalgroup.get_regid(),
                  name=uwcalgroup.get_group_name(),
                  display_name=uwcalgroup.get_group_title(),
                  description=uwcalgroup.get_group_desc())
    group.admins = [GroupEntity(name=uwcalgroup.get_group_admin(),
                                type=GroupEntity.GROUP_TYPE)]
    group.updaters = [GroupEntity(name=uwcalgroup.get_member_manager(),
                                  type=GroupEntity.GROUP_TYPE)]
    group.readers = [GroupEntity(name='all',
                                 type=GroupEntity.SET_TYPE)]
    group.optouts = [GroupEntity(name='all',
                                 type=GroupEntity.SET_TYPE)]
    return group
