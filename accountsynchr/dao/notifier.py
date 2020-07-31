import logging
from django.core.mail import send_mail
from accountsynchr.util.settings import (
    get_email_address_domain, get_user_email_sender, get_next_purge_date)

logger = logging.getLogger(__name__)
RM_MSG_BODY = (
        'Greetings!\n\nYou are receiving this message because you have '
        'an editor account in Trumba (campus event calendars) that has '
        'been inactive for over a year. Upon the recommendation of the '
        'vendor, we will regularly close unused editor accounts.\n\n'
        'Your account is scheduled to be deleted on {}. If you wish to '
        'remain an editor, simply log into http://trumba.uw.edu/ with '
        'your UW NetID before then. Otherwise no action is needed.\n\n'
        'Contact us at help@uw.edu if you have any questions.\n\nBest,\n'
        'The UW campus event calendars team\n')


def send_acc_removal_email(uwnetid):
    """
    Send Trumba account removal email
    Required settings:
      EMAIL_BACKEND
      EMAIL_HOST
      EMAIL_PORT
      EMAIL_ADDRESS_DOMAIN
      EMAIL_SENDER
      PURGE_DATE
    """
    sender = get_user_email_sender()
    recipient = "{}{}".format(uwnetid, get_email_address_domain())
    try:
        send_mail('Your Trumba Account Will Be Closed',
                  RM_MSG_BODY.format(get_next_purge_date()),
                  sender, [recipient], fail_silently=False)
        logger.info("Sent deletion notification to {}".format(recipient))
        return True
    except Exception as ex:
        logger.error("send_mail({}) ==> {}".format(recipient, ex))
    return False
