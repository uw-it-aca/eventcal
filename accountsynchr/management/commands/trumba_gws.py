import logging
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.trumba_gws import TrumbaToGws
from accountsynchr.util.settings import get_cronjob_sender

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Sync Trumba calendars to UW groups and members.
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        sender = get_cronjob_sender()
        try:
            synchr = TrumbaToGws()
            synchr.sync()
            if synchr.has_err():
                err = synchr.get_error_report()
                logger.error(err)
                send_mail(
                    "Sync Trumba calendars to UW groups and members",
                    err, sender, [sender])
        except Exception as ex:
            logger.error(ex)
            send_mail("Sync Trumba calendars to UW groups and members",
                      "{}".format(ex), sender, [sender])
