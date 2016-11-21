from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.models.gws import GroupMember
from accountsynchr.ucalgroup.member_manager import MemberManager
from accountsynchr.test import GWS_DAO_CLASS


class TestMemberManager(TestCase):

    def test_normal_cases(self):
        with self.settings(RESTCLIENTS_GWS_DAO_CLASS=GWS_DAO_CLASS):
            mem_m = MemberManager()
            users = mem_m.get_campus_editors('bot')
            self.assertEqual(len(users), 0)
            users = mem_m.get_campus_editors('sea')
            self.assertEqual(len(users), 2)
            users = mem_m.get_campus_editors('tac')
            self.assertEqual(len(users), 0)

            users = mem_m.get_all_members()
            self.assertEqual(len(users), 2)
            self.assertTrue('user1' in users)
            self.assertTrue('user2' in users)

            groupid = 'u_eventcal_sea_1036368-editor'
            members = mem_m.get_members_by_groupid(groupid)

            self.assertEqual(len(members), 2)

            self.assertEqual(members[0].name, 'user1')
            self.assertTrue(members[0].is_uwnetid())

            self.assertEqual(members[1].name, 'user2')
            self.assertTrue(members[1].is_uwnetid())

            self.assertTrue(mem_m.is_member(groupid, 'user1'))
            self.assertTrue(mem_m.is_member(groupid, 'user2'))
            self.assertFalse(mem_m.is_member(groupid, 'user'))

    def test_get_members_none_cases(self):
        with self.settings(RESTCLIENTS_GWS_DAO_CLASS=GWS_DAO_CLASS):
            groupid = 'u_eventcal_sea_1019930-editor'
            members = MemberManager().get_members_by_groupid(groupid)
            self.assertIsNotNone(members)
            self.assertEqual(len(members), 0)
