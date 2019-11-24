"""
Send Trumba account removal email
Required settings:
    EMAIL_BACKEND
    EMAIL_HOST
    EMAIL_PORT
"""

import logging
from django.core.mail import send_mail


logger = logging.getLogger(__name__)
MESSAGE = (
    'Greetings!\n\n' +
    'You are receiving this message because you have an editor account ' +
    'in Trumba (campus event calendars) that has been inactive for ' +
    'over a year.\n\nYour account will be deleted on the first day of ' +
    'the next month. If you wish to remain an editor, simply log into ' +
    'trumba.uw.edu before then. Otherwise no action is needed.\n\n' +
    'Contact us at help@uw.edu if you have any questions.\n\n' +
    'Best,\nThe UW campus event calendars team'
    )
SENDER = 'uweventcalweb@uw.edu'
SUBJECT = 'Your Trumba Account Will Be Closed'


def send_acc_removal_email(uwnetid):
    recipient = "{}@uw.edu".format(uwnetid)
    try:
        send_mail(SUBJECT, MESSAGE, SENDER, [recipient], fail_silently=False)
        logger.info("Sent deletion notification to {}".format(recipient))
        return True
    except Exception as ex:
        logger.error("send_mail({}) ==> {}".format(recipient, str(ex)))
    return False
