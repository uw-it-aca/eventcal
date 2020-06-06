import logging
from django.core.mail import send_mail
from accountsynchr.util.settings import (
    get_email_address_domain, get_email_sender, get_email_message,
    get_email_subject)

logger = logging.getLogger(__name__)


def send_acc_removal_email(uwnetid):
    """
    Send Trumba account removal email
    Required settings:
      EMAIL_BACKEND
      EMAIL_HOST
      EMAIL_PORT
      EMAIL_ADDRESS_DOMAIN
      EMAIL_SENDER
      PURGE_EMAIL_MESSAGE
      PURGE_EMAIL_SUBJECT
    """

    email_address_domain = get_email_address_domain()
    recipient = "{}{}".format(uwnetid, email_address_domain)
    try:
        send_mail(get_email_subject(), get_email_message(),
                  get_email_sender(), [recipient], fail_silently=False)
        logger.info("Sent deletion notification to {}".format(recipient))
        return True
    except Exception as ex:
        logger.error("send_mail({}) ==> {}".format(recipient, ex))
    return False
