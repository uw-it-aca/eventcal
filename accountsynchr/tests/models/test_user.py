# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta
from django.utils import timezone
import time
from django.test import TransactionTestCase
from accountsynchr.models import EditorCreation


class TestEditorCreation(TransactionTestCase):

    def test_get_editors(self):
        EditorCreation.update('a')
        time.sleep(5)
        EditorCreation.update('b')
        EditorCreation.update('c')
        obj = EditorCreation.objects.get(uwnetid='a')
        self.assertIsNotNone(str(obj))
        records = EditorCreation.objects.all()
        self.assertEqual(len(records), 3)
        cutoff = timezone.now() - timedelta(seconds=3)
        recent_users = EditorCreation.get_editors(cutoff)
        self.assertEqual(len(recent_users), 2)
        self.assertTrue('c' in recent_users)
        self.assertTrue('b' in recent_users)
        self.assertTrue(EditorCreation.exists('a'))
        EditorCreation.delete_old_records(cutoff)
        self.assertFalse(EditorCreation.exists('s'))
