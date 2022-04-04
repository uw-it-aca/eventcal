# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import logging
from uw_trumba.models import TrumbaCalendar, EDITOR, SHOWON
from accountsynchr.syncer import Syncer
from accountsynchr.dao.trumba import get_cal_permissions, remove_permission

logger = logging.getLogger(__name__)


class TrumbaToGws(Syncer):

    def __init__(self):
        super(TrumbaToGws, self).__init__()
        self.ttl_editor_grps_synced = 0
        self.ttl_showon_grp_synced = 0
        self.del_editor_perm_counts = 0
        self.del_showon_perm_counts = 0

    def sync(self):
        """
        Synchronizes changes from Trumba to GWS
        """
        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            if self.cal_per_m.exists(campus_code):
                calendars = self.cal_per_m.get_campus_calendars(campus_code)
                for cal in calendars:
                    self.sync_cal_to_groups(cal)

        logger.info("{0:d} editor groups sync-ed".format(
                self.ttl_editor_grps_synced))
        logger.info("{0:d} showon groups sync-ed".format(
                self.ttl_showon_grp_synced))
        logger.info("{0:d} editor perm deleted".format(
                self.del_editor_perm_counts))
        logger.info("{0:d} showon perm deleted".format(
                self.del_showon_perm_counts))
        if self.has_err():
            logger.error(self.get_error_report())

    def sync_cal_to_groups(self, trumba_cal):
        """
        Synchronizes accounts from Trumba to the corresponding
        calendar editor and showon groups for the following changes:
         - Group creation
         - Title update
         - Clean up the permissions no longer Group member
        :param trumba_cal: a TrumbaCalendar object
        """
        self.put_editor_group(trumba_cal,
                              not self.gro_m.has_editor_group(trumba_cal))
        self.put_showon_group(trumba_cal,
                              not self.gro_m.has_showon_group(trumba_cal))

    def put_editor_group(self, trumba_cal, is_new_calendar):
        """
        Create the corrsponding editor group
        or update the group general info
        """
        uwcal_group = self.gro_m.put_editor_group(trumba_cal)
        if uwcal_group is None:
            self.append_error("Failed to update editor group {0}\n".format(
                trumba_cal.get_group_name(EDITOR)))
            return
        self.ttl_editor_grps_synced += 1
        if not is_new_calendar:
            self.sync_edit_perms(trumba_cal, uwcal_group)

    def put_showon_group(self, trumba_cal, is_new_calendar):
        """
        Create the corrsponding showon group
        or update the group general info
        """
        uwcal_group = self.gro_m.put_showon_group(trumba_cal)
        if uwcal_group is None:
            self.append_error("Failed to update showon group {0}\n".format(
                trumba_cal.get_group_name(SHOWON)))
            return
        self.ttl_showon_grp_synced += 1
        if not is_new_calendar:
            self.sync_showon_perms(trumba_cal, uwcal_group)

    def sync_edit_perms(self, trumba_cal, uwcal_group):
        """
        Delete the edit permission no longer having the membership
        """
        for perm in get_cal_permissions(trumba_cal):
            if not perm.in_editor_group():
                continue
            uwnetid = perm.uwnetid
            if not_member(uwcal_group, uwnetid):
                if remove_permission(trumba_cal, uwnetid) is True:
                    self.del_editor_perm_counts += 1
                    logger.info("Removed editor {0} from {1}".format(
                            uwnetid, trumba_cal.name))
                else:
                    self.append_error(
                        "Failed to remove editor {0} from {1}\n".format(
                            uwnetid, trumba_cal.name))

    def sync_showon_perms(self, trumba_cal, uwcal_group):
        """
        Delete the showon permission no longer having the correspoding
        membership
        """
        for perm in get_cal_permissions(trumba_cal):
            if not perm.in_showon_group():
                continue
            uwnetid = perm.uwnetid
            if not_member(uwcal_group, uwnetid):
                if remove_permission(trumba_cal, uwnetid) is True:
                    logger.info("Removed showon {0} from {1}".format(
                            uwnetid, trumba_cal.name))
                    self.del_showon_perm_counts += 1
                else:
                    self.append_error(
                        "Failed to remove showon {0} from {1}\n".format(
                            uwnetid, trumba_cal.name))


def not_member(uwcal_group, uwnetid):
    for gmember in uwcal_group.members:
        if gmember.name == uwnetid:
            return False
    return True
