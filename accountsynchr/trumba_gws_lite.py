# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import logging
from uw_trumba.calendars import Calendars
from uw_trumba.models import TrumbaCalendar, EDITOR, SHOWON
from accountsynchr.models import new_editor_group, new_showon_group
from accountsynchr.models.gcalendar import GCalendar
from accountsynchr.dao.gws import Gws

logger = logging.getLogger(__name__)


class TrumbaGwsLite:
    def __init__(self):
        self.trumba_cals = Calendars()
        self.gws = Gws()
        self.updated_cals = []
        self.errors = []
        self.ttl_editor_grps_synced = 0
        self.ttl_showon_grp_synced = 0

    def append_error(self, message):
        self.errors.append(message)

    def get_error_report(self):
        return ',\n\n'.join(self.errors)

    def has_err(self):
        return len(self.errors) > 0

    def log_report(self):
        logger.info("{0:d} editor groups sync-ed".format(
            self.ttl_editor_grps_synced))
        logger.info("{0:d} showon groups sync-ed".format(
            self.ttl_showon_grp_synced))
        if self.has_err():
            logger.error(self.get_error_report())

    def sync(self):
        """
        Synchronizes calendar changes from Trumba to GCal to UW Groups
        """
        self.collect_changes()
        if len(self.updated_cals):
            for trumba_cal in self.updated_gcals:
                self.put_editor_group(trumba_cal)
                self.put_showon_group(trumba_cal)
            self.log_report()
        else:
            logger.info("No change detected.")

    def collect_changes(self):
        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            if self.trumba_cals.exists(campus_code):
                calendars = self.trumba_cals.get_campus_calendars(campus_code)
                for trumba_calendar in calendars:
                    if not GCalendar.exists(trumba_calendar):
                        # it is a new calendar, create editor, showon groups
                        trumba_calendar.is_new = True
                        if self.save_gcal(trumba_calendar) is not None:
                            self.updated_cals.append(trumba_calendar)
                    else:
                        gcal = GCalendar.objects.get(
                            calendarid=trumba_calendar.calendarid,
                            campus=trumba_calendar.campus)
                        if gcal.name != trumba_calendar.name:
                            trumba_calendar.is_new = False
                            if self.save_gcal(trumba_calendar) is not None:
                                self.updated_cals.append(trumba_calendar)

    def save_gcal(self, trumba_calendar):
        try:
            if trumba_calendar.is_new:
                return GCalendar.create(trumba_calendar)
            else:
                return GCalendar.update(trumba_calendar)
        except Exception as ex:
            self.append_error("Failed to {} GCalendar: {}\n".format(
                "create" if trumba_calendar.is_new else "update",
                {'calendarid': trumba_calendar.calendarid,
                 'campus': trumba_calendar.campus,
                 'name': trumba_calendar.name}))
        return None

    def put_editor_group(self, trumba_cal):
        """
        Create the corrsponding editor group
        or update the group general info
        """
        uw_editor_group = self.gws.get_uw_group(trumba_cal, EDITOR)
        editor_uwcalgroup = new_editor_group(
            trumba_cal, uw_editor_group)
        ret_group = self.gsw.put_group(editor_uwcalgroup)
        if ret_group is None:
            self.append_error("Failed to update editor group {0}\n".format(
                editor_uwcalgroup))
            return
        self.ttl_editor_grps_synced += 1

    def put_showon_group(self, trumba_cal):
        """
        Create the corrsponding showon group
        or update the group general info
        """
        uw_showon_group = self.gws.get_uw_group(trumba_cal, SHOWON)
        showon_uwcalgroup = new_showon_group(
            trumba_cal, uw_showon_group)
        ret_group = self.self.gsw.put_group(showon_uwcalgroup)
        if ret_group is None:
            self.append_error("Failed to update showon group {0}\n".format(
                showon_uwcalgroup))
            return
        self.ttl_showon_grp_synced += 1
