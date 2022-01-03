from ..services.helper_functions import *


def read_all():
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
