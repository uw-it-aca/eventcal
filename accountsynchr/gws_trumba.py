import logging
from restclients.models.trumba import TrumbaCalendar
from accountsynchr.ucalgroup.group_manager import GroupManager
from accountsynchr.ucalgroup.member_manager import MemberManager
from accountsynchr.trumba.permission_manager import PermissionManager
from accountsynchr.log import log_resp_time


logger = logging.getLogger(__name__)


class GwsToTrumba:

    def __init__(self):
        self.per_m = PermissionManager()
        self.gro_m = GroupManager()
        self.mem_m = MemberManager()
        self.new_acounts = 0
        self.new_acount_errs = 0
        self.new_editor_perm_counts = 0
        self.err_editor_perm_counts = 0
        self.new_showon_perm_counts = 0
        self.err_showon_perm_counts = 0

    def sync(self):
        """
        Synchronizes new editor/showon accounts from GWS to Trumba
        """
        self.sync_accounts()
        logger.info("%d new accounts added, %d failed" %
                    (self.new_acounts,
                     self.new_acount_errs))

        self.sync_campus_perm(TrumbaCalendar.SEA_CAMPUS_CODE)
        self.sync_campus_perm(TrumbaCalendar.BOT_CAMPUS_CODE)
        self.sync_campus_perm(TrumbaCalendar.TAC_CAMPUS_CODE)
        logger.info("%d editor permissions added, %d failed" %
                    (self.new_editor_perm_counts,
                     self.err_editor_perm_counts))
        logger.info("%d showon permissions added, %d failed" %
                    (self.new_showon_perm_counts,
                     self.err_showon_perm_counts))

    def sync_accounts(self):
        """
        Create new Trumba accounts for any new members in GWS
        """
        member_set = self.mem_m.get_all_members()
        account_set = self.per_m.get_all_accounts()
        for uwnetid in member_set:
            if uwnetid not in account_set:
                logger.debug("To create account: %s" % uwnetid)
                if PermissionManager.add_account(uwnetid, uwnetid):
                    self.new_acounts = self.new_acounts + 1
                else:
                    self.new_acount_errs = self.new_acount_errs + 1

    def sync_campus_perm(self, campus_code):
        """
        Synchronizes permissions from GWS to Trumba
        for the given campus
        """
        if self.gro_m.exists(campus_code):
            for uwcal_group in self.gro_m.get_all_groups(campus_code):
                self.sync_cal_perm(uwcal_group)

    def sync_cal_perm(self, uwcal_group):
        """
        Synchronizes the editor and showon permissions
        from GWS to Trumba for the Trumba calendar
        corresponding to the given UwcalGroup object.
        :param uwcal_group: a UwcalGroup object
        """
        trumba_cal = uwcal_group.calendar
        grp_member_list = self.mem_m.get_members(uwcal_group)
        if grp_member_list is None or len(grp_member_list) == 0:
            return
        logger.debug("To sync perm for %s" % uwcal_group)
        if uwcal_group.is_editor_group():
            for group_member in grp_member_list:
                if group_member.is_uwnetid():
                    self.sync_editor_perm(trumba_cal,
                                          group_member.name)
        elif uwcal_group.is_showon_group():
            for group_member in grp_member_list:
                if group_member.is_uwnetid():
                    self.sync_showon_perm(trumba_cal,
                                          group_member.name)

    def sync_editor_perm(self, trumba_cal, uwnetid):
        if self.per_m.is_editor(trumba_cal, uwnetid):
            return
        if PermissionManager.set_editor_permission(trumba_cal, uwnetid):
            self.new_editor_perm_counts = self.new_editor_perm_counts + 1
        else:
            self.err_editor_perm_counts = self.err_editor_perm_counts + 1
            logger.error(
                "Failed to set %s editor for %s" % (uwnetid, trumba_cal))

    def sync_showon_perm(self, trumba_cal, uwnetid):
        if self.per_m.is_showon(trumba_cal, uwnetid) or\
                self.per_m.is_editor(trumba_cal, uwnetid):
            return
        if PermissionManager.set_showon_permission(trumba_cal, uwnetid):
            self.new_showon_perm_counts = self.new_showon_perm_counts + 1
        else:
            self.err_showon_perm_counts = self.err_showon_perm_counts + 1
            logger.error(
                "Failed to set %s showon for %s" % (uwnetid, trumba_cal))

    def del_accounts(self):
        """
        Clean up the no-longer used accounts from Trumba
        """
        pass
