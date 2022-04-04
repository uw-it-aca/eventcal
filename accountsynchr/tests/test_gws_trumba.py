# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from accountsynchr.gws_trumba import GwsToTrumba
from accountsynchr.tests import fdao_gws_override


@fdao_gws_override
class TestTrumbaToGws(TestCase):

    def test_group_manager(self):
        g_t = GwsToTrumba()
        g_t.sync()
        self.assertEqual(g_t.new_acounts, 2)
        self.assertEqual(g_t.new_editor_perm_counts, 2)
        self.assertEqual(g_t.new_showon_perm_counts, 1)
        self.assertTrue(g_t.has_err())
