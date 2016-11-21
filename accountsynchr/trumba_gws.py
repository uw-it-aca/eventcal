import logging
from restclients.models.trumba import TrumbaCalendar
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.ucalgroup.member_manager import MemberManager
from accountsynchr.trumba.calendar_manager import CalendarManager
from accountsynchr.trumba.permission_manager import PermissionManager
from accountsynchr.log import log_resp_time


logger = logging.getLogger(__name__)


class TrumbaToGws:

    def __init__(self):
        self.cal_m = CalendarManager()
        self.per_m = PermissionManager()
        self.gro_m = GroupManager()
        self.mem_m = MemberManager()

        self.ttl_editor_grps_synced = 0
        self.upd_editor_grp_errs = 0
        self.editor_grp_mem_counts = 0

        self.ttl_showon_grp_synced = 0
        self.upd_showon_grp_errs = 0

        self.del_editor_perm_counts = 0
        self.err_del_editor_perm_counts = 0
        self.del_showon_perm_counts = 0
        self.err_del_showon_perm_counts = 0

    def sync(self, campus_code):
        """
        Synchronizes changes from Trumba to GWS
        """
        if campus_code is None or\
                campus_code == TrumbaCalendar.SEA_CAMPUS_CODE:
            self.sync_campus_groups(TrumbaCalendar.SEA_CAMPUS_CODE)

        if campus_code is None or\
                campus_code == TrumbaCalendar.BOT_CAMPUS_CODE:
            self.sync_campus_groups(TrumbaCalendar.BOT_CAMPUS_CODE)

        if campus_code is None or\
                campus_code == TrumbaCalendar.TAC_CAMPUS_CODE:
            self.sync_campus_groups(TrumbaCalendar.TAC_CAMPUS_CODE)

        logger.info("%d editor groups sync-ed, %d failed." %
                    (self.ttl_editor_grps_synced,
                     self.upd_editor_grp_errs))
        logger.info("%d editor groups sync-ed members." %
                    self.editor_grp_mem_counts)
        logger.info("%d showon groups sync-ed, %d failed." %
                    (self.ttl_showon_grp_synced,
                     self.upd_showon_grp_errs))

    def sync_campus_groups(self, campus_code):
        """
        Synchronizes changes from Trumba to GWS for the
        given campus code
        """
        if self.cal_m.exists(campus_code):
            for trumba_cal in self.cal_m.get_all_calendars(campus_code):
                self.sync_cal_groups(trumba_cal)

    def sync_cal_groups(self, trumba_cal):
        """
        Synchronizes information from Trumba to GWS for the
        corresponding event calendar groups for the given TrumbaCalendar
        object for the following changes:
         - group creation
         - title update
         - member updates of the editor group
        :param trumba_cal: a TrumbaCalendar object
        """
        is_new_calendar = not self.gro_m.has_editor_group(trumba_cal)
        self.put_editor_group(trumba_cal, is_new_calendar)
        self.put_showon_group(trumba_cal, is_new_calendar)

    def put_editor_group(self, trumba_cal, is_new_calendar):
        """
        Create the corrsponding editor group
        or update the group general info
        """
        editor_group = self.gro_m.put_editor_group(trumba_cal)
        if editor_group is None:
            self.upd_editor_grp_errs = self.upd_editor_grp_errs + 1
            logger.error(
                "Failed to sync editor group for %s" % trumba_cal)
        else:
            self.ttl_editor_grps_synced = self.ttl_editor_grps_synced + 1
            if is_new_calendar:
                self.sync_group_members(trumba_cal, editor_group)
            else:
                self.sync_edit_perms(trumba_cal, editor_group)

    def sync_group_members(self, trumba_cal, editor_group):
        """
        Add editor group members for editor permissions
        set in Trumba.
        """
        if self.per_m.has_editor(trumba_cal):
            editors = self.per_m.get_editor_permissions(trumba_cal)
            logger.debug(
                "To sync %d members to %s" % (len(editors),
                                              editor_group))
            MemberManager.update_editor_group_members(
                editor_group.name, editors)
            self.editor_grp_mem_counts = self.editor_grp_mem_counts + 1

    def sync_edit_perms(self, trumba_cal, editor_group):
        """
        Delete the edit permission no longer having the correspoding
        member in the editor group
        """
        edit_perm_list = self.per_m.get_editor_permissions(trumba_cal)
        for perm in edit_perm_list:
            # currently having edit permission in Trumba
            if not self.mem_m.is_member(editor_group.name, perm.uwnetid):
                # not an editer group member

                logger.info("TO REMOVE editor %s from %s" % (perm.uwnetid,
                                                             trumba_cal))
                success = self.per_m.remove_permission(trumba_cal,
                                                       perm.uwnetid)
                if success:
                    self.del_editor_perm_counts =\
                        self.del_editor_perm_counts + 1
                else:
                    logger.error(
                        "Failed to remove editor %s from %s" % (perm.uwnetid,
                                                                trumba_cal))
                    self.err_del_editor_perm_counts =\
                        self.err_del_editor_perm_counts + 1

    def put_showon_group(self, trumba_cal, is_new_calendar):
        """
        Create the corrsponding showon group
        or update the group general info
        """
        showon_group = self.gro_m.put_showon_group(trumba_cal)
        if showon_group is None:
            self.upd_showon_grp_errs = self.upd_showon_grp_errs + 1
            logger.error(
                "Failed to sync showon group for %s" % trumba_cal)
        else:
            self.ttl_showon_grp_synced = self.ttl_showon_grp_synced + 1
            if not is_new_calendar:
                self.sync_showon_perms(trumba_cal, showon_group)

    def sync_showon_perms(self, trumba_cal, showon_group):
        """
        Delete the showon permission no longer having the correspoding
        member in the showon group
        """
        showon_perm_list = self.per_m.get_showon_permissions(trumba_cal)
        for perm in showon_perm_list:
            # currently having showon permission in Trumba
            if not self.mem_m.is_member(showon_group.name, perm.uwnetid):
                # not an showon group member

                logger.info("TO REMOVE showon %s from %s" % (perm.uwnetid,
                                                             trumba_cal))
                success = self.per_m.remove_permission(trumba_cal,
                                                       perm.uwnetid)
                if success:
                    self.del_showon_perm_counts =\
                        self.del_showon_perm_counts + 1
                else:
                    logger.error(
                        "Failed to remove showon %s from %s" % (perm.uwnetid,
                                                                trumba_cal))
                    self.err_del_showon_perm_counts =\
                        self.err_del_showon_perm_counts + 1
