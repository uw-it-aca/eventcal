# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.core.management.base import BaseCommand
from accountsynchr.dao.campus_location import get_campus_locations_from_spacews

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "name", type=str, help="Location name (code)")

    def handle(self, *args, **options):
        self.name = options["name"]
        campus_locations = get_campus_locations_from_spacews()
        if campus_locations and len(campus_locations) > 0:
            logger.info(f"Found {len(campus_locations)} records")
            for bdg in campus_locations:
                logger.info(f"{bdg.space_obj}\n")
