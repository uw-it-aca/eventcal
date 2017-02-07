import logging
import time


def log_resp_time(logger, message, timer):
    logger.info("%s Time=%f sec", message, timer.get_elapsed())


def log_exception(logger, message, exception_info):
    """
    :param message: the message that caused the exception
    :param exception_info: a string containing the exception type and value
    """
    logger.error("%s =except=> %s ", message, exception_info)


class Timer:
    def __init__(self):
        """
        Start the timer
        """
        self.start = time.time()

    def get_elapsed(self):
        """
        Return the time spent in seconds
        """
        return time.time() - self.start
