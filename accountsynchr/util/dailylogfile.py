from logging import FileHandler as BaseFileHandler
from datetime import date


class DailyLogFileHandler(BaseFileHandler):
    """
    A custom handler that always writes to a log file
    with the current date in the file name.
    """
    def __init__(self, filename, *args, **kwargs):
        datedfilename = "%s.%s" % (
            filename, str(date.today()))
        BaseFileHandler.__init__(self, datedfilename)
