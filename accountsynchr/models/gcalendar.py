# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import json
from django.db import models
from django.db import transaction
from django.utils import timezone
from uw_trumba.models import TrumbaCalendar


class GCalendar(models.Model):
    calendar_id = models.PositiveIntegerField(db_index=True)
    campus = models.CharField(max_length=3)
    name = models.CharField(max_length=255, default=None)
    last_updated = models.DateTimeField(editable=True)

    def to_json(self):
        return {'calendarid': self.calendarid,
                'campus': self.campus,
                'name': self.name}

    def __eq__(self, other):
        return self.calendarid == other.calendarid

    def __hash__(self):
        return super().__hash__()

    def __lt__(self, other):
        return (self.campus == other.campus and
                self.name < other.name)

    def __str__(self):
        return json.dumps(self.to_json())

    @classmethod
    def exists(cls, trumba_calendar):
        return GCalendar.objects.filter(
            calendar_id=trumba_calendar.calendar_id).filter(
            campus=trumba_calendar.campus).exists()

    @classmethod
    @transaction.atomic
    def update(cls, trumba_calendar):
        obj = GCalendar.objects.select_for_update().get(
            calendar_id=trumba_calendar.calendarid,
            campus=trumba_calendar.campus)
        obj.calendar_id = trumba_calendar.calendarid
        obj.campus = trumba_calendar.campus
        obj.last_updated = timezone.now()
        obj.save()
        return obj

    class Meta:
        app_label = 'accountsynchr'
        db_table = "accountsynchr_gcalendar"
        unique_together = (("calendar_id", "campus"),)
