# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import re
from django.core.management.base import BaseCommand
from accountsynchr.dao.campus_location import (
  FAC, DataFailureException)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "name", type=str, help="Location name (code)")

    def handle(self, *args, **options):
        name = options["name"]
        res = re.match(r"^(.*)\(([^()]+)\)\s*$", name)
        if not res:
            logger.error(f"Could not parse {name}\n")
            return
        name = res.group(1).rstrip()
        if res.group(2):
            code = res.group(2).strip()
        else:
            code = ""
        logger.info(f"name: {name}, code: {code}\n")
        fac_objs = []
        if code and len(code) > 1:
            try:
                fac_objs = FAC.search_by_code(code)
                for fac in fac_objs:
                    logger.info(f"{fac}\n")
                return
            except DataFailureException as ex:
                logger.error(f"search_by_code {code} {ex}\n")
        if name and len(name) > 1:
            try:
                fac_objs = FAC.search_by_name(name)
                for fac in fac_objs:
                    logger.info(f"{fac}\n")
                return
            except DataFailureException as ex:
                logger.error(f"search_by_name {name} {ex}\n")

            try:
                fac_objs = FAC.search_by_street(name)
                for fac in fac_objs:
                    logger.info(f"{fac}\n")
                return
            except DataFailureException as ex:
                logger.error(f"search_by_street {name} {ex}\n")
