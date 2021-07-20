# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from copy import deepcopy
import logging
from uw_trumba.models import TrumbaCalendar
from accountsynchr.gws_trumba import GwsToTrumba
from uw_trumba.account import delete_editor
from accountsynchr.dao.inactive_accounts import get_accounts_to_purge
from accountsynchr.dao.gws import Gws
from accountsynchr.dao.trumba import (
    CalPermManager, get_permission, remove_permission)

logger = logging.getLogger(__name__)


class AccountPurger(GwsToTrumba):
    def __init__(self):
        super(AccountPurger, self).__init__()
        self.gws = Gws()
        self.total_accounts_deleted = 0
        self.total_groups_purged = 0

    def set_accounts_to_purge(self):
        self.accounts_to_delete, self.netid_set = get_accounts_to_purge(
            self.gro_m.gws.all_editor_uwnetids, notify_inactive_users=True)
        logger.info("{} accounts will be purged".format(len(self.netid_set)))

    def sync(self):
        self.clean_editor_groups()
        self.clean_showon_groups()
        super().sync()
        self.clean_accounts_in_trumba()

    def clean_editor_groups(self):
        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            for group in self.gro_m.get_campus_editor_groups(campus_code):
                self.purge_group_member(group)

    def clean_showon_groups(self):
        for choice in TrumbaCalendar.CAMPUS_CHOICES:
            campus_code = choice[0]
            for group in self.gro_m.get_campus_showon_groups(campus_code):
                self.purge_group_member(group)

    def purge_group_member(self, group):
        members_to_del = self.get_members_to_delete(group.members)
        if len(members_to_del) > 0:
            group_name = group.group_ref.name
            try:
                self.gws.delete_members(group_name, members_to_del)
                self.total_groups_purged += 1
                logger.info("DELETED MEMBER {0} from {1}".format(
                        members_to_del, group_name))
            except Exception as ex:
                msg = "delete_members({}, {}) ==> {}".format(
                    group_name, members_to_del, ex)
                logger.error(msg)
                self.append_error(msg)

    def get_members_to_delete(self, group_members):
        members_to_del = []
        for gmember in deepcopy(group_members):
            if gmember.name in self.netid_set:
                members_to_del.append(gmember.name)
                group_members.remove(gmember)
        return members_to_del

    def clean_accounts_in_trumba(self):
        for acc in self.accounts_to_delete:
            try:
                if delete_editor(acc.uwnetid):
                    logger.info("CLOSED EDITOR: {}".format(acc))
                    self.total_accounts_deleted += 1
            except Exception as ex:
                msg = "close_editor({}) ==> {}".format(acc, ex)
                logger.error(msg)
                self.append_error(msg)
