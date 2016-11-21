from django.core.management.base import BaseCommand, CommandError
from restclients.trumba.account import delete_editor


class Command(BaseCommand):
    help = "Close an account on Trumba."

    def add_arguments(self, parser):
        parser.add_argument('uwnetid')

    def handle(self, *args, **options):
        userid = options['uwnetid']
        print "Account.delete_editor(%s) ==> %s" % (
            userid, delete_editor(userid))
