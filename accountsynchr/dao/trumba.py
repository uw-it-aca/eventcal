import logging
from uw_trumba.account import (
    add_editor, set_perm_editor, set_perm_showon, set_perm_none)
from uw_trumba.calendars import Calendars
from uw_trumba.models import (
    is_editor, is_showon, new_edit_permission, new_showon_permission)

logger = logging.getLogger(__name__)


class CalPermManager(Calendars):
    # methods in super class
    # exists(campus_code)
    # get_calendar(campus, calendarid)
    # get_campus_calendars(campus_code)
    # has_calendar(campus, calendarid)
    # total_calendars(campus_code)

    def __init__(self):
        super(CalPermManager, self).__init__()
        # self.campus_calendars is a dict of
        # {campus-code: {calendar id: TrumbaCalendar}} preloaded

    def account_exists(self, uwnetid):
        return self.perm_loader.account_exists(uwnetid)

    def total_accounts(self):
        return self.perm_loader.total_accounts()

    def add_account(self, display_name, uwnetid):
        """
        Add a new account in Trumba for the given user
        :except: uw_trumba.exceptions.
        """
        if add_editor(display_name, uwnetid):
            self.perm_loader.add_account(uwnetid)
            return True


"""
Helper functions:
"""


def get_cal_permissions(trumba_cal):
    if len(trumba_cal.permissions) > 0:
        return sorted(trumba_cal.permissions.values())
    return []


def get_permission(trumba_cal, uwnetid):
    """
    :param trumba_cal: a valid TrumbaCalendar object
    returns a Permission object of the uwnetid
    """
    return trumba_cal.permissions.get(uwnetid)


def _has_editor_permission(trumba_cal, uwnetid):
    """
    :param trumba_cal: a valid TrumbaCalendar object
    :return: True if the uwnetid has an editor or higher level
    permission on the given calendar.
    """
    perm = get_permission(trumba_cal, uwnetid)
    return perm is not None and perm.in_editor_group()


def _has_showon_or_higher_permission(trumba_cal, uwnetid):
    """
    :param trumba_cal: a valid TrumbaCalendar object
    :return: True if the uwnetid has showon or higher level permission
    on the given trumba_cal.
    """
    perm = get_permission(trumba_cal, uwnetid)
    return perm is not None and perm.is_showon_or_higher()


def remove_permission(trumba_cal, uwnetid):
    """
    :return: Ture if request is successful.
    :except: uw_trumba.exceptions.*
    """
    if set_perm_none(trumba_cal, uwnetid):
        del trumba_cal.permissions[uwnetid]
        logger.info("Removed {0} permission of {1} from {2}".format(
            trumba_cal.campus, uwnetid, trumba_cal.name))
        return True


def set_editor_permission(trumba_cal, uwnetid):
    """
    :param trumba_cal: a valid TrumbaCalendar object
    :return: 1 if permission is set, 0 permission already exists,
    :except: uw_trumba.exceptions.*
    """
    if _has_editor_permission(trumba_cal, uwnetid):
        return 0
    if set_perm_editor(trumba_cal, uwnetid):
        _set_trumba_cal_editor(trumba_cal, uwnetid)
        logger.info("Set {0} editor permission for {1} on {2}".format(
            trumba_cal.campus, uwnetid, trumba_cal.name))
        return 1


def set_showon_permission(trumba_cal, uwnetid):
    """
    :param trumba_cal: a valid TrumbaCalendar object
    :return: 1 if permission is set, 0 permission already exists,
    :except: uw_trumba.exceptions.
    """
    if _has_showon_or_higher_permission(trumba_cal, uwnetid):
        return 0
    if set_perm_showon(trumba_cal, uwnetid):
        _set_trumba_cal_showon(trumba_cal, uwnetid)
        logger.info("Set {0} showon permission for {1} on {2}".format(
            trumba_cal.campus, uwnetid, trumba_cal.name))
        return 1


def _set_trumba_cal_editor(trumba_cal, uwnetid):
    perm = trumba_cal.permissions.get(uwnetid)
    if perm is not None and not perm.in_editor_group():
        perm.set_edit()
    else:
        trumba_cal.permissions[uwnetid] = new_edit_permission(uwnetid)


def _set_trumba_cal_showon(trumba_cal, uwnetid):
    perm = trumba_cal.permissions.get(uwnetid)
    if perm is not None and not perm.in_showon_group():
        perm.set_showon()
    else:
        trumba_cal.permissions[uwnetid] = new_showon_permission(uwnetid)
