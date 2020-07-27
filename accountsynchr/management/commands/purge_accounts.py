import logging
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.gws_trumba import GwsToTrumba
from accountsynchr.user_purger import AccountPurger
from accountsynchr.util.settings import get_cronjob_sender

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Purge inactive user accounts from Groups and Trumba.
    """

    def handle(self, *args, **options):
        msgs = []
        purger = AccountPurger()
        purger.set_accounts_to_purge()
        msgs.append("Accounts closed in this run:")
        for acc in purger.accounts_to_delete:
            msgs.append("{},{}".format(acc.uwnetid, acc.last_visit))

        purger.sync()
        msgs.append("Total accounts purged: {}".format(
                purger.total_accounts_deleted))
        msgs.append("Total groups updated: {}".format(
                purger.total_groups_purged))

        if purger.has_err():
            err = purger.get_error_report()
            msgs.append(err)
            logger.error(err)

        message = "\n".join(msgs)
        sender = "{}@uw.edu".format(get_cronjob_sender())
        send_mail("Purge Inactive User Accounts", message, sender, [sender])
