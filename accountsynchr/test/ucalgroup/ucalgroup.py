from django.test import TestCase
from django.conf import settings
from restclients.models.gws import GroupUser, Group, GroupReference
from restclients.models.trumba import UwcalGroup, TrumbaCalendar
from restclients.exceptions import DataFailureException
from accountsynchr.ucalgroup import get_group, _convert_to_uwcalgroup,\
    _convert_to_group
from accountsynchr.test import GWS_DAO_CLASS


class TestUcalGroup(TestCase):

    def test_get_group(self):
        with self.settings(RESTCLIENTS_GWS_DAO_CLASS=GWS_DAO_CLASS):
            group = get_group('u_eventcal_sea_1013649-editor')

            self.assertEquals(group.name, "u_eventcal_sea_1013649-editor")
            self.assertEquals(group.uwregid,
                              "143bc3d173d244f6a2c3ced159ba9c97")
            self.assertEquals(group.title,
                              ("College of Arts and Sciences calendar " +
                               "editor group"))
            self.assertEquals(group.description,
                              ("Specifying the editors who are able to " +
                               "add/edit/delete any event on the " +
                               "corresponding Seattle Trumba calendar"))

            self.assertIsNotNone(group.admins)
            self.assertEquals(len(group.admins), 1)
            self.assertEquals(group.admins[0].user_type, GroupUser.GROUP_TYPE)
            self.assertEquals(group.admins[0].name, "u_eventcal_support")

            self.assertIsNotNone(group.updaters)
            self.assertEquals(len(group.updaters), 1)
            self.assertEquals(group.updaters[0].user_type,
                              GroupUser.GROUP_TYPE)
            self.assertEquals(group.updaters[0].name,
                              "u_eventcal_sea_1013649-editor")

            self.assertIsNotNone(group.readers)
            self.assertEquals(len(group.readers), 1)
            self.assertEquals(group.readers[0].user_type, GroupUser.NONE_TYPE)
            self.assertEquals(group.readers[0].name, "dc=all")

            self.assertIsNotNone(group.optouts)
            self.assertEquals(len(group.optouts), 1)
            self.assertEquals(group.optouts[0].user_type, GroupUser.NONE_TYPE)
            self.assertEquals(group.optouts[0].name, "dc=all")

    def test_get_group_error(self):
        with self.settings(RESTCLIENTS_GWS_DAO_CLASS=GWS_DAO_CLASS):
            group = get_group('u_eventcal_sea_1036795-showon')
            self.assertIsNone(group)

    def test_convert_to_uwcalgroup(self):
        gr = GroupReference(
            uwregid='772287deb68449ac813d5307c7bc168e',
            name='u_eventcal_sea_448712-editor',
            title='Department of Chemistry >> Chemistry Sandbox',
            description=None)
        uwcalgroup = _convert_to_uwcalgroup(gr)
        self.assertIsNotNone(uwcalgroup)
        self.assertEquals(uwcalgroup.uwregid,
                          '772287deb68449ac813d5307c7bc168e')
        self.assertEquals(uwcalgroup.name,
                          'u_eventcal_sea_448712-editor')
        self.assertEquals(uwcalgroup.title,
                          'Department of Chemistry >> Chemistry Sandbox')
        self.assertTrue(uwcalgroup.is_editor_group())

    def test_convert_to_group(self):
        gr = UwcalGroup(
            calendar=TrumbaCalendar(name='Chemistry Sandbox',
                                    calendarid=448712,
                                    campus='sea'),
            uwregid='772287deb68449ac813d5307c7bc168e',
            name='u_eventcal_sea_448712-editor',
            title='Department of Chemistry >> Chemistry Sandbox',
            description=('Specifying the editors who are able to ' +
                         'add/edit/delete any event on the corresponding ' +
                         'Trumba calendar'))
        group = _convert_to_group(gr)
        self.assertIsNotNone(group)
        self.assertEquals(group.uwregid,
                          '772287deb68449ac813d5307c7bc168e')
        self.assertEquals(group.name,
                          'u_eventcal_sea_448712-editor')
        self.assertEquals(group.title,
                          'Department of Chemistry >> Chemistry Sandbox')
        self.assertEquals(group.description,
                          ('Specifying the editors who are able to ' +
                           'add/edit/delete any event on the ' +
                           'corresponding Trumba calendar'))
        self.assertEquals(len(group.admins), 1)
        self.assertEquals(group.admins[0].name, UwcalGroup.ADMIN_GROUP_NAME)
        self.assertEquals(group.admins[0].user_type, GroupUser.GROUP_TYPE)
        self.assertEquals(len(group.updaters), 1)
        self.assertEquals(group.updaters[0].name,
                          'u_eventcal_sea_448712-editor')
        self.assertEquals(group.updaters[0].user_type, GroupUser.GROUP_TYPE)
        self.assertEquals(len(group.readers), 1)
        self.assertEquals(group.readers[0].name, 'dc=all')
        self.assertEquals(group.readers[0].user_type, GroupUser.NONE_TYPE)
        self.assertEquals(len(group.optouts), 1)
        self.assertEquals(group.optouts[0].name, 'dc=all')
        self.assertEquals(group.optouts[0].user_type, GroupUser.NONE_TYPE)
