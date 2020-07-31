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
        if send_acc_removal_email(userid):
            print("Purge Notification email sent to {}@uw.edu".format(userid))
