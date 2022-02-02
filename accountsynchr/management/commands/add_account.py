# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from uw_trumba.account import add_editor


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
        print("Add account({0}, {1}) ==> {2}".format(
            name, userid, add_editor(name, userid)))
