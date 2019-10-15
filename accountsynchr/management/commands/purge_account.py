import logging
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.acc_purger import AccountPurger

logger = logging.getLogger("eventcal.commands")


class Command(BaseCommand):
    """
    Purge old accounts in Groups and Trumba.
    """

    def handle(self, *args, **options):

        gmp = GroupMemberPurger()
        gmp.sync()
        if gmp.has_err():
            logger.error(gmp.get_error_report())
        logger.info("Purged {} accounts.".format(gmp.total_accounts_deleted))
        logger.info("Purged {} groups.".format(gmp.total_groups_purged))
