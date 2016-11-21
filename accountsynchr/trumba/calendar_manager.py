import logging
from restclients.models.trumba import TrumbaCalendar
import restclients.trumba.calendar as Calendar


logger = logging.getLogger(__name__)


class CalendarManager:
    """
    The CalendarManager class
    """

    def __init__(self):
        self.tcal_dict = {}
        # a dict of {campus-code: a dict of {calendar id: TrumbaCalendar}}
        # preload Seattle calendars
        self.tcal_dict[TrumbaCalendar.SEA_CAMPUS_CODE] =\
            Calendar.get_campus_calendars(TrumbaCalendar.SEA_CAMPUS_CODE)

    def _get_dict(self, campus_code):
        """
        :return: a dictionary of {calenderid, TrumbaCalendar}
                 corresponding to the given campus.
                 None if error, {} if not exists
        """
        if campus_code not in self.tcal_dict:
            self.tcal_dict[campus_code] = self._rm_duplicates(
                Calendar.get_campus_calendars(campus_code))
        return self.tcal_dict[campus_code]

    def _rm_duplicates(self, calendar_dict):
        """
        Remove those calendars shared with Bothell or Tacoma from Seattle
        """
        sea_cal_ids = self.get_calendarids(TrumbaCalendar.SEA_CAMPUS_CODE)
        for cal_id in calendar_dict.keys():
            if cal_id in sea_cal_ids:
                logger.info("Rm shared sea cal %s" % calendar_dict[cal_id])
                del calendar_dict[cal_id]
        return calendar_dict

    def exists(self, campus_code):
        """
        :return: true if the campus has some calendars
        """
        cald = self._get_dict(campus_code)
        return cald is not None and len(cald) > 0

    def get_all_calendars(self, campus_code):
        """
        :return: a list of TrumbaCalendar objects of the given campus
                 sorted by calendar names
        """
        if self.exists(campus_code):
            return sorted(self._get_dict(campus_code).values())
        return None

    def get_calendar(self, campus_code, calendarid):
        """
        :return: the TrumbaCalendar object of the given calendarid.
                 None if not exists
        """
        return self._get_dict(campus_code).get(calendarid)

    def get_calendarids(self, campus_code):
        """
        :return: the list of calendarids of the given campus
        """
        if self.exists(campus_code):
            return self._get_dict(campus_code).keys()
        return None

    def has_calendar(self, campus_code, calendarid):
        """
        :return: True if there is a TrumbaCalendar with the same calendarid
        """
        return self.exists(campus_code) and\
            calendarid in self.get_calendarids(campus_code)

    def len(self, campus_code):
        """
        :return: Total number of Trumba Calendars of the given campus
        """
        if self.exists(campus_code):
            return len(self._get_dict(campus_code))
        return 0
