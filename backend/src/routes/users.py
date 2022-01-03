import connexion

from ..services.helper_functions import *
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required()
def read_all():
    return query(
        "SELECT userid, first_name, last_name, email, roleid, role_name, screening_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen),created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) GROUP BY userid")


def read_one(id):
    return query(
        "SELECT userid, first_name, last_name, email, roleid, role_name, screening_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen),created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) GROUP BY userid where "
        "userid= %(id)s",
        {'id': id})


def read_user_projects(id):
    return query("SELECT * FROM users_have_projects INNER JOIN projects ON "
                 "users_have_projects.projectid = projects.projectid "
                 "WHERE users_have_projects.userid = %(id)s AND projects.is_archived = 0", {'id': id})


def delete(id):
    is_int(id)
    query_update("DELETE FROM users WHERE userid =%(id)s", {'id': id})
    return response("{id} successfully deleted".format(id=str(id)), 200)


def post():
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
        "INSERT INTO users (first_name, last_name, email, roleid, screening_status, password_hash) VALUES (%(first_name)s, "
        "%(last_name)s, %(email)s, %(roleid)s, %(screening_status)s,%(password_hash)s)",
        {'first_name': first_name, 'last_name': last_name, 'email': email, 'roleid': roleid,
         'screening_status': screening_status, 'password_hash': password_hash})
    return response("User successfully added", 200)


def put(id):
    is_int(id)
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
        "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, roleid=%(roleid)s, screening_status=%(screening_status)s WHERE userid=%(userid)s",
        {'first_name': first_name, 'last_name': last_name, 'email': email, 'roleid': roleid,
         'screening_status': screening_status, "userid": id})
    return response("User successfully updated", 200)
