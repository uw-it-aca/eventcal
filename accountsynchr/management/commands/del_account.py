import logging
from django.core.management.base import BaseCommand, CommandError
from uw_trumba.account import delete_editor


class Command(BaseCommand):
    """
    Close an account on Trumba.
    """

    def add_arguments(self, parser):
        parser.add_argument('uwnetid')

    def handle(self, *args, **options):
        userid = options['uwnetid']
        print("Delete account({0}) ==> {1}".format(
            userid, delete_editor(userid)))
