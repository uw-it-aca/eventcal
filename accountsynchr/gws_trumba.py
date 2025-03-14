# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import logging
import traceback
from uw_trumba.models import TrumbaCalendar
from accountsynchr.syncer import Syncer
from accountsynchr.dao.trumba import (
    set_editor_permission, set_showon_permission)
from accountsynchr.util.log import log_resp_time, log_exception

logger = logging.getLogger(__name__)


class GwsToTrumba(Syncer):

    def __init__(self):
        super(GwsToTrumba, self).__init__()
        self.new_acounts = 0
        self.new_editor_perm_counts = 0
        self.new_showon_perm_counts = 0

    def sync(self):
        """
        Synchronizes new editor/showon accounts from GWS to Trumba
        """
        self.sync_accounts()
        logger.info("{0:d} new accounts added".format(
                self.new_acounts))

        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            for u_group in self.gro_m.get_campus_editor_groups(campus_code):
                if len(u_group.members) > 0:
                    self.sync_editor_group_perm(u_group)

            for u_group in self.gro_m.get_campus_showon_groups(campus_code):
                if len(u_group.members) > 0:
                    self.sync_showon_group_perm(u_group)

        logger.info("{0:d} editor permissions added".format(
                self.new_editor_perm_counts))
        logger.info("{0:d} showon permissions added".format(
                self.new_showon_perm_counts))
        if self.has_err():
            logger.error(self.get_error_report())

    def sync_accounts(self):
        """
        Create new Trumba accounts for any new members in GWS
        """
        for gmember in self.gro_m.get_all_editors():
            uwnetid = gmember.name
            if not self.cal_per_m.account_exists(uwnetid):
                self._add_account(uwnetid)

    def _add_account(self, uwnetid):
        action = "Create account: {0}".format(uwnetid)
        try:
            if self.cal_per_m.add_account(uwnetid, uwnetid) is True:
                self.new_acounts += 1
                logger.info(action)
        except Exception as ex:
            log_exception(logger, action, traceback.format_exc(chain=False))
            self.append_error("Failed to {0} {1}\n".format(action, ex))

    def _check_cal(self, uwcal_group):
        trumba_cal = self.cal_per_m.get_calendar(
            uwcal_group.calendar.campus, uwcal_group.calendar.calendarid)
        if (trumba_cal is None):
            logger.error("{0} is missing!".format(uwcal_group.calendar))
            self.append_error(
                "{0} is missing! Please check!\n".format(uwcal_group.calendar))
            return None
        return trumba_cal

    def sync_editor_group_perm(self, uwcal_group):
        trumba_cal = self._check_cal(uwcal_group)
        if trumba_cal is not None:
            for gm in uwcal_group.members:
                self.sync_editor_perm(trumba_cal, gm.name)

    def sync_showon_group_perm(self, uwcal_group):
        trumba_cal = self._check_cal(uwcal_group)
        if trumba_cal is not None:
            for gm in uwcal_group.members:
                self.sync_showon_perm(trumba_cal, gm.name)

    def sync_editor_perm(self, trumba_cal, uwnetid):
        action = "Set editor permission for {0} of {1}_{2}".format(
            uwnetid, trumba_cal.campus, trumba_cal.calendarid)
        try:
            ret = set_editor_permission(trumba_cal, uwnetid)
            if ret >= 0:
                self.new_editor_perm_counts += ret
        except Exception as ex:
            log_exception(logger, "Failed to {0}".format(action),
                          traceback.format_exc(chain=False))
            self.append_error("Failed to {0} {1}\n".format(action, ex))

    def sync_showon_perm(self, trumba_cal, uwnetid):
        action = "Set showon permission for {0} of {1}_{2}".format(
            uwnetid, trumba_cal.campus, trumba_cal.calendarid)
        try:
            ret = set_showon_permission(trumba_cal, uwnetid)
            if ret >= 0:
                self.new_showon_perm_counts += ret
        except Exception as ex:
            log_exception(logger, "Failed to {0}".format(action),
                          traceback.format_exc(chain=False))
            self.append_error("Failed to {0} {1}\n".format(action, ex))
