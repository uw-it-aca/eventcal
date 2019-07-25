from django.test import TestCase
from uw_gws.models import GroupReference
from uw_trumba.models import TrumbaCalendar
from uw_trumba.exceptions import AccountNameEmpty, AccountNotExist
from accountsynchr.dao import DataFailureException
from accountsynchr.dao.trumba import (
    CalPermManager, remove_permission, set_editor_permission,
    set_showon_permission, _has_editor_permission,
    _has_showon_or_higher_permission, get_cal_permissions,
    get_permission, _set_trumba_cal_editor, _set_trumba_cal_showon)


class TestCalPermManager(TestCase):

    def test_cal_perm_manager(self):
        cal_per_m = CalPermManager()
        self.assertTrue(cal_per_m.exists('bot'))
        self.assertTrue(cal_per_m.exists('sea'))
        self.assertTrue(cal_per_m.exists('tac'))
        self.assertEqual(cal_per_m.total_calendars('bot'), 3)
        self.assertEqual(cal_per_m.total_calendars('sea'), 2)
        self.assertEqual(cal_per_m.total_calendars('tac'), 1)

        self.assertEqual(cal_per_m.total_accounts(), 6)
        self.assertTrue(cal_per_m.account_exists('dummyp'))
        self.assertTrue(cal_per_m.account_exists('dummye'))
        self.assertTrue(cal_per_m.account_exists('dummys'))
        self.assertTrue(cal_per_m.account_exists("tdummyp"))
        self.assertTrue(cal_per_m.account_exists("tdummye"))
        self.assertTrue(cal_per_m.account_exists("tdummys"))

        sea_cal = cal_per_m.get_calendar('sea', 1)
        perms = get_cal_permissions(sea_cal)
        self.assertEqual(len(perms), 3)
        self.assertEqual(perms[0].to_json(),
                         {'display_name': 'publisher',
                          'level': 'PUBLISH',
                          'uwnetid': 'dummyp'})
        self.assertEqual(perms[1].to_json(),
                         {'display_name': 'editor',
                          'level': 'EDIT',
                          'uwnetid': 'dummye'})
        self.assertEqual(perms[2].to_json(),
                         {'display_name': 'showon',
                          'level': 'SHOWON',
                          'uwnetid': 'dummys'})

        self.assertTrue(_has_editor_permission(sea_cal, 'dummyp'))
        self.assertTrue(_has_editor_permission(sea_cal, 'dummye'))
        self.assertFalse(_has_editor_permission(sea_cal, 'dummys'))

        self.assertTrue(_has_showon_or_higher_permission(
                sea_cal, 'dummys'))
        self.assertTrue(_has_showon_or_higher_permission(
                sea_cal, 'dummyp'))
        self.assertTrue(_has_showon_or_higher_permission(
                sea_cal, 'dummye'))

        self.assertFalse(_has_showon_or_higher_permission(
                sea_cal, 'dummy'))

        not_exsit_cal = TrumbaCalendar(calendarid=101,
                                       campus='sea',
                                       name='Not exsit')
        self.assertIsNone(get_permission(not_exsit_cal, 'dummyp'))
        self.assertEqual(len(get_cal_permissions(not_exsit_cal)), 0)

    def test_set_permissions(self):
        cal_per_m = CalPermManager()

        self.assertTrue(cal_per_m.add_account('sdummye', 'sdummye'))
        self.assertRaises(AccountNameEmpty, cal_per_m.add_account, '', '')

        sea_cal = cal_per_m.get_calendar('sea', 1)
        self.assertEqual(set_editor_permission(sea_cal, 'dummye'), 0)
        # _set_trumba_cal_showon case.1
        _set_trumba_cal_showon(sea_cal, 'dummye')
        perm = get_permission(sea_cal, 'dummye')
        self.assertTrue(perm.in_showon_group())

        self.assertFalse(_has_editor_permission(sea_cal, 'sdummye'))
        self.assertEqual(set_editor_permission(sea_cal, 'sdummye'), 1)
        self.assertTrue(_has_editor_permission(sea_cal, 'sdummye'))
        self.assertTrue(_has_showon_or_higher_permission(sea_cal, 'sdummye'))

        self.assertEqual(set_showon_permission(sea_cal, 'sdummye'), 0)
        self.assertFalse(_has_showon_or_higher_permission(sea_cal, 'sdummys'))
        self.assertEqual(set_showon_permission(sea_cal, 'sdummys'), 1)
        self.assertTrue(_has_showon_or_higher_permission(sea_cal, 'sdummys'))

        # _set_trumba_cal_editor case.1
        _set_trumba_cal_editor(sea_cal, 'sdummys')
        self.assertTrue(_has_editor_permission(sea_cal, 'sdummys'))

        self.assertRaises(AccountNotExist,
                          set_editor_permission,
                          sea_cal, 'none')
        self.assertRaises(AccountNotExist,
                          set_showon_permission,
                          sea_cal, 'none')
        self.assertRaises(DataFailureException,
                          set_editor_permission,
                          sea_cal, 'u404')

        self.assertTrue(_has_editor_permission(sea_cal, 'dummyp'))
        self.assertTrue(remove_permission(sea_cal, 'dummyp'))
        self.assertFalse(_has_editor_permission(sea_cal, 'dummyp'))

        self.assertTrue(_has_showon_or_higher_permission(sea_cal, 'dummys'))
        self.assertTrue(remove_permission(sea_cal, 'dummys'))
        self.assertFalse(_has_showon_or_higher_permission(sea_cal, 'dummys'))

        self.assertRaises(AccountNotExist,
                          remove_permission,
                          sea_cal, 'none')
        self.assertRaises(DataFailureException, remove_permission,
                          sea_cal, 'u404')

        bot_cal = cal_per_m.get_calendar('bot', 2)

        self.assertEqual(set_editor_permission(bot_cal, 'test10'), 1)
        self.assertTrue(_has_editor_permission(bot_cal, 'test10'))

        self.assertEqual(set_showon_permission(bot_cal, 'test10'), 0)
        self.assertTrue(_has_editor_permission(bot_cal, 'test10'))
        self.assertTrue(remove_permission(bot_cal, 'test10'))

        self.assertTrue(set_showon_permission(bot_cal, 'test11'))

        tac_cal = cal_per_m.get_calendar('tac', 3)
        self.assertTrue(remove_permission(tac_cal, 'tdummyp'))
