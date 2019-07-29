import logging
from django.core.management.base import BaseCommand, CommandError
from uw_trumba.account import add_editor


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Create a new account on Trumba.
    """

    def add_arguments(self, parser):
        parser.add_argument('name')
        parser.add_argument('uwnetid')

    def handle(self, *args, **options):
        name = options['name']
        userid = options['uwnetid']

        logger.info("Add account({0}, {1}) ==> {2}".format(
            name, userid,  add_editor(name, userid)))
