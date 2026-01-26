# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import logging
from django.core.management.base import BaseCommand
from accountsynchr.dao.campus_location import (
  get_campus_locations_from_spacews, tidy_name)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Process Trumba campus locations, perform one of the following:
    1) Identify location differences by comparing with SpaceWS data
    2) Create an import file with data from SpaceWS
    """

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
            new_name = tidy_name(bdg.space_obj.name)
            if new_name != bdg.old_name:
                logger.info(
                    f"{bdg.old_name} ({bdg.old_code})  ==>  " +
                    f"{new_name} ({bdg.space_obj.code})\n"
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
                    if (not bdg.space_obj or
                            bdg.space_obj.latitude == 0.0 or
                            bdg.space_obj.longitude == 0.0):
                        continue

                    new_name = tidy_name(bdg.space_obj.name)
                    if new_name != bdg.old_name:
                        logger.warning(
                            f"{bdg.old_name} ({bdg.old_code})  ==>  "
                            + f"{new_name} ({bdg.space_obj.code})\n"
                        )
                    maplink = (
                        f"https://maps.google.com/maps?q=" +
                        f"{bdg.space_obj.latitude}," +
                        f"{bdg.space_obj.longitude}&t=k&z=18"
                    )
                    address = (
                        f"{bdg.space_obj.latitude},{bdg.space_obj.longitude}"
                    )
                    writer.writerow([
                        f"{bdg.old_name} ({bdg.space_obj.code})",
                        maplink,
                        address
                    ])

        except Exception as ex:
            logger.error(ex)
