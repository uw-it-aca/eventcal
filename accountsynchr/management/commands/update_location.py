# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import html
import logging
import os
import re
from urllib.parse import quote_plus
from django.core.management.base import BaseCommand
from accountsynchr.dao.campus_location import get_campus_locations_from_spacews

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "op", choices=["identify-location-renames", "make-import-csv"])

    def handle(self, *args, **options):
        self.op = options["op"]
        campus_locations = get_campus_locations_from_spacews()
        if campus_locations and len(campus_locations) > 0:
            logger.info(f"Found {len(campus_locations)} buildings")

            if self.op == "identify-location-renames":
                self.identify_location_renames(campus_locations)

            elif self.op == "make-import-csv":
                self.make_import_csv_file(campus_locations)

    def identify_location_renames(self, campus_locations):
        for bdg in campus_locations:
            if not bdg.space_obj:
                logger.info(
                    f"{bdg.old_name} ({bdg.old_code})  ==>  \n")
                continue
            if bdg.space_obj.name != bdg.old_name:
                logger.info(
                    f"{bdg.old_name} ({bdg.old_code})  ==>  " +
                    f"{bdg.space_obj.name} ({bdg.space_obj.code})\n"
                )

    def make_import_csv_file(self, campus_locations):
        try:
            with open(
                "./update_location_import.csv", "w", newline="",
                    encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["Campus location Name", "Map link", "Address"])
                for bdg in campus_locations:
                    if not bdg.space_obj:
                        continue
                    address = (
                        f"{bdg.space_obj.latitude},{bdg.space_obj.longitude}")
                    bname = html.escape(bdg.space_obj.name)
                    maplink = (
                        f"https://maps.google.com/maps?q=" +
                        f"{bdg.space_obj.latitude}," +
                        f"{bdg.space_obj.longitude}&t=k&z=18"
                    )
                    writer.writerow([
                        f"\"{bname} ({bdg.space_obj.code})\"",
                        f"\"{maplink}\"",
                        f"\"{address}\""
                        ])

        except Exception as ex:
            logger.error(ex)
