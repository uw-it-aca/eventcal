import logging
from restclients.exceptions import DataFailureException
from restclients.models.trumba import TrumbaCalendar, UwcalGroup
from restclients.trumba.account import add_editor,\
    set_bot_editor, set_bot_showon, set_bot_none,\
    set_sea_editor, set_sea_showon, set_sea_none,\
    set_tac_editor, set_tac_showon, set_tac_none
from restclients.trumba.calendar import get_campus_permissions
from restclients.trumba.exceptions import TrumbaException
from accountsynchr.log import log_exception
from accountsynchr.trumba.calendar_manager import CalendarManager


logger = logging.getLogger(__name__)


class PermissionManager:
    """
    Provides user account related methods
    """

    def __init__(self):
        self.cal_perm_dict = {}
        # {calendarid:
        #   {UwcalGroup.GTYEP_EDITOR: [trumba.Permission],
        #    UwcalGroup.GTYEP_SHOWON: [trumba.Permission]}}

    @staticmethod
    def add_account(name, uwnetid):
        """
        Add a new account in Trumba for the given user
        """
        try:
            return add_editor(name, uwnetid)
        except TrumbaException as ex:
            log_exception(logger,
                          "create account for %s" % uwnetid,
                          ex)
        return False

    def get_all_accounts(self):
        """
        :return a set of uwnetids
        """
        account_set = set()

        cal_m = CalendarManager()
        for campus_code in (TrumbaCalendar.SEA_CAMPUS_CODE,
                            TrumbaCalendar.BOT_CAMPUS_CODE,
                            TrumbaCalendar.TAC_CAMPUS_CODE):
            trumba_cal_list = cal_m.get_all_calendars(campus_code)
            if trumba_cal_list is None or len(trumba_cal_list) == 0:
                continue
            for trumba_cal in trumba_cal_list:
                if self.has_editor(trumba_cal):
                    for perm in self.get_editor_permissions(trumba_cal):
                        if perm.uwnetid not in account_set:
                            account_set.add(perm.uwnetid)
                if self.has_showon(trumba_cal):
                    for perm in self.get_showon_permissions(trumba_cal):
                        if perm.uwnetid not in account_set:
                            account_set.add(perm.uwnetid)
        return account_set

    def get_permissions(self, trumba_cal):
        """
        :return: a dict of {UwcalGroup.GTYEP_EDITOR: [trumba.Permission],
                            UwcalGroup.GTYEP_SHOWON: [trumba.Permission]}
                 for the given campus calendar.
        """
        return self._get_permissions(trumba_cal.calendarid,
                                     trumba_cal.campus)

    def _get_permissions(self, calendarid, campus_code):
        """
        loading the calendar edit and showon
        permissions into self.cal_perm_dict
        """
        if calendarid not in self.cal_perm_dict:
            perm_list = None
            try:
                perm_list = get_campus_permissions(calendarid, campus_code)
                self.cal_perm_dict[calendarid] =\
                    PermissionManager._load_perm_dict(perm_list)
            except TrumbaException as ex:
                log_exception(logger,
                              "get permissions on %d" % calendarid,
                              ex)
        return self.cal_perm_dict[calendarid]

    @staticmethod
    def _load_perm_dict(perm_list):
        """
        Process the edit and showon permission list and
        return a dict of {UwcalGroup.GTYEP_EDITOR: [trumba.Permission],
                          UwcalGroup.GTYEP_SHOWON: [trumba.Permission]}
        """
        edit_perm_list = []
        showon_perm_list = []
        perm_dict = {}
        perm_dict[UwcalGroup.GTYEP_EDITOR] = edit_perm_list
        perm_dict[UwcalGroup.GTYEP_SHOWON] = showon_perm_list
        if perm_list is not None:
            for perm in perm_list:
                if perm.is_edit():
                    edit_perm_list.append(perm)
                elif perm.is_showon():
                    showon_perm_list.append(perm)
        return perm_dict

    def get_editor_permissions(self, trumba_cal):
        """
        return [trumba.Permission]
        """
        return self.get_permissions(trumba_cal)[UwcalGroup.GTYEP_EDITOR]

    def get_showon_permissions(self, trumba_cal):
        """
        return [trumba.Permission]
        """
        return self.get_permissions(trumba_cal)[UwcalGroup.GTYEP_SHOWON]

    def exists(self, trumba_cal):
        """
        :return: True if exsits any permission users
        on the given campus calendar.
        """
        return self.has_editor(trumba_cal) or self.has_showon(trumba_cal)

    def has_editor(self, trumba_cal):
        """
        :return: True if exsits any editor account
        (publisher is treated as editor) on the given campus calendar.
        """
        return len(self.get_editor_permissions(trumba_cal)) > 0

    def has_showon(self, trumba_cal):
        """
        :return: True if exsits any showon account
        on the given campus calendar.
        """
        return len(self.get_showon_permissions(trumba_cal)) > 0

    def is_editor(self, trumba_cal, uwnetid):
        """
        :return: True if the uwnetid has an editor or a publisher
        permission on the given campus calendar.
        """
        if self.has_editor(trumba_cal):
            for perm in self.get_editor_permissions(trumba_cal):
                if perm.uwnetid == uwnetid:
                    return True
        return False

    def is_showon(self, trumba_cal, uwnetid):
        """
        :return: True if the uwnetid has showon permission
        on the given campus calendar.
        """
        if self.exists(trumba_cal):
            for perm in self.get_showon_permissions(trumba_cal):
                if perm.uwnetid == uwnetid:
                    return True
        return False

    def rm_permission(self, perm):
        """
        Remove the corresponding permission from Trumba event calendars
        upon the removal of group members
        """
        pass

    @staticmethod
    def set_editor_permission(trumba_cal, uwnetid):
        """
        :return: Ture if request is successful, False otherwise.
        """
        calendarid = trumba_cal.calendarid
        try:
            if trumba_cal.is_bot():
                return set_bot_editor(calendarid, uwnetid)
            elif trumba_cal.is_sea():
                return set_sea_editor(calendarid, uwnetid)
            else:
                return set_tac_editor(calendarid, uwnetid)
        except TrumbaException as ex:
            log_exception(logger,
                          "set editor permission for %s on %d" % (uwnetid,
                                                                  calendarid),
                          ex)
        return False

    @staticmethod
    def set_showon_permission(trumba_cal, uwnetid):
        """
        :return: Ture if request is successful, False otherwise.
        """
        calendarid = trumba_cal.calendarid
        try:
            if trumba_cal.is_bot():
                return set_bot_showon(calendarid, uwnetid)
            elif trumba_cal.is_sea():
                return set_sea_showon(calendarid, uwnetid)
            else:
                return set_tac_showon(calendarid, uwnetid)
        except TrumbaException as ex:
            log_exception(logger,
                          "set showon permission for %s on %d" % (uwnetid,
                                                                  calendarid),
                          ex)
        return False

    @staticmethod
    def remove_permission(trumba_cal, uwnetid):
        """
        :return: Ture if request is successful, False otherwise.
        """
        calendarid = trumba_cal.calendarid
        try:
            if trumba_cal.is_bot():
                return set_bot_none(calendarid, uwnetid)
            elif trumba_cal.is_sea():
                return set_sea_none(calendarid, uwnetid)
            else:
                return set_tac_none(calendarid, uwnetid)
        except TrumbaException as ex:
            log_exception(logger,
                          "remove permission for %s on %d" % (uwnetid,
                                                              calendarid),
                          ex)
        return False
