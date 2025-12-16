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

    def handle(self, *args, **options):
        campus_locations = get_campus_locations_from_spacews()
        if campus_locations and len(campus_locations) > 0:
            logger.info(f"Found {len(campus_locations)} buildings")
            try:
                with open(
                    "./upd_buildings.csv", "w", newline="", encoding="utf-8"
                ) as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        ["OLD Campus location Name", "Campus location Name"])
                        # "Map link", "Address"])
                    for bdg in campus_locations:
                        #bname = html.escape(bdg.name)
                        writer.writerow([
                            f"{bdg.old_name} ({bdg.old_code})",
                            f"{bdg.space_obj.name} ({bdg.space_obj.code})"
                            # (f"\"https://maps.google.com/maps?q={bname}@" +
                            #    f"{bdg.latitude},{bdg.longitude}&t=k&z=18\""),
                            # f"\"{bdg.latitude},{bdg.longitude}\""
                        ])
            except Exception as ex:
                logger.error(ex)
