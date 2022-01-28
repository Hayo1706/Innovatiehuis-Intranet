from flask_jwt_extended import get_jwt_identity

import src.services.permissions.permissions as permissions
from src.services.helper_functions import query


def may_read(user_perm, user_id):
    return user_perm["may_read_any_user"] or \
           permissions.user_owns_account(user_id) or \
           (user_perm["may_read_user_in_own_project"] and
            permissions.user_owns_associated_user_project(user_id))


def may_read_all(user_perm):
    return user_perm["may_read_any_user"]


def may_create(user_perm):
    return user_perm["may_create_users"]


def may_update(user_perm, user_id):
    return user_perm["may_update_any_user_account"] or \
           (user_perm["may_update_own_account"] and permissions.user_owns_account(user_id)) \
           and has_high_enough_power_level(user_id)


def may_update_password(user_perm, user_id):
    return user_perm["may_update_any_password"] or \
           (user_perm["may_update_own_password"] and permissions.user_owns_account(user_id)) \
           and has_high_enough_power_level(user_id)


def may_update_role(user_perm, *ids):
    print(get_power_level((get_jwt_identity())))
    return user_perm["may_update_any_user_role"] and not permissions.user_owns_account(ids[0]) \
           and has_high_enough_power_level(ids[0]) \
           and get_power_level(get_jwt_identity())['may_cud_users_with_power_level_up_to'] >= int(ids[1])


def may_update_screening(user_perm, *ids):
    return user_perm["may_update_any_user_screening_status"] and not permissions.user_owns_account(ids[0]) \
           and has_high_enough_power_level(ids[0])


def may_read_user_projects(user_perm, user_id):
    return user_perm['may_read_any_project'] or \
           (permissions.user_owns_account(user_id) and user_perm['may_read_own_project'])


def may_delete_user(user_perm, user_id):
    return user_perm["may_delete_any_user"] and not permissions.user_owns_account(user_id) \
           and has_high_enough_power_level(user_id)


def has_high_enough_power_level(called):
    caller_role = get_power_level(get_jwt_identity())
    called_role = get_power_level(called)
    return caller_role['may_cud_users_with_power_level_up_to'] >= called_role['power_level']


def get_power_level(user_id):
    return query("SELECT roles.power_level, roles.may_cud_users_with_power_level_up_to "
                 "FROM roles INNER JOIN users ON users.roleid=roles.roleid WHERE users.userid=%(userid)s",
                 {'userid': user_id})[0]
