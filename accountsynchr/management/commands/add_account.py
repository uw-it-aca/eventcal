from django.core.management.base import BaseCommand, CommandError
from accountsynchr.trumba.permission_manager import PermissionManager


class Command(BaseCommand):
    help = "Create a new account on Trumba."

    def add_arguments(self, parser):
        parser.add_argument('name')
        parser.add_argument('uwnetid')

    def handle(self, *args, **options):
        name = options['name']
        userid = options['uwnetid']

        print "PermissionManager().add_account(%s, %s) ==> %s" % (
            name, userid, PermissionManager().add_account(name, userid))
