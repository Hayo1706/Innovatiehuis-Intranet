import connexion

from ..services.helper_functions import *


def read_one(user_id):
    return query(
        "SELECT userid, first_name, last_name, email, roleid, role_name, screening_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen),created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) GROUP BY userid "
        "WHERE userid= %(id)s",
        {'id': user_id})


def read_all():
    return query(
        "SELECT userid, first_name, last_name, email, roleid, role_name, screening_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen),created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) GROUP BY userid")


def create():
    try:
        body = connexion.request.json
        first_name = body['first_name']
        last_name = body['last_name']
        email = body['email']
        roleid = body['roleid']
        screening_status = body['screening_status']
        password_hash = "123"  # TODO: dynamic hash creation
    except KeyError:
        return response("Invalid body", 404)

    query_update(
        "INSERT INTO users (first_name, last_name, email, roleid, screening_status, password_hash) "
        "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(roleid)s, %(screening_status)s,%(password_hash)s)",
        {'first_name': first_name, 'last_name': last_name, 'email': email, 'roleid': roleid,
         'screening_status': screening_status, 'password_hash': password_hash})
    return response("User successfully added", 200)


def update(user_id):
    is_int(user_id)

#   1 get current role of user
#   2 if specified role is changed, check permission using "UPDATE ROLE" OR "UPDATE ROLE PROTECTED"
#   3 abort immediately if user has no permission!

    try:
        body = connexion.request.json
        first_name = body['first_name']
        last_name = body['last_name']
        email = body['email']
        roleid = body['roleid']
        screening_status = body['screening_status']
    except KeyError:
        return response("Invalid body", 404)

    query_update(
        "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, roleid=%(roleid)s, "
        "screening_status=%(screening_status)s "
        "WHERE userid=%(userid)s",
        {'first_name': first_name, 'last_name': last_name, 'email': email, 'roleid': roleid,
         'screening_status': screening_status, "userid": user_id})
    return response(f"User {user_id} successfully updated", 200)


def delete(user_id):
    is_int(user_id)
    query_update("DELETE FROM users WHERE userid = %(id)s", {'id': user_id})
    return response(f"User {user_id} successfully deleted", 200)


# users/{id}/password
def update_password(user_id):
    is_int(user_id)
    try:
        body = connexion.request.json
        new_password_hash = body['password_hash']  # TODO: how to hash
    except KeyError:
        return response("Invalid body", 404)
    query_update("UPDATE users SET password_hash = %(hash)s WHERE userid = %(userid)s", {'hash': new_password_hash, 'userid': user_id})


# users/{id}/projects
def read_projects(user_id):
    return query("SELECT * FROM users_have_projects INNER JOIN projects ON "
                 "users_have_projects.projectid = projects.projectid "
                 "WHERE users_have_projects.userid = %(id)s AND projects.is_archived = 0", {'id': user_id})


def add_project(user_id):
    is_int(user_id)
    try:
        body = connexion.request.json
        project_id = body['projectid']
        is_int(project_id)
    except KeyError:
        return response("Invalid body", 404)
    query_update(f"INSERT INTO users_have_projects (userid, projectid) VALUES (%(userid)s, %(projectid)s)", {'userid': user_id, 'projectid': project_id})
    return response(f"Successfully assigned {project_id} to project {project_id}")
