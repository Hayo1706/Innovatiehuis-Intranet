# GET roles
import connexion
from flask_jwt_extended import get_jwt_identity

from src.services.helper_functions import query_update, query, response
from src.services.permissions import Roles
from src.services.permissions.permissions import check_permissions, check_jwt
from ..services.extensions import bcrypt


@check_jwt()
def get_roles():
    return response('Succes', 200, query(
        "SELECT * FROM roles;"))


# PUT roles/{roleid}
@check_permissions(Roles.check_role_permissions)
def update_role(role_id):
    if not verify_password():
        return response('Wachtwoord Incorrect', 400)
    body = connexion.request.json
    body.pop('password')
    if body['role_name'] == 'admin':
        return response('Admin mag niet gewijzigd worden', 400)
    if str(body['roleid']) != role_id:
        return response('Fout bij het updaten van rol', 400)
    if int(body['may_cud_users_with_power_level_up_to']) > int(body['power_level']):
        return response('may_cud_users_with_power_level_up_to mag niet hoger zijn dan power_level', 400)
    if body['role_name'] == 'admin':
        return response('Admin mag niet gewijzigd worden', 400)
    admin_power_level = query("SELECT power_level FROM roles WHERE role_name=admin")
    if int(body['power_level']) >= int(admin_power_level) or body[
        'may_cud_users_with_power_level_up_to'] >= admin_power_level:
        return response('Er mag geen rol bestaan met een hogere of gelijke power_level/ '
                        'may_cud_users_with_power_level_up_to als het power_level van die van de admin', 400)
    if int(body['power_level']) < 0 or int(body['power_level']) > 100 or \
            int(body['may_cud_users_with_power_level_up_to']) < 0 or int(
        body['may_cud_users_with_power_level_up_to']) > 100:
        return response('may_cud_users_with_power_level_up_to en power_level moeten waardes hebben tussen 0 en 100')
    query_update(
        "UPDATE roles SET may_cud_users_with_power_level_up_to=%(may_cud_users_with_power_level_up_to)s,power_level=%("
        "power_level)s,may_archive_any_project=%(may_archive_any_project)s, "
        "may_create_announcement_anywhere=%(may_create_announcement_anywhere)s,"
        "may_create_announcement_in_own_project=%(may_create_announcement_in_own_project)s,"
        "may_create_chat_message_anywhere=%(may_create_chat_message_anywhere)s,"
        "may_create_chat_message_in_own_project=%(may_create_chat_message_in_own_project)s,"
        "may_create_project=%(may_create_project)s,may_create_reply_anywhere=%(may_create_reply_anywhere)s,"
        "may_create_reply_in_own_project=%(may_create_reply_in_own_project)s,may_create_users=%("
        "may_create_users)s,may_crud_roles=%(may_crud_roles)s,may_delete_any_user=%(may_delete_any_user)s,"
        "may_read_any_project=%("
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
