# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import html
import logging
import os
import re
from restclients_core.exceptions import DataFailureException
from uw_space import Facilities

logger = logging.getLogger(__name__)
FAC = Facilities()


class CampusLocation:
    def __init__(self, old_name, old_code, space_obj):
        self.old_name = old_name
        self.old_code = old_code
        self.space_obj = space_obj


def get_campus_locations_from_spacews():
    """
    Return a list of CampusLocation objects
    """
    campus_locations = []
    data_file = os.path.join(
        os.path.join(os.path.dirname(__file__), "../", "data"),
        "campus_map_buildings.csv")
    with open(data_file, "r", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=",")

        next(reader)  # skip header
        for line in reader:
            try:
                res = re.match(r"^(.*)\(([^()]+)\)\s*$", line[0])
                if not res:
                    logger.error(f"Could not parse {line}")
                    continue
                name = html.unescape(res.group(1).rstrip())
                if res.group(2):
                    code = res.group(2).strip()
                else:
                    code = ""
                logger.debug(f"name: {name}, code: {code}\n")

                fac_objs = []
                if code and len(code):
                    try:
                        fac_objs = FAC.search_by_code(code)
                    except DataFailureException as ex:
                        logger.error(f"{ex} with {code}")
                if not fac_objs or len(fac_objs) == 0:
                    try:
                        fac_objs = FAC.search_by_name(name)
                    except DataFailureException as ex:
                        logger.error(f"{ex} with {name}")
                if not fac_objs or len(fac_objs) == 0:
                    try:
                        fac_objs = FAC.search_by_street(name)
                    except DataFailureException as ex:
                        logger.error(f"{ex} with {name}")

                campus_locations.append(
                    CampusLocation(
                        name, code,
                        fac_objs[0] if fac_objs and len(fac_objs) else None
                        )
                    )
            except Exception as ex:
                logger.error(f"{ex} with {line}")
    return campus_locations
