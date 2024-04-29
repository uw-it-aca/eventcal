# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import logging
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from accountsynchr.trumba_gws_lite import TrumbaGwsLite
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
            synchr = TrumbaGwsLite()
            synchr.sync()
            if synchr.has_err():
                err = synchr.get_error_report()
                logger.error(err)
                send_mail(
                    "Sync Trumba calendars to UW groups",
                    err, sender, [sender])
        except Exception as ex:
            logger.error(ex)
            raise CommandError(ex)
