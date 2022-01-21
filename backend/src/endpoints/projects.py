import src.config as config
import connexion
from ..services.helper_functions import *
from flask_jwt_extended import get_jwt_identity
from ..services.permissions import Projects, Announcements
from ..services.permissions.permissions import check_permissions


@check_permissions(Projects.may_read)
def read_one(project_id):
    return response("Succes",200,query(
        "SELECT projectid, project_name, description, is_archived, created, last_updated "
        "FROM projects WHERE projectid = %(id)s",
        {'id': project_id}))


@check_permissions(Projects.may_read_all)
def read_all():
    return response("Succes",200,query("SELECT projectid, project_name, description, is_archived, created, last_updated FROM projects"))


@check_permissions(Projects.may_create)
def create():
    try:
        body = connexion.request.json['project']
        project_name = body['project_name']
        description = body['description']
        memberIds = body['memberids']
        parentIds = body['parentids']
        childIds = body['childids']
    except KeyError:
        return response("Foute aanvraag", 400)
    query_update(
        "INSERT INTO projects (project_name, description) VALUES (%(project_name)s, %(description)s)",
        {'project_name': project_name, 'description': description}
    )
    projectid = query(
        "SELECT projectid FROM projects ORDER BY created DESC LIMIT 1"
    )[0]["projectid"]
    for id in memberIds:
        add_user(project_id=projectid, user_id=id)
    for id in parentIds:
        add_parent(project_id=projectid, parent_id=id)
    for id in childIds:
        add_child(project_id=projectid, child_id=id)
    return response("Project aangemaakt", 200)


@check_permissions(Projects.may_update)
def update(project_id):
    try:
        body = connexion.request.json['project']
        project_name = body['project_name']
        description = body['description']
    except KeyError:
        return response("Foute aanvraag", 400)

    query_update("UPDATE projects "
                 "SET project_name = %(project_name)s, description = %(description)s "
                 "WHERE projectid = %(projectid)s",
                 {'project_name': project_name, 'description': description,
                  'projectid': project_id})
    return response("Project gewijzigd")


# projects/{id}/archive
@check_permissions(Projects.may_archive)
def update_archive(project_id):
    try:
        body = connexion.request.json['project']
        is_archived = body['is_archived']
    except KeyError:
        return response("Foute aanvraag", 400)

    query_update("UPDATE projects "
                 "SET is_archived = %(is_archived)s "
                 "WHERE projectid = %(id)s",
                 {'is_archived': str(int(is_archived)),
                  'id': project_id})
    return response("Project gearchiveerd")


@check_permissions(Projects.may_delete)
def delete(project_id):
    query_update("DELETE FROM projects WHERE projectid = %(id)s", {'id': project_id})
    return response("Project verwijderd")


# projects/{id}/users
@check_permissions(Projects.may_read)   # TODO: placeholder for more specific permissions?
def read_users(project_id):
    return response("Succes",200,query(
        "SELECT userid, last_seen, first_name, last_name, email, phone_number, roleid, role_name, screening_status, "
        "created "
        "FROM users_have_projects "
        "LEFT JOIN users USING(userid) "
        "RIGHT JOIN roles USING(roleid) "
        "WHERE projectid = %(projectid)s",
        {'projectid': project_id}
    ))


@check_permissions(Projects.may_update)
def update_users(project_id):
    try:
        body = connexion.request.json
        new_ids = body['ids']
    except KeyError:
        return response("Foute aanvraag", 400)

    # 1 get all userids for project
    old_ids = [result["userid"] for result in query(
        "SELECT userid FROM users_have_projects WHERE projectid = %(projectid)s",
        {'projectid': project_id}
    )]
    # 2 cross-check with supplied userids
    ids_to_add = list(set(new_ids) - set(old_ids))
    ids_to_remove = list(set(old_ids) - set(new_ids))
    # 3 query changes
    for new_id in ids_to_add:
        query_update(
            "INSERT INTO users_have_projects (userid, projectid) VALUES (%(id)s, %(projectid)s);",
            {'id': new_id, 'projectid': project_id}
        )
    for old_id in ids_to_remove:
        query_update(
            "DELETE FROM users_have_projects WHERE userid = %(id)s AND projectid = %(projectid)s;",
            {'id': old_id, 'projectid': project_id}
        )
    return response("Gebruikerslijst van project gewijzigd", 200)


@check_permissions(Projects.may_update)
def add_user(project_id, user_id):
    query_update(
        "INSERT INTO users_have_projects (userid, projectid) VALUES (%(id)s, %(projectid)s);",
        {'id': user_id, 'projectid': project_id}
    )
    return response("Gebruiker toegevoegd aan project", 200)


@check_permissions(Projects.may_update)
def remove_user(project_id, user_id):
    query_update(
        "DELETE FROM users_have_projects WHERE userid = %(id)s AND projectid = %(projectid)s;",
        {'id': user_id, 'projectid': project_id}
    )
    return response("Gebruiker verwijderd van project", 200)


# projects/{id}/parents
@check_permissions(Projects.may_read)  # TODO: placeholder for more specific permissions?
def read_parents(project_id):
    return response("Succes",200,query(
        "SELECT projectid, shared_files, project_name, description, is_archived, created, last_updated "
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.parentid = projects.projectid "
        "WHERE childid = %(projectid)s",
        {'projectid': project_id}))


@check_permissions(Projects.may_update)
def update_parents(project_id):
    try:
        body = connexion.request.json
        new_ids = body['ids']
    except KeyError:
        return response("Foute aanvraag", 400)

    # 1 get all parent project ids
    old_ids = [result["parentid"] for result in query(
        "SELECT parentid FROM projects_have_parents WHERE childid = %(projectid)s",
        {'projectid': project_id}
    )]
    # 2 cross-check with supplied userids
    ids_to_add = list(set(new_ids) - set(old_ids))
    ids_to_remove = list(set(old_ids) - set(new_ids))
    # 3 query changes
    for new_id in ids_to_add:
        query_update(
            "INSERT INTO projects_have_parents (parentid, childid) VALUES (%(new_id)s, %(projectid)s);",
            {'new_id': new_id, 'projectid': project_id}
        )
    for old_id in ids_to_remove:
        query_update(
            "DELETE FROM projects_have_parents WHERE parentid = %(old_id)s AND childid = %(projectid)s;",
            {'old_id': old_id, 'projectid': project_id}
        )
    return response("Overkoepelende projecten van project gewijzigd", 200)


@check_permissions(Projects.may_update)  # TODO: placeholder for more specific permissions?
def add_parent(project_id, parent_id):
    query_update(
        "INSERT INTO projects_have_parents (childid, parentid) VALUES (%(projectid)s, %(parentid)s)",
        {'projectid': project_id, 'parentid': parent_id})
    return response("Overkoepelend project toegevoegd aan project")


@check_permissions(Projects.may_update)  # TODO: placeholder for more specific permissions?
def remove_parent(project_id, parent_id):
    query_update(
        "DELETE FROM projects_have_parents WHERE childid = %(projectid)s AND parentid = %(parentid)s",
        {'projectid': project_id, 'parentid': parent_id})
    return response("Overkoepelend project verwijderd van project")


# projects/{id}/children
@check_permissions(Projects.may_read)  # TODO: placeholder for more specific permissions?
def read_children(project_id):  # returns array of id/name/shared_files combinations
    return response('Succes',200, query(
        "SELECT projectid, project_name, description, is_archived, created, projects.last_updated "
        "FROM projects_have_parents "
        "JOIN projects "
        "ON projects_have_parents.childid = projects.projectid "
        "WHERE parentid = %(projectid)s",
        {'projectid': project_id}))


@check_permissions(Projects.may_update)
def update_children(project_id):
    try:
        body = connexion.request.json
        new_ids = body['ids']
    except KeyError:
        return response("Foute aanvraag", 400)

    # 1 get all parent project ids
    old_ids = [result["childid"] for result in query(
        "SELECT childid FROM projects_have_parents WHERE parentid = %(projectid)s",
        {'projectid': project_id}
    )]
    # 2 cross-check with supplied userids
    ids_to_add = list(set(new_ids) - set(old_ids))
    ids_to_remove = list(set(old_ids) - set(new_ids))
    # 3 query changes
    for new_id in ids_to_add:
        query_update(
            "INSERT INTO projects_have_parents (parentid, childid) VALUES (%(projectid)s, %(new_id)s);",
            {'new_id': new_id, 'projectid': project_id}
        )
    for old_id in ids_to_remove:
        query_update(
            "DELETE FROM projects_have_parents WHERE parentid = %(projectid)s AND childid = %(old_id)s;",
            {'old_id': old_id, 'projectid': project_id}
        )
    return response("Sub-projecten van project gewijzigd", 200)


# projects/{id}/children/{id}
@check_permissions(Projects.may_update)  # TODO: placeholder for more specific permissions?
def add_child(project_id, child_id):
    query_update(
        "INSERT INTO projects_have_parents (childid, parentid) VALUES (%(childid)s, %(projectid)s)",
        {'projectid': project_id, 'childid': child_id})
    return response("Sub-project toegevoegd aan project")


@check_permissions(Projects.may_update)  # TODO: placeholder for more specific permissions?
def update_shared_files(project_id, child_id):
    try:
        body = connexion.request.json['project']
        shared_files_string = body['shared_files']
    except KeyError:
        return response("Foute aanvraag", 400)
    query_update(
        "UPDATE projects_have_parents "
        "SET shared_files = %(shared_files)s "
        "WHERE parentid = %(projectid)s AND childid = %(childid)s",
        {'shared_files': shared_files_string, 'projectid': project_id, 'childid': child_id}
    )
    #TODO dit nederlands maken
    return response(f"Successfully updated list of files shared between parent {project_id} and child {child_id}.", 200)


@check_permissions(Projects.may_update)  # TODO: placeholder for more specific permissions?
def remove_child(project_id, child_id):
    query_update(
        "DELETE FROM projects_have_parents WHERE childid = %(childid)s AND parentid = %(projectid)s",
        {'projectid': project_id, 'childid': child_id})
    return response("Sub-project verwijderd van project", 200)


# projects/{id}/announcements
@check_permissions(Announcements.may_read_all_from_project)
def read_announcements(project_id):
    return response('Succes',200,query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid = %(id)s "
        "ORDER BY announcements.timestamp DESC", {'id': project_id}))


@check_permissions(Announcements.may_read_all_from_project)
def read_announcements_recent(project_id):
    cutoff_date = config.CUTOFF_DATE
    return response('Succes', 200,query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid = %(id)s AND announcements.timestamp > %(cutoff_date)s "
        "ORDER BY announcements.timestamp DESC", {'id': project_id, 'cutoffdate': cutoff_date}))


@check_permissions(Announcements.may_create_in_project)
def add_announcement(project_id):
    try:
        body = connexion.request.json['announcement']
        title = body['title']
        content = body['content']
    except KeyError:
        return response("Foute aanvraag", 400)
    query_update(
        "INSERT INTO announcements (userid, projectid, title, content) "
        "VALUES (%(userid)s, %(id)s, %(title)s, %(content)s)",
        {'userid': get_jwt_identity(), 'id': project_id, 'content': content, 'title': title})
    return response("Mededeling in project geplaatst", 200)
