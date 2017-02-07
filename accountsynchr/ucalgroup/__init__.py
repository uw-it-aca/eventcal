"""
The core interface with GWS restclient.
"""

from django.conf import settings
import logging
import re
import traceback
from restclients.gws import GWS
from restclients.exceptions import DataFailureException
from restclients.models.gws import Group, GroupReference, GroupUser
from restclients.models.trumba import TrumbaCalendar, UwcalGroup,\
    is_valid_campus_code
from accountsynchr.log import log_resp_time, log_exception, Timer


logger = logging.getLogger(__name__)
gws = GWS()


def get_campus_groups(campus_code):
    """
    :return: a dictionary object of {group-name, UwcalGroup}
    of the given campus
    """
    if is_valid_campus_code(campus_code):
        return _load_dict(
            _search_groups('u_eventcal_%s' % campus_code))
    else:
        logger.warn(
            "Calling get_campus_groups with invalid campus code: %s"
            % campus_code)
        return None


def _search_groups(gr_stem):
    """
    :param gr_stem: a string of format: u_eventcal_{bot,sea,tac}
    :return: a list of GroupReference objects
    Search GWS with the given gr_stem
    """
    action = 'search groups with stem=%s' % gr_stem
    timer = Timer()
    try:
        return gws.search_groups(stem=gr_stem)
    finally:
        log_resp_time(logger,
                      action,
                      timer)


def _load_dict(group_refs):
    """
    :param group_refs: an array of GroupReference objects
    :return: a dictionary object of {group-name, UwcalGroup}
    """
    uwcalgroup_dict = {}
    if group_refs is None or len(group_refs) == 0:
        return uwcalgroup_dict
    for gr in group_refs:
        if re.match(r'^u_eventcal_[a-z]{3}$', gr.name):
            # skip parent group
            continue
        calgr = _convert_to_uwcalgroup(gr)
        if calgr is not None:
            uwcalgroup_dict[calgr.name] = calgr
    return uwcalgroup_dict


def _convert_to_uwcalgroup(gr):
    cal = TrumbaCalendar()
    if re.match(r'^u_eventcal_[a-z]{3}_[1-9]\d*-editor$', gr.name):
        gtype = UwcalGroup.GTYEP_EDITOR
        cal.name = re.sub(r'^(.+) calendar editor group$', r'\1', gr.title)
    elif re.match(r'^u_eventcal_[a-z]{3}_[1-9]\d*-showon$', gr.name):
        gtype = UwcalGroup.GTYEP_SHOWON
        cal.name = re.sub(r'^(.+) calendar showon group$', r'\1', gr.title)
    else:
        logger.warn("Skip it due to invalid group name: %s" % gr)
        return None
    cal.calendarid = int(
        re.sub(r'^u_eventcal_[a-z]{3}_([1-9]\d*)-[a-z]+$', r'\1', gr.name))
    cal.campus = re.sub(r'^u_eventcal_([a-z]{3})_.+$', r'\1', gr.name)

    calgr = UwcalGroup(calendar=cal,
                       gtype=gtype,
                       uwregid=gr.uwregid,
                       name=gr.name,
                       title=gr.title,
                       description=gr.description)
    return calgr


def del_group(uwcalgroup):
    """
    :param uwcalgroup: an UwcalGroup object
    :return: True if successful
    Remove the UW Event Calendar group from GWS
    """
    action = 'delete group %s' % uwcalgroup
    timer = Timer()
    try:
        return gws.delete_group(group.uwregid)
    finally:
        log_resp_time(logger,
                      action,
                      timer)


def get_members(group_id):
    """
    Get effective members of the speficied group
    :param group_id: the name or uwregid of the uw group
    :return: a list of restclients.GroupMember object;
    [] if the group has no members
    """
    action = 'get effective members of %s' % group_id
    timer = Timer()
    try:
        return gws.get_effective_members(group_id)
    except DataFailureException as ex:
        if ex.status == 404:
            return None
    finally:
        log_resp_time(logger,
                      action,
                      timer)


def get_group(group_id):
    """
    :param group_id: the name or uwregid of the uw group
    :return: the Group object
    """
    action = 'get group %s' % group_id
    timer = Timer()
    try:
        return gws.get_group_by_id(group_id)
    except DataFailureException as ex:
        if ex.status == 404:
            return None
    finally:
        log_resp_time(logger,
                      action,
                      timer)


def put_group(uwcalgroup):
    """
    :param uwcalgroup: an UwcalGroup object
    :return: the Group object
    Create or update the UW Group
    """
    gwsgroup = _convert_to_group(uwcalgroup)
    action = 'create/update group %s' % gwsgroup
    timer = Timer()
    try:
        if gwsgroup.has_regid():
            return gws.update_group(gwsgroup)
        else:
            return gws.create_group(gwsgroup)
    finally:
        log_resp_time(logger,
                      action,
                      timer)


def _convert_to_group(uwcalgroup):
    """
    :param uwcalgroup: an UwcalGroup object
    :return: a gws.Group object
    Convert/map the given UwcalGroup object into a Group object
    """
    group = Group(uwregid=uwcalgroup.uwregid,
                  name=uwcalgroup.name,
                  title=uwcalgroup.title,
                  description=uwcalgroup.description)
    group.admins.append(GroupUser(name=UwcalGroup.ADMIN_GROUP_NAME,
                                  user_type=GroupUser.GROUP_TYPE))
    if uwcalgroup.is_editor_group():
        updater_gname = group.name
    else:
        updater_gname = re.sub('-showon', '-editor', group.name)
    group.updaters.append(GroupUser(name=updater_gname,
                                    user_type=GroupUser.GROUP_TYPE))
    group.readers.append(GroupUser(name='dc=all',
                                   user_type=GroupUser.NONE_TYPE))
    group.optouts.append(GroupUser(name='dc=all',
                                   user_type=GroupUser.NONE_TYPE))
    return group


def update_members(group_id, members):
    """
    :param group_id: the name or uwregid of the uw group
    :param members: an array of GroupMember objects
    :return: a list of members not found.
    Updates the membership of the group with the given groupid
    """
    action = 'update members of %s' % group_id
    timer = Timer()
    try:
        rejected_users = gws.update_members(group_id, members)
        if rejected_users is not None and len(rejected_users) > 0:
            logger.warn(
                "GWS Rejected %s member: %s" % (group_id, rejected_users))
        return rejected_users
    finally:
        log_resp_time(logger,
                      action,
                      timer)
