# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import json
import re
from restclients_core import models
from uw_trumba.models import (
    TrumbaCalendar, is_editor, is_showon, EDITOR, SHOWON)
from accountsynchr.models.gcalendar import GCalendar


class UwcalGroup(models.Model):

    GTYEP_CHOICES = (
        (EDITOR, 'Editor'),
        (SHOWON, 'Showon'),
        )
    calendar = models.ForeignKey(TrumbaCalendar)
    gtype = models.CharField(max_length=6, choices=GTYEP_CHOICES)

    def get_calendarid(self):
        return self.calendar.calendarid

    def get_campus_code(self):
        return self.calendar.campus

    def has_group_ref(self):
        return self.group_ref is not None

    def get_regid(self):
        if self.has_group_ref():
            return self.group_ref.uwregid
        return None

    def get_group_id(self):
        if self.has_group_ref():
            return self.group_ref.name
        return self.get_group_name()

    def get_group_admin(self):
        return self.calendar.get_group_admin()

    def get_group_desc(self):
        return self.calendar.get_group_desc(self.gtype)

    def get_group_name(self):
        return self.calendar.get_group_name(self.gtype)

    def get_group_title(self):
        return self.calendar.get_group_title(self.gtype)

    def get_member_manager(self):
        return self.calendar.get_group_name(EDITOR)

    def is_editor_group(self):
        return is_editor(self.gtype)

    def is_showon_group(self):
        return is_showon(self.gtype)

    def same_name(self, calendar):
        if self.group_ref is not None:
            group_name = self.group_ref.display_name
            return (
                group_name == calendar.name or
                group_name == calendar.get_group_title(self.gtype))
        return False

    def set_calendar_name(self, cal_name):
        self.calendar.name = cal_name

    def to_json(self):
        group_ref_data = None
        if self.group_ref is not None:
            group_ref_data = {
                "id": self.group_ref.name,
                "regid": self.group_ref.uwregid,
                "displayName": self.group_ref.display_name}
        return {
            'calendar': self.calendar.to_json(),
            'gtype': self.gtype,
            'group_ref': group_ref_data,
            'members': [m.json_data() for m in self.members]}

    def __eq__(self, other):
        try:
            return (
                self.calendar == other.calendar and
                self.gtype == other.gtype and
                self.group_ref == other.group_ref)
        except Exception:
            return False

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        super(UwcalGroup, self).__init__(*args, **kwargs)
        # self.group_ref is a GroupReference or Group object
        self.members = []  # a list of uw_gws.GroupMember


def new_editor_group(trumba_cal, group_ref=None):
    return UwcalGroup(calendar=trumba_cal, gtype=EDITOR, group_ref=group_ref)


def new_showon_group(trumba_cal, group_ref=None):
    return UwcalGroup(calendar=trumba_cal, gtype=SHOWON, group_ref=group_ref)


def get_cal_name(display_name):
    return re.sub(r'^(.+) calendar (editor|showon) group$', r'\1',
                  display_name)


class UserAccount(models.Model):
    uwnetid = models.CharField(max_length=128)
    display_name = models.CharField(max_length=96, null=True, default=None)
    last_visit = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(null=True, default=None)

    def to_json(self):
        return {
            "uwnetid": self.uwnetid,
            "display_name": self.display_name,
            "last_visit": date_to_str(self.last_visit),
            "created_at": date_to_str(self.created_at)}

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        super(UserAccount, self).__init__(*args, **kwargs)

    def __hash__(self):
        return super().__hash__()


def date_to_str(dt):
    return str(dt) if dt is not None else None
