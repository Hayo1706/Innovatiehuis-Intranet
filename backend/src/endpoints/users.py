import secrets
from datetime import date

import connexion
from flask_jwt_extended import jwt_required
from ..config import PASSWORD_CHANGE_SECRET_KEY, DOMAIN_NAME
from ..services.helper_functions import *
from itsdangerous import URLSafeSerializer
from ..services.permissions import Users
from ..services.permissions.permissions import check_permissions
from ..services.extensions import bcrypt


@check_permissions(Users.may_read)
def read_one(user_id):
    return query(
        "SELECT userid, first_name, last_name, email, roleid, role_name, screening_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen), created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) "
        "WHERE userid= %(id)s",
        {'id': user_id})


@check_permissions(Users.may_read_all)
def read_all():
    return query(
        "SELECT userid, first_name, last_name, email, roleid, role_name, screening_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen),created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) GROUP BY userid")


@check_permissions(Users.may_create)
def create():
    try:
        body = connexion.request.json
        first_name = body['first_name']
        last_name = body['last_name']
        email = body['email']
        roleid = body['roleid']
        screening_status = body['screening_status']
        password_hash = bcrypt.generate_password_hash(secrets.token_urlsafe(16)).decode('utf-8')
    except KeyError:
        return response("Invalid body", 400)

    query_update(
        "INSERT INTO users (first_name, last_name, email, roleid, screening_status, password_hash) "
        "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(roleid)s, %(screening_status)s,%(password_hash)s)",
        {'first_name': first_name, 'last_name': last_name, 'email': email, 'roleid': roleid,
         'screening_status': screening_status, 'password_hash': password_hash})
    serializer = URLSafeSerializer(PASSWORD_CHANGE_SECRET_KEY)
    d1 = date.today().strftime("%d/%m/%Y")
    userid = query("SELECT userid FROM users WHERE email=%(email)s", {'email': email})[0]['userid']
    return response("User successfully added", 200, link=
        DOMAIN_NAME + "/manage/resetpassword?resettoken=" + serializer.dumps([userid, password_hash]))


@check_permissions(Users.may_update)
def update(user_id):
    

    # TODO:
    #   1 get current role and screening status of user
    #   2 if specified role is changed, check permission using "UPDATE ROLE" OR "UPDATE ROLE PROTECTED"
    #   3 abort immediately if user has no permission!
    #   4 if screening status is changed and role is protected, abort! admin should not be able to disable their own account...

    try:
        body = connexion.request.json
        first_name = body['first_name']
        last_name = body['last_name']
        email = body['email']
        roleid = body['roleid']
        screening_status = body['screening_status']
    except KeyError:
        return response("Invalid body", 400)

    query_update(
        "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, roleid=%(roleid)s, "
        "screening_status=%(screening_status)s "
        "WHERE userid=%(userid)s",
        {'first_name': first_name, 'last_name': last_name, 'email': email, 'roleid': roleid,
         'screening_status': screening_status, "userid": user_id})
    return response(f"User {user_id} successfully updated", 200)


@check_permissions(Users.may_delete_user)
def delete(user_id):
    
    query_update("DELETE FROM users WHERE userid = %(id)s", {'id': user_id})
    return response(f"User {user_id} successfully deleted", 200)


# users/{id}/password
@check_permissions(Users.may_update_password)
def update_password(user_id):
    
    try:
        body = connexion.request.json
        new_password_hash = body['password_hash']  # TODO: how to hash
    except KeyError:
        return response("Invalid body", 400)
    query_update("UPDATE users SET password_hash = %(hash)s WHERE userid = %(userid)s",
                 {'hash': new_password_hash, 'userid': user_id})


# users/{id}/projects
@check_permissions(Users.may_read_user_projects)
def read_projects(user_id):
    return query("SELECT * FROM users_have_projects INNER JOIN projects ON "
                 "users_have_projects.projectid = projects.projectid "
                 "WHERE users_have_projects.userid = %(id)s AND projects.is_archived = 0", {'id': user_id})


# TODO Welke permissie?
def add_project(user_id):
    
    try:
        body = connexion.request.json
        project_id = body['projectid']
        
    except KeyError:
        return response("Invalid body", 400)
    query_update(f"INSERT INTO users_have_projects (userid, projectid) VALUES (%(userid)s, %(projectid)s)",
                 {'userid': user_id, 'projectid': project_id})
    return response(f"Successfully assigned {project_id} to project {project_id}")
