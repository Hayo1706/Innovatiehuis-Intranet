import secrets
from datetime import date

import connexion
from flask_jwt_extended import jwt_required
from ..config import PASSWORD_CHANGE_SECRET_KEY, DOMAIN_NAME
from ..services.helper_functions import *
from itsdangerous import URLSafeSerializer
from ..services.permissions import Users, Projects
from ..services.permissions.permissions import check_permissions
from ..services.extensions import bcrypt


# READ users
@check_permissions(Users.may_read_all)
def read_all():
    return query(
        "SELECT userid, first_name, last_name, email, phone_number, roleid, role_name, screening_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen),created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) GROUP BY userid")

# READ users/{id}
@check_permissions(Users.may_read)
def read_one(user_id):
    return query(
        "SELECT userid, first_name, last_name, email, phone_number, roleid, role_name, screening_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen), created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) "
        "WHERE userid= %(id)s",
        {'id': user_id})

# POST users
@check_permissions(Users.may_create)
def create():
    try:
        body = connexion.request.json
        first_name = body['first_name']
        last_name = body['last_name']
        email = body['email']
        phone_number = body['phone_number']
        roleid = body['roleid']
        screening_status = body['screening_status']
        password_hash = bcrypt.generate_password_hash(secrets.token_urlsafe(16)).decode('utf-8')
    except KeyError:
        return response("Invalid body", 400)
    query_update(
        "INSERT INTO users (first_name, last_name, email, phone_number, roleid, screening_status, password_hash) "
        "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(roleid)s, %(screening_status)s,%(password_hash)s)",
        {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone_number': phone_number, 'roleid': roleid,
         'screening_status': screening_status, 'password_hash': password_hash})
    serializer = URLSafeSerializer(PASSWORD_CHANGE_SECRET_KEY)
    d1 = date.today().strftime("%d/%m/%Y")
    userid = query("SELECT userid FROM users WHERE email=%(email)s", {'email': email})[0]['userid']
    return response("User successfully added", 200, link=
        DOMAIN_NAME + "/manage/resetpassword?resettoken=" + serializer.dumps([userid, password_hash]))


# PUT users/{id}
@check_permissions(Users.may_update)
def update(user_id):
    try:
        body = connexion.request.json
        first_name = body['first_name']
        last_name = body['last_name']
        email = body['email']
        phone_number = body['phone_number']
        roleid = body['roleid']
        screening_status = body['screening_status']
    except KeyError:
        return response("Invalid body", 400)

    data = query(
        "SELECT screening_status, roleid FROM users JOIN roles USING(roleid) WHERE userid = %(user_id)s",
        {'user_id': user_id})

    if roleid != data[0]["roleid"]:
        update_role(user_id, roleid)
    if screening_status != data[0]["screening_status"]:
        update_screening(user_id, screening_status)

    query_update(
        "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, "
        "phone_number=%(phone_number)s "
        "WHERE userid=%(userid)s",
        {'first_name': first_name, 'last_name': last_name, 'email': email,'phone_number': phone_number,
         "userid": user_id})
    return response(f"User {user_id} successfully updated", 200)


# PATCH users/{id}/screening/{status}
@check_permissions(Users.may_update_screening)
def update_screening(user_id, screening_status):
    query_update(
        "UPDATE users SET screening_status=%(screening_status)s WHERE userid=%(userid)s",
        {'screening_status': screening_status, "userid": user_id})
    return response(f"Successfully changed screening status of User {user_id}", 200)


# PATCH users/{id}/role/{id}
@check_permissions(Users.may_update_role)
def update_role(user_id, role_id):
    is_protected = query(
        "SELECT is_protected FROM roles WHERE roleid = %(role_id)s",
        {'role_id': role_id})[0]["is_protected"]
    if is_protected:
        return update_role_protected(user_id, role_id)

    query_update(
        "UPDATE users SET roleid=%(roleid)s WHERE userid=%(userid)s",
        {'roleid': role_id, "userid": user_id})
    return response(f"User {user_id} successfully granted new role", 200)


# NOT AN ENDPOINT
@check_permissions(Users.may_update_role_protected)
def update_role_protected(user_id, role_id):
    query_update(
        "UPDATE users SET roleid=%(roleid)s WHERE userid=%(userid)s",
        {'roleid': role_id, "userid": user_id})
    return response(f"User {user_id} successfully elevated to protected role", 200)


# PATCH users/{id}/password
@check_permissions(Users.may_update_password)
def update_password(user_id):
    try:
        body = connexion.request.json
        new_password_hash = body['password_hash']  # TODO: how to hash
    except KeyError:
        return response("Invalid body", 400)
    query_update("UPDATE users SET password_hash = %(hash)s WHERE userid = %(userid)s",
                 {'hash': new_password_hash, 'userid': user_id})


# DELETE users/{id}
@check_permissions(Users.may_delete_user)
def delete(user_id):
    query_update("DELETE FROM users WHERE userid = %(id)s", {'id': user_id})
    return response(f"User {user_id} successfully deleted", 200)


# READ users/{id}/projects
@check_permissions(Users.may_read_user_projects)
def read_projects(user_id):
    return query("SELECT * FROM users_have_projects INNER JOIN projects "
                 "ON users_have_projects.projectid = projects.projectid "
                 "WHERE users_have_projects.userid = %(id)s AND projects.is_archived = 0", {'id': user_id})


# POST users/{id}/projects/{id}
# TODO: WERKT DEZE PERMISSIE? ZO NIET, DELETE (ook uit YAML)
@check_permissions(Projects.may_update)
def add_project(user_id, project_id):
    try:
        body = connexion.request.json
    except KeyError:
        return response("Invalid body", 400)
    query_update(f"INSERT INTO users_have_projects (userid, projectid) VALUES (%(userid)s, %(projectid)s)",
                 {'userid': user_id, 'projectid': project_id})
    return response(f"Successfully assigned {project_id} to project {project_id}")
