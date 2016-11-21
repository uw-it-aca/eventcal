from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from accountsynchr.trumba.calendar_manager import CalendarManager
from accountsynchr.test import BOT_DAO_CLASS, SEA_DAO_CLASS, TAC_DAO_CLASS


class TestCalendarManager(TestCase):

    def test_exists(self):
        with self.settings(RESTCLIENTS_TRUMBA_BOT_DAO_CLASS=BOT_DAO_CLASS,
                           RESTCLIENTS_TRUMBA_SEA_DAO_CLASS=SEA_DAO_CLASS,
                           RESTCLIENTS_TRUMBA_TAC_DAO_CLASS=TAC_DAO_CLASS):

            cal_m = CalendarManager()
            self.assertTrue(cal_m.exists('bot'))
            self.assertTrue(cal_m.exists('sea'))
            self.assertTrue(cal_m.exists('tac'))

            sea_cal_list = cal_m.get_all_calendars('sea')
            self.assertEqual(len(sea_cal_list), 10)

            bot_cal_list = cal_m.get_all_calendars('bot')
            self.assertEqual(len(bot_cal_list), 4)

            tac_cal_list = cal_m.get_all_calendars('tac')
            self.assertEqual(len(tac_cal_list), 1)
