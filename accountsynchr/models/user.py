# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import logging
from django.db import models
from django.db import transaction

logger = logging.getLogger(__name__)


class EditorCreation(models.Model):
    uwnetid = models.CharField(max_length=128, db_index=True, unique=True)
    last_updated = models.DateTimeField(auto_now=True)

    def to_json(self):
        return {'uwnetid': self.uwnetid,
                'last_updated': str(self.last_updated)}

    def __eq__(self, other):
        return (
            isinstance(other, EditorCreation) and
            self.uwnetid == other.uwnetid)

    def __hash__(self):
        return hash(self.uwnetid)

    def __lt__(self, other):
        if isinstance(other, EditorCreation):
            return self.uwnetid < other.uwnetid
        return NotImplemented

    def __str__(self):
        return json.dumps(self.to_json())

    @classmethod
    def exists(cls, uwnetid):
        return EditorCreation.objects.filter(uwnetid=uwnetid).exists()

    @classmethod
    def update(cls, uwnetid):
        with transaction.atomic():
            obj, created = EditorCreation.objects.update_or_create(
                uwnetid=uwnetid, defaults={"uwnetid": uwnetid},)
        if obj:
            logger.info(
                f"EditorCreation Set {obj.uwnetid} editor {obj.last_updated}")

    @classmethod
    @transaction.atomic
    def delete_old_records(cls, cutoff_dt):
        # Clean up all records that are older than the cutoff_dt
        EditorCreation.objects.filter(last_updated__lt=cutoff_dt).delete()

    @classmethod
    def get_editors(cls, cutoff_dt):
        logger.debug(f"get_editors {cutoff_dt}")
        editors = EditorCreation.objects.filter(last_updated__gte=cutoff_dt)
        editor_uwnetids = {editor.uwnetid for editor in editors}
        return editor_uwnetids

    class Meta:
        app_label = 'accountsynchr'
        db_table = "accountsynchr_editor_creation"
