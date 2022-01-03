import src.config as config
import connexion
from ..services.helper_functions import *
from ..services.permissions import *
from flask_jwt_extended import get_jwt_identity


def read_all():

    user_has_permission(get_jwt_identity(), "READ", "project")
    return query("SELECT projectid, project_name, description, is_archived, created, last_updated FROM projects")


def read_one(id):
    is_int(id)
    return query(
        "SELECT projectid, project_name, description, is_archived, created, last_updated "
        "FROM projects WHERE projectid = %(id)s",
        {'id': id})


def update(id, is_archived):
    is_int(id)
    is_boolean(is_archived)
    query_update("UPDATE projects SET is_archived =%(is_archived)s where projectid=%(id)s",
                 {'id': id, 'is_archived': str(int(is_archived))})
    return response("{id} successfully updated".format(id=str(id)), 200)


def delete(id):
    is_int(id)
    query_update("DELETE FROM projects WHERE projectid =%(id)s", {'id': id})
    return response("{id} successfully deleted".format(id=str(id)), 200)


def read_parents(id):
    is_int(id)
    return query(
        "SELECT projects.projectid, projects.project_name, projects.description, projects.is_archived, projects.created, projects.last_updated"
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.parentid = projects.projectid "
        "WHERE childid = %(id)s",
        {'id': id})


def create_parent(id, parentid):
    is_int(id)
    is_int(parentid)
    query_update(
        "SELECT projects.projectid, projects.project_name, projects.description, projects.is_archived, projects.created, projects.last_updated"
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.parentid = projects.projectid "
        "WHERE childid = %(id)s",
        {'id': id})


def update_child_files(id, parentid, shared_files):
    is_int(id)
    is_int(parentid)
    query_update(
        "SELECT projects.projectid, projects.project_name, projects.description, projects.is_archived, projects.created, projects.last_updated"
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.parentid = projects.projectid "
        "WHERE childid = %(id)s",
        {'id': id})


def delete_parent(id, parentid):
    is_int(id)
    is_int(parentid)
    query_update(
        "SELECT projects.projectid, projects.project_name, projects.description, projects.is_archived, projects.created, projects.last_updated"
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.parentid = projects.projectid "
        "WHERE childid = %(id)s",
        {'id': id})


def read_children(id):
    is_int(id)
    return query(
        "SELECT projects.projectid, projects.project_name, projects.description, projects.is_archived, projects.created, projects.last_updated"
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.childid = projects.projectid "
        "WHERE parentid = %(id)s",
        {'id': id})


def read_announcements(id):
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid = %(id)s "
        "ORDER BY announcements.timestamp DESC", {'id': id})


def read_announcements_recent(id):
    cutoff_date = config.CUTOFF_DATE
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid = %(id)s AND announcements.timestamp > %(cutoff_date)s "
        "ORDER BY announcements.timestamp DESC", {'id': id, 'cutoffdate': cutoff_date})


def add_announcement(id):
    is_int(id)
    try:
        body = connexion.request.json['announcement']
        title = body['title']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)

    query_update(
        "INSERT INTO announcements (userid, projectid, title, content) VALUES (%(userid)s, %(id)s, %(title)s, "
        "%(content)s)",
        {'userid': get_jwt_identity(), 'id': id, 'content': content, 'title': title})
    return response("Announcement in project={projectid} successfully posted".format(projectid=str(id)), 200)