# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta
from django.utils import timezone
import time
from django.test import TransactionTestCase
from accountsynchr.models import EditorCreation


class TestEditorCreation(TransactionTestCase):

    def test_custom_methods(self):
        EditorCreation.update('a')
        time.sleep(5)
        EditorCreation.update('b')
        EditorCreation.update('c')
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

    def test_comparison_operators(self):
        obj = EditorCreation.objects.create(uwnetid='a')
        o_json = obj.to_json()
        self.assertEqual(o_json['uwnetid'], 'a')
        self.assertIsNotNone(str(obj))

        obj1 = EditorCreation.objects.create(uwnetid='b')
        self.assertFalse(obj == obj1)
        self.assertFalse(obj.__eq__(None))
        self.assertTrue(obj < obj1)
        res = obj1.__lt__(None)
        self.assertEqual(res, NotImplemented)

        obj2 = EditorCreation.objects.create(uwnetid='a1')
        obj2.save()
        self.assertFalse(obj1 < obj2)
        self.assertEqual(hash(obj2), hash('a1'))
