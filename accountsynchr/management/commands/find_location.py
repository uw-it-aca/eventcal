# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.core.management.base import BaseCommand
from accountsynchr.dao.campus_location import (
    CampusLocation,
    parse_campus_location_title
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Look up a campus location by name or address (facility code)
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "location", type=str,
            help="Location name or address (facility code)")

    def handle(self, *args, **options):
        location = options["location"]
        name, code = parse_campus_location_title(location)
        fac = CampusLocation(name, code).space_obj
        if fac:
            logger.info(f"Found: {fac}\n")
        else:
            logger.info("No matching location found.\n")
