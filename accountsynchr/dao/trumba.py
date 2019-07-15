from uw_trumba.account import (
    add_editor, set_perm_editor, set_perm_showon, set_perm_none)
from uw_trumba.calendars import Calendars
from uw_trumba.models import is_editor, is_showon, new_edit_permission


class CalPermManager(Calendars):

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
        """
        if add_editor(display_name, uwnetid):
            self.perm_loader.add_account(uwnetid)
            return True
        return False

    def _get_perm_dict(self, calendar):
        """
        returns a dict of {uwnetid: Permission} of the calendar
        """
        cal = self.get_calendar(calendar.campus, calendar.calendarid)
        if cal is not None:
            return cal.permissions
        return None

    def get_permission(self, calendar, uwnetid):
        """
        returns a Permission object of the uwnetid
        """
        perm_dict = self._get_perm_dict(calendar)
        if perm_dict is not None:
            return perm_dict.get(uwnetid)
        return None

    def get_permissions(self, calendar):
        """
        returns a list of the Permission objects of the calendar
        """
        perm_dict = self._get_perm_dict(calendar)
        if perm_dict is not None:
            return sorted(perm_dict.values())
        return []

    def has_editor_permission(self, calendar, uwnetid):
        """
        :return: True if the uwnetid has an editor or higher level
        permission on the given calendar.
        """
        perm = self.get_permission(calendar, uwnetid)
        return perm is not None and perm.in_editor_group()

    def has_showon_or_higher_permission(self, calendar, uwnetid):
        """
        :return: True if the uwnetid has showon or higher level permission
        on the given calendar.
        """
        perm = self.get_permission(calendar, uwnetid)
        return perm is not None and perm.is_showon_or_higher()

    def set_editor_permission(self, calendar, uwnetid):
        """
        :return: Ture if request is successful, False otherwise.
        """
        if not self.has_editor_permission(calendar, uwnetid):
            if set_perm_editor(calendar, uwnetid):
                self._add_editor_perm(calendar, uwnetid)
                return True
        return False

    def set_showon_permission(self, calendar, uwnetid):
        """
        :return: Ture if request is successful, False otherwise.
        """
        if not self.has_showon_or_higher_permission(calendar, uwnetid):
            return set_perm_showon(calendar, uwnetid)
        return False

    def _add_editor_perm(self, calendar, uwnetid):
        perm_dict = self._get_perm_dict(calendar)
        perm = perm_dict.get(uwnetid)
        if perm is not None and not perm.in_editor_group():
            perm.set_editor()
        else:
            perm_dict[uwnetid] = new_edit_permission(uwnetid)


def remove_permission(calendar, uwnetid):
    """
    :return: Ture if request is successful, False otherwise.
    """
    return set_perm_none(calendar, uwnetid)
