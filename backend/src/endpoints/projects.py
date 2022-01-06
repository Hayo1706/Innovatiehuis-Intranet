import src.config as config
import connexion
from ..services.helper_functions import *
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..services.permissions import Projects
from ..services.permissions.permissions import check_permissions


@check_permissions(Projects.may_read)
def read_one(project_id):
    is_int(project_id)
    return query(
        "SELECT projectid, project_name, description, is_archived, created, last_updated "
        "FROM projects WHERE projectid = %(id)s",
        {'id': project_id})


@check_permissions(Projects.may_read_all)
def read_all():
    # TODO: user_has_permission(get_jwt_identity(), "READ", "project")
    return query("SELECT projectid, project_name, description, is_archived, created, last_updated FROM projects")


def create():
    # project_name, description, [userids]
    # 1 add projects row
    # 2 add users_have_projects rows for every userid
    return


# projectid, project_name, description, is_archived, [userids], [parentids], [childids]
def update(project_id, is_archived):
    is_int(project_id)
    is_boolean(is_archived)
    query_update("UPDATE projects SET is_archived =%(is_archived)s where projectid=%(id)s",
                 {'id': id, 'is_archived': str(int(is_archived))})
    return response(f"Project {project_id} successfully updated", 200)


# 1 get all userids for project
# 2 cross-check with supplied userids
# 3 add row if in 2 but not 1
# 4 remove row if in 1 but not 2
# 5 do the same for parents!!!
# 6 do the same for children!!!
# 7 set new values for project

def delete(project_id):
    is_int(project_id)
    query_update("DELETE FROM projects WHERE projectid =%(id)s", {'id': id})
    return response(f"Project {project_id} successfully deleted", 200)


# projects/{id}/users
def read_users(project_id):
    return


def add_user(project_id, user_id):
    return


def remove_user(project_id, user_id):
    return


# projects/{id}/parents

def read_parents(project_id):
    # returns array of id/name combinations
    is_int(project_id)
    return query(
        "SELECT projects.projectid, projects.project_name, projects.description, projects.is_archived, projects.created, projects.last_updated"
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.parentid = projects.projectid "
        "WHERE childid = %(id)s",
        {'id': project_id})


def add_parent(project_id, parent_id):
    is_int(project_id)
    is_int(parent_id)
    query_update(
        "INSERT INTO projects_have_parents (childid, parentid) VALUES (%(id)s, %(parentid)s)",
        {'id': project_id, 'parentid': parent_id})


def remove_parent(project_id, parent_id):
    is_int(project_id)
    is_int(parent_id)
    query_update(
        "INSERT INTO projects_have_parents (childid, parentid) VALUES (%(id)s, %(parentid)s)",
        {'id': project_id, 'parentid': parent_id})  # TODO: FIX


# projects/{id}/children
def read_children(project_id):  # returns array of id/name/shared_files combinations
    is_int(project_id)
    return query(
        "SELECT projects.projectid, projects.project_name, projects.description, projects.is_archived, projects.created, projects.last_updated"
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.childid = projects.projectid "
        "WHERE parentid = %(id)s",
        {'id': project_id})


def add_child(project_id, child_id):
    return


def update_shared_files(project_id, child_id):
    # 1 get all child ids
    # 2 cross-check with update ids
    # 3 add row if in 2 but not 1
    # 4 remove row if in 1 but not 2
    # shared_files from body

    is_int(project_id)
    is_int(child_id)
    query_update(
        "SELECT projects.projectid, projects.project_name, projects.description, projects.is_archived, projects.created, projects.last_updated"
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.parentid = projects.projectid "
        "WHERE childid = %(id)s",
        {'id': project_id})


def remove_child(project_id, child_id):
    return


# projects/{id}/announcements
def read_announcements(project_id):
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid = %(id)s "
        "ORDER BY announcements.timestamp DESC", {'id': project_id})


def read_announcements_recent(project_id):
    cutoff_date = config.CUTOFF_DATE
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid = %(id)s AND announcements.timestamp > %(cutoff_date)s "
        "ORDER BY announcements.timestamp DESC", {'id': project_id, 'cutoffdate': cutoff_date})


@jwt_required()
def add_announcement(project_id):
    is_int(project_id)
    try:
        body = connexion.request.json['announcement']
        title = body['title']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)

    query_update(
        "INSERT INTO announcements (userid, projectid, title, content) VALUES (%(userid)s, %(id)s, %(title)s, "
        "%(content)s)",
        {'userid': get_jwt_identity(), 'id': project_id, 'content': content, 'title': title})
    return response(f"Announcement in project {project_id} successfully posted", 200)
