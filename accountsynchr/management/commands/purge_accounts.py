# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import logging
import time
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
    def run_purge(self):
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
        sender = get_cronjob_sender()
        send_mail(
            "Purge Inactive User Accounts",
            message, sender, [sender])

    def handle(self, *args, **options):
        try:
            self.run_purge()
        except Exception as ex:
            logger.error(ex)
            time.sleep(60)
            try:
                self.run_purge()
            except Exception as ex1:
                logger.error(ex1)
                sender = get_cronjob_sender()
                send_mail(
                    "Purge Inactive User Account",
                    "{}".format(ex1), sender, [sender])
