# import src.config as config
from functools import wraps

from flask import jsonify

from .helper_functions import *
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, unset_jwt_cookies


# ###### HOW TO CHECK ######
# ####### 1 RESOURCE #######
# # if !user_has_permission(userid, "READ", "project", projectid):
# #   abort(403, "Access Forbidden")
# # return query("SQL")
# ###### HOW TO CHECK ######
# ### MULTIPLE RESOURCES ###
# # data = query("SQL")
# # for project in data:
# #   if !user_has_permission(userid, "READ", "project", project["projectid"]):
# #       remove project (with iteration?)
# # if data.length = 0:
# #   abort(403, "Access Forbidden")
# # return data
# ###### HOW TO CHECK ######
# ######## FOR FILE ########
# # use projectid as resource_id!!!
#
from src import config


def any_permission(*permissions):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if any(permissions) or config.UI_ENABLED:
                return fn(*args, **kwargs)
            else:
                return response("No permission", 403)
        return decorator
    return wrapper


def all_permission(*permissions):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if all(permissions) or config.UI_ENABLED:
                return fn(*args, **kwargs)
            else:
                return response("No permission", 403)
        return decorator
    return wrapper


def remove_jwt_if_expired():
    try:
        verify_jwt_in_request()
    except Exception as e:
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp, 401


class PermissionsBase:
    def __init__(self):
        remove_jwt_if_expired()
        self.identity = get_jwt_identity()
        self.permissions = \
        query("SELECT roles.* FROM users JOIN roles ON users.roleid = roles.roleid WHERE userid = %(user_id)s",
              {'user_id': self.identity})[0]

    def user_owns_project(self, resource_id):
        return len(
            query("SELECT userid FROM users_have_projects WHERE userid = %(userid)s AND projectid = %(projectid)s",
                  {'userid': self.identity, 'projectid': resource_id})) > 0


class Projects(PermissionsBase):
    def __init__(self):
        PermissionsBase.__init__(self)

    def may_read_all(self):
        return self.permissions["may_read_any_project"]
    def may_read(self, resource_id):
        return self.may_read_all() or (self.permissions["may_read_own_project"] and self.user_owns_project(resource_id))
    def may_create(self):
        return self.permissions["may_create_project"]
    def may_update(self, resource_id):
        return self.permissions["may_update_any_project"] or (
                    self.permissions["may_update_own_project"] and self.user_owns_project(resource_id))
    def may_archive(self):
        return self.permissions["may_archive_any_project"]
    def may_delete(self):
        return self.permissions["may_delete_any_project"]

    def may_read_files(self, project_id):
        return self.user_owns_project(project_id) or self.permissions["may_read_any_project"]
    def may_cud_files(self, project_id):
        return self.permissions["may_update_any_file"] or \
               self.permissions["may_update_file_in_own_project"] and self.user_owns_project(project_id)


class Announcements(PermissionsBase):
    def __init__(self):
        PermissionsBase.__init__(self)

    def user_owns_associated_project(self, announcement_id):
        return self.user_owns_project(query("SELECT projectid FROM announcements announcementid = %(announcementid)s",
                                            {'announcementid': announcement_id})[0]['projectid'])
    def user_owns_announcement(self, announcement_id):
        return len(
            query("SELECT userid FROM announcements WHERE userid = %(userid)s AND announcementid = %(announcementid)s",
                  {'userid': self.identity, 'announcementid': announcement_id})) > 0
    def user_owns_reply(self, reply_id):
        return len(
            query("SELECT userid FROM announcements WHERE userid = %(userid)s AND replyid = %(replyid)s",
                  {'userid': self.identity, 'replyid': reply_id})) > 0
    def may_read(self, announcement_id):
        print(announcement_id)
        return self.permissions['may_read_any_project'] or self.user_owns_associated_project(announcement_id)
    def may_read_all_from_project(self, project_id):
        self.user_owns_project(project_id)
    def may_create(self, project_id):
        return self.permissions["may_create_announcement_anywhere"] or (self.permissions[
            "may_create_announcement_in_own_project"] and self.user_owns_project(project_id))
    def may_update_delete(self, announcement_id):
        return self.permissions["may_update_any_announcement"] or \
               self.permissions["may_update_own_content"] and self.user_owns_announcement(announcement_id)
    def may_add_reply(self, announcement_id):
        return self.permissions['may_create_reply_anywhere'] or (self.permissions['may_create_reply_in_own_project'] and self.user_owns_associated_project(announcement_id))
    def may_read_reply(self, announcement_id):
        return self.permissions['may_read_any_project'] or self.user_owns_associated_project(announcement_id)
    def may_update_delete_reply(self, reply_id):
        return self.permissions["may_update_any_announcement"] or (
               self.permissions["may_update_own_content"] and self.user_owns_reply(reply_id))


class Users(PermissionsBase):
    def __init__(self):
        PermissionsBase.__init__(self)

    def user_owns_itself(self, user_id):
        return user_id == get_jwt_identity()
    def get_user_projects(self, user_id):
        return [int(x['projectid']) for x in
                query("SELECT * FROM users_have_projects WHERE userid = %(userid)s", {'userid': user_id})]
    def user_owns_associated_project(self, user_id):
        other_user_projects = self.get_user_projects(user_id)
        current_user_projects = self.get_user_projects(get_jwt_identity())
        for project in other_user_projects:
            if project in current_user_projects:
                return True
        return False
    def may_read(self, user_id):
        return self.permissions["may_read_any_user"] or \
               self.user_owns_itself(user_id) or \
               (self.permissions["may_read_user_in_own_project"] and
                self.user_owns_associated_project(user_id))
    def may_read_all(self):
        return self.permissions["may_read_any_user"]
    def may_create(self):
        return self.permissions["may_create_user"]
    def may_update(self, user_id):
        return self.permissions["may_update_any_user"] or \
               (self.permissions["may_update_own_account"] and self.user_owns_itself(user_id))
    def may_update_password(self, user_id):
        return self.permissions["may_update_any_password"] or \
               (self.permissions["may_update_own_password"] and self.user_owns_project(user_id))
    def may_update_role(self):
        return self.permissions["may_update_any_user_role"]
    def may_update_role_protected(self):
        return self.permissions["may_elevate_to_protected_role"]
    def may_delete_user(self, user_id):
        return self.permissions["may_delete_any_user"] and not self.user_owns_itself(user_id)


class Roles(PermissionsBase):
    def __init__(self):
        PermissionsBase.__init__(self)

    def check_role_permissions(self):
        return self.permissions["may_crud_roles"]
