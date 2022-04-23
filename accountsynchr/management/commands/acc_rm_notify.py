# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand, CommandError
from accountsynchr.dao.notifier import send_acc_removal_email


class Command(BaseCommand):
    """
    Notify the given user for account colosing
    """

    def add_arguments(self, parser):
        parser.add_argument('uwnetid')

    def handle(self, *args, **options):
        userid = options['uwnetid']
        print("Purge Notification email sent to {} ==> {}".format(
                userid, send_acc_removal_email(userid)))
