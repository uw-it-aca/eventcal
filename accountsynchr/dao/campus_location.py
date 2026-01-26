# Copyright 2026 UW-IT, University of Washington
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


class CampusLocation(object):
    def __init__(self, old_name, old_code):
        self.old_name = old_name
        self.old_code = old_code
        self.space_obj = self.find_space_obj()

    def find_space_obj(self):
        logger.debug(
            f"name: {self.old_name}, code: {self.old_code}\n")

        if self.old_code and len(self.old_code) > 1:
            try:
                fac_objs = FAC.search_by_code(self.old_code)
                if fac_objs and len(fac_objs) == 1:
                    return fac_objs[0]
                    # facility codes are unique,
                    # either find a match or no match
            except DataFailureException as ex:
                logger.error(
                    f"search_by_code {self.old_code} {ex}\n")

        if self.old_name and len(self.old_name) > 1:
            try:
                fac_objs = FAC.search_by_name(self.old_name)
                if fac_objs:
                    if len(fac_objs) == 1:
                        return fac_objs[0]
                    if len(fac_objs) > 1:
                        logger.error(
                            f"search_by_name {self.old_name} " +
                            f"found {len(fac_objs)} matches, skip!"
                        )
                        return None
            except DataFailureException as ex:
                logger.error(f"search_by_name {self.old_name} {ex}\n")

            try:
                fac_objs = FAC.search_by_street(self.old_name)
                if fac_objs:
                    if len(fac_objs) == 1:
                        return fac_objs[0]
                    if len(fac_objs) > 1:
                        logger.error(
                            f"search_by_street {self.old_name} " +
                            f"found {len(fac_objs)} matches, skip!"
                        )
                        return None
            except DataFailureException as ex:
                logger.error(f"search_by_street {self.old_name} {ex}\n")
        return None


def get_campus_locations_from_spacews():
    """
    Process Trumba location data from campus_location_export.csv
    Return a list of CampusLocation objects
    """
    campus_locations = []
    data_file = os.path.join(
        os.path.join(os.path.dirname(__file__), "../", "data"),
        "campus_location_export.csv",
    )
    with open(data_file, "r", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)  # skip header
        for line in reader:
            try:
                name, code = parse_campus_location_title(line[0])
                if len(code) > 1:
                    campus_locations.append(
                        CampusLocation(name, code)
                        )
            except Exception as ex:
                logger.error(f"{ex} with {line}\n")
    return campus_locations


def parse_campus_location_title(title_str):
    """
    Parse campus location title from Trumba
    :param title_str: original title string
    :return: tuple of (name, code)
    """
    name = html.unescape(title_str.strip())
    code = ""
    if "(" in title_str and ")" in title_str:
        res = re.match(r"^(.*)\(([A-Za-z0-9]+)\)\s*$", title_str)
        # UW Facility code has no spaces, hyphens, or special symbols
        if not res:
            logger.error(f"Could not parse {title_str}, skip!\n")
        else:
            name = html.unescape(res.group(1).rstrip())
            if res.group(2):
                code = res.group(2).strip()
    return name, code


def tidy_name(name):
    """
    Remove trailing (** ... **) from name in SpaceWS
    :param name: original name
    :return: cleaned name
    """
    if not name:
        return name
    return re.sub(r"\s*\(\*\*.*?\*\*\)", "", name)
