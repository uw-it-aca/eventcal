from restclients.util.log import log_info, log_err


def log_resp_time(logger, action_desc, timer):
    log_info(logger, action_desc + ' fulfilled', timer)


def log_exception(logger, action, exception_info):
    """
    :param action: the action that caused the exception
    :param exception_info: a string containing the full stack trace,
                           the exception type and value
    """
    logger.error("%s =exception=> %s ",
                 action,
                 exception_info)
    # exception_info.splitlines())
    # exc_info.splitlines()[-3:])
    # print the last function call, exception type and value
