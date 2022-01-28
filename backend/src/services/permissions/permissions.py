from datetime import datetime, timedelta, timezone

import src.config as config
from functools import wraps
from flask import jsonify
from src.services.helper_functions import query, response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, unset_jwt_cookies, get_jwt, create_access_token, \
    set_access_cookies


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

def check_permissions(rule, *parameters):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception as e:
                resp = jsonify({'logout': True})
                unset_jwt_cookies(resp)
                return resp, 401
            access_status = query("SELECT access_status FROM users WHERE userid = %(user_id)s",
                                     {'user_id': get_jwt_identity()})[0]
            if access_status['access_status'] == 1:
                user_perm = \
                    query("SELECT roles.* FROM users JOIN roles ON users.roleid = roles.roleid WHERE userid = %(user_id)s",
                          {'user_id': get_jwt_identity()})[0]
                compare = parameters if len(parameters) > 0 else kwargs
                if rule(user_perm, *[kwargs[v] for v in compare]) or config.DEBUG_MODE:
                    return fn(*args, **kwargs)

            return response("TIP: De politie hacken is een slecht idee!", 403)

        return decorator

    return wrapper


def check_jwt():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not config.DEBUG_MODE:
                verify_jwt_in_request()
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def user_owns_project(resource_id):
    return len(query("SELECT userid FROM users_have_projects WHERE userid = %(userid)s AND projectid = %(projectid)s",
                       {'userid': get_jwt_identity(), 'projectid': resource_id})) > 0


def user_owns_announcement_associated_project(announcement_id):
    announcement = query("SELECT projectid FROM announcements WHERE announcementid = %(announcementid)s",
                         {'announcementid': announcement_id})[0]['projectid']
    if announcement is None:
        return True
    return user_owns_project(announcement)


def user_owns_announcement(announcement_id):
    return len(
        query("SELECT userid FROM announcements WHERE userid = %(userid)s AND announcementid = %(announcementid)s",
              {'userid': get_jwt_identity(), 'announcementid': announcement_id})) > 0


def user_owns_reply(reply_id):
    return len(
        query("SELECT userid FROM announcements WHERE userid = %(userid)s AND replyid = %(replyid)s",
              {'userid': get_jwt_identity(), 'replyid': reply_id})) > 0


def user_owns_account(user_id):
    return user_id == str(get_jwt_identity())


def get_user_projects(user_id):
    return [int(x['projectid']) for x in
            query("SELECT * FROM users_have_projects WHERE userid = %(userid)s", {'userid': user_id})]


def user_owns_associated_user_project(user_id):
    other_user_projects = get_user_projects(user_id)
    current_user_projects = get_user_projects(get_jwt_identity())
    for project in other_user_projects:
        if project in current_user_projects:
            return True
    return False
