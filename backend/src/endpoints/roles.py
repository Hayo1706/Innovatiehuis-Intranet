# GET roles
import connexion
from flask_jwt_extended import get_jwt_identity

from src.services.helper_functions import query_update, query, response
from src.services.permissions import Roles
from src.services.permissions.permissions import check_permissions, check_jwt
from ..services.extensions import bcrypt


@check_jwt()
def get_roles():
    return response('Sucecs',200, query(
        "SELECT * FROM roles;"))


# PUT roles/{roleid}
@check_permissions(Roles.check_role_permissions)
def update_role(role_id):
    if not verify_password():
        return response('Wachtwoord Incorrect', 400)
    body = connexion.request.json
    body.pop('password')
    if body['role_name'] == 'admin':
        return response('Admin mag niet gewijzigd worden',400)
    if str(body['roleid']) != role_id:
        return response('Fout bij het updaten van rol', 400)

    query_update(
        "UPDATE roles SET is_protected=%(is_protected)s,may_archive_any_project=%(may_archive_any_project)s,"
        "may_create_announcement_anywhere=%(may_create_announcement_anywhere)s,"
        "may_create_announcement_in_own_project=%(may_create_announcement_in_own_project)s,"
        "may_create_chat_message_anywhere=%(may_create_chat_message_anywhere)s,"
        "may_create_chat_message_in_own_project=%(may_create_chat_message_in_own_project)s,"
        "may_create_project=%(may_create_project)s,may_create_reply_anywhere=%(may_create_reply_anywhere)s,"
        "may_create_reply_in_own_project=%(may_create_reply_in_own_project)s,may_create_users=%("
        "may_create_users)s,may_crud_roles=%(may_crud_roles)s,may_delete_any_user=%(may_delete_any_user)s,"
        "may_elevate_to_protected_role=%(may_elevate_to_protected_role)s,may_read_any_project=%("
        "may_read_any_project)s,may_read_any_user=%(may_read_any_user)s,may_read_own_project=%("
        "may_read_own_project)s,may_read_user_in_own_project=%(may_read_user_in_own_project)s,"
        "may_update_any_announcement=%(may_update_any_announcement)s,may_update_any_chat_message=%("
        "may_update_any_chat_message)s,may_update_any_file=%(may_update_any_file)s,may_update_any_project=%("
        "may_update_any_project)s,may_update_any_reply=%(may_update_any_reply)s,"
        "may_update_any_user_account=%(may_update_any_user_account)s,may_update_any_user_password=%("
        "may_update_any_user_password)s,may_update_any_user_role=%(may_update_any_user_role)s,"
        "may_update_any_user_screening_status=%(may_update_any_user_screening_status)s,"
        "may_update_file_in_own_project=%(may_update_file_in_own_project)s,may_update_own_chat_message=%("
        "may_update_own_chat_message)s,may_update_own_content=%(may_update_own_content)s,"
        "may_update_own_project=%(may_update_own_project)s,may_update_own_user_account=%("
        "may_update_own_user_account)s,may_update_own_user_password=%(may_update_own_user_password)s,"
        "role_name=%(role_name)s WHERE roleid=%(roleid)s", body)
    return response('Updaten van rol succesvol')


# POST roles
@check_permissions(Roles.check_role_permissions)
def add_role():
    try:
        name = connexion.request.json['role_name']
    except KeyError:
        return response("Foute aanvraag", 400)
    query_update("INSERT INTO roles (role_name) VALUES (%(role_name)s)", {'role_name': name})
    return response('Rol toegevoegd')


# DELETE roles/{roleid}
@check_permissions(Roles.check_role_permissions)
def delete_role(role_id):
    if not verify_password():
        return response('Wachtwoord Incorrect', 400)

    name = query("SELECT role_name FROM roles WHERE roleid=%(role_id)s", {'role_id': role_id})[0]
    if name == 'admin':
        return response('Admin mag niet verwijderd worden', 400)
    query_update("DELETE from roles WHERE roleid=%(role_id)s", {'role_id': role_id})
    return response('Rol verwijderd')


def verify_password():
    try:
        password = connexion.request.json['password']
    except KeyError:
        return False
    id = get_jwt_identity()
    user = query("SELECT password_hash FROM users WHERE userid =%(userid)s",
                 {'userid': id})[0]
    return bcrypt.check_password_hash(user['password_hash'], password)
