import logging
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.gws_trumba import GwsToTrumba
from accountsynchr.util.settings import get_cronjob_sender

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Sync UW group members to Trumba user and permissions.
    """
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        sender = get_cronjob_sender()
        try:
            synchr = GwsToTrumba()
            synchr.sync()
            if synchr.has_err():
                err = synchr.get_error_report()
                logger.error(err)
                send_mail(
                    "Sync UW Group members to Trumba user and permissions",
                    err, sender, [sender])
        except Exception as ex:
            logger.error(ex)
            send_mail("Sync UW Group members to Trumba user and permissions",
                      "{}".format(ex), sender, [sender])
