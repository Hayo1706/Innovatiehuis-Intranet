import secrets
from datetime import date
import src.config as config
import pyotp
from ..config import PASSWORD_CHANGE_SECRET_KEY, DOMAIN_NAME
from ..services.helper_functions import *
from itsdangerous import URLSafeSerializer
from ..services.permissions import Users, Projects, Roles
from ..services.permissions.permissions import check_permissions, check_jwt
from ..services.extensions import bcrypt
from flask_jwt_extended import get_jwt_identity
import threading
import qrcode
from PIL import Image


# READ users
@check_permissions(Users.may_read_all)
def read_all():
    return response('Succes',200, query(
        "SELECT userid, first_name, last_name, email, phone_number, roleid, role_name, power_level, access_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen),created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) GROUP BY userid"))


# READ users/{id}
@check_permissions(Users.may_read)
def read_one(user_id):
    return response('Succes',200, query(
        "SELECT userid, first_name, last_name, email, phone_number, roleid, role_name, access_status, created, "
        "COUNT(projectid) AS amountprojects, IFNULL(MAX(last_seen), created) AS last_seen FROM (SELECT * FROM users "
        "LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_have_projects USING(userid) "
        "WHERE userid= %(id)s",
        {'id': user_id}))


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
        access_status = body['access_status']
        password_hash = bcrypt.generate_password_hash(secrets.token_urlsafe(16)).decode('utf-8')
        auth_key = pyotp.random_base32()



    except KeyError:
        return response("Een verzoek aan de server miste belangrijke informatie; neem contact op met de beheerder!", 400)

    emails_in_use = [user["email"] for user in query("SELECT email FROM users")]
    if email in emails_in_use:
        return response("Dit mailadres is al in gebruik!", 400)

    query_update(
        "INSERT INTO users (first_name, last_name, email, phone_number, roleid, access_status, password_hash, auth_key) "
        "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(roleid)s, %(access_status)s,%(password_hash)s,%(auth_key)s)",
        {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone_number': phone_number,
         'roleid': roleid,
         'access_status': access_status, 'password_hash': password_hash, 'auth_key': auth_key})
    serializer = URLSafeSerializer(PASSWORD_CHANGE_SECRET_KEY)
    d1 = date.today().strftime("%d/%m/%Y")
    userid = query("SELECT userid FROM users WHERE email=%(email)s", {'email': email})[0]['userid']
    resp = DOMAIN_NAME + "/manage/resetpassword?resettoken=" + serializer.dumps([userid, password_hash])

    data_thread = threading.Thread(target=lambda: send_data_to_user(auth_key, first_name, email, resp))
    data_thread.start()

    return response("Gebruiker toegevoegd", 200, resp)

# TODO send data below to user via mail
def send_data_to_user(auth_key, first_name, email, resp):
    print(resp)
    totp_url = pyotp.totp.TOTP(auth_key, interval=30).provisioning_uri(name=first_name+ "@innovatiehuis",issuer_name='Innovatiehuis')
    img = qrcode.make(totp_url)
    img.show()

# PUT users/{id}
@check_permissions(Users.may_update)
def update(user_id):
    try:
        body = connexion.request.json
        first_name = body['first_name']
        last_name = body['last_name']
        email = body['email']
        phone_number = body['phone_number']
    except KeyError:
        return response("Een verzoek aan de server miste belangrijke informatie; neem contact op met de beheerder!", 400)

    query_update(
        "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, "
        "phone_number=%(phone_number)s "
        "WHERE userid=%(userid)s",
        {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone_number': phone_number,
         "userid": user_id})
    return response("Persoonsgegevens aangepast", 200)


# PATCH users/{id}/access/{status}
@check_permissions(Users.may_update_access)
def update_access(user_id, access_status):
    query_update(
        "UPDATE users SET access_status=%(access_status)s WHERE userid=%(userid)s",
        {'access_status': access_status, "userid": user_id})
    return response("Toegang van gebruiker aangepast")


# PATCH users/{id}/role/{id}
@check_permissions(Users.may_update_role)
def update_role_user(user_id, role_id):
    query_update(
        "UPDATE users SET roleid=%(roleid)s WHERE userid=%(userid)s",
        {'roleid': role_id, "userid": user_id})
    return response("Rol van gebruiker aangepast")


# PATCH users/{id}/password
@check_permissions(Users.may_update_password)
def update_password(user_id):
    try:
        body = connexion.request.json
        new_password_hash = body['password_hash']
    except KeyError:
        return response("Een verzoek aan de server miste belangrijke informatie; neem contact op met de beheerder!", 400)
    query_update("UPDATE users SET password_hash = %(hash)s WHERE userid = %(userid)s",
                 {'hash': new_password_hash, 'userid': user_id})
    response('Wachtwoord gewijzigd')


# DELETE users/{id}
@check_permissions(Users.may_delete_user)
def delete(user_id):
    query_update("DELETE FROM users WHERE userid = %(id)s", {'id': user_id})
    return response(f"Gebruiker verwijderd")


# READ users/{id}/projects
@check_jwt()
def read_projects(user_id):
    # this endpoint only returns the projects that the requesting user is permitted to see
    if config.DEBUG_MODE or get_jwt_identity() == user_id or check_permissions(Projects.may_read_all):
        return response('Succes', 200, query("SELECT * FROM users_have_projects INNER JOIN projects "
                                             "ON users_have_projects.projectid = projects.projectid "
                                             "WHERE users_have_projects.userid = %(id)s AND projects.is_archived = 0",
                                             {'id': user_id}))

    permitted_projects = query("SELECT projectid FROM users_have_projects WHERE users_have_projects.userid = %(id)s",
                               {'id': get_jwt_identity()})
    permitted_ids = [project.projectid for project in permitted_projects]
    data = []
    for project in query("SELECT * FROM users_have_projects INNER JOIN projects "
                         "ON users_have_projects.projectid = projects.projectid "
                         "WHERE users_have_projects.userid = %(id)s AND projects.is_archived = 0",
                         {'id': user_id}):
        if project.projectid in permitted_ids:
            data.append(project)
    return response('Succes', 200, data)
