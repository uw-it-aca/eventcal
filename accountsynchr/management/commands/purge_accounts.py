import logging
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.user_purger import AccountPurger

logger = logging.getLogger("eventcal.commands")


class Command(BaseCommand):
    """
    Purge old accounts in Groups and Trumba.
    """

    def handle(self, *args, **options):

        p = AccountPurger()
        p.set_accounts_to_purge()
        logger.info("Accounts will be closed in this run:")
        for acc in p.accounts_to_delete:
            logger.info("{},{}".format(acc.uwnetid, acc.last_visit))

        p.sync()
        logger.info("Total accounts purged: {}".format(
                p.total_accounts_deleted))
        logger.info("Total groups updated: {}".format(p.total_groups_purged))
        if p.has_err():
            logger.error(p.get_error_report())
