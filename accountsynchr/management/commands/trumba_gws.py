import logging
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.gws_trumba import GwsToTrumba
from accountsynchr.trumba_gws import TrumbaToGws

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Sync Trumba calendars to UW groups and members.
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        synchr = TrumbaToGws()
        synchr.sync()
        if synchr.has_err():
            err = synchr.get_error_report()
            sender = "{}@uw.edu".format(get_cronjob_sender())
            logger.error(err)
            send_mail("Sync Trumba calendars to UW groups and members",
                      err, sender, [sender])
