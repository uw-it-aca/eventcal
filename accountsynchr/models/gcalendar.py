# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import json
from django.db import models
from django.db import transaction
from django.utils import timezone


class GCalendar(models.Model):
    calendarid = models.PositiveIntegerField(db_index=True)
    campus = models.CharField(max_length=3)
    name = models.CharField(max_length=255, default=None)
    last_updated = models.DateTimeField(editable=True)

    def to_json(self):
        return {'calendarid': self.calendarid,
                'campus': self.campus,
                'name': self.name}

    def __eq__(self, other):
        return (
            isinstance(other, GCalendar) and
            self.calendarid == other.calendarid)

    def __hash__(self):
        return self.calendarid

    def __lt__(self, other):
        if isinstance(other, GCalendar):
            return (self.campus == other.campus and
                    self.name < other.name)
        return NotImplemented

    def __str__(self):
        return json.dumps(self.to_json())

    @classmethod
    def exists(cls, trumba_calendar):
        # uw_trumba.models.TrumbaCalendar
        return GCalendar.objects.filter(
            calendarid=trumba_calendar.calendarid,
            campus=trumba_calendar.campus).exists()

    @classmethod
    @transaction.atomic
    def create(cls, trumba_calendar):
        obj = GCalendar.objects.create(
            calendarid=trumba_calendar.calendarid,
            campus=trumba_calendar.campus,
            name=trumba_calendar.name,
            last_updated=timezone.now())
        return obj

    @classmethod
    @transaction.atomic
    def update(cls, trumba_calendar):
        obj = GCalendar.objects.select_for_update().get(
            calendarid=trumba_calendar.calendarid,
            campus=trumba_calendar.campus)
        obj.name = trumba_calendar.name
        obj.last_updated = timezone.now()
        obj.save()
        return obj

    class Meta:
        app_label = 'accountsynchr'
        db_table = "accountsynchr_gcalendar"
        unique_together = (("calendarid", "campus"),)
