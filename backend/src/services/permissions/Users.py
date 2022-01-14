import src.services.permissions.permissions as permissions


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
           (user_perm["may_update_own_account"] and permissions.user_owns_account(user_id))


def may_update_password(user_perm, user_id):
    return user_perm["may_update_any_password"] or \
           (user_perm["may_update_own_password"] and permissions.user_owns_account(user_id))


def may_update_role(user_perm, *ids):
    return user_perm["may_update_any_user_role"] and not permissions.user_owns_account(ids[0])


def may_update_role_protected(user_perm, user_id):
    return user_perm["may_elevate_to_protected_role"] and not permissions.user_owns_account(user_id)


def may_update_screening(user_perm, *ids):
    return user_perm["may_update_any_user_screening_status"] and not permissions.user_owns_account(ids[0])


def may_read_user_projects(user_perm, user_id):
    return user_perm['may_read_any_project'] or \
           (permissions.user_owns_account(user_id) and user_perm['may_read_own_project'])


def may_delete_user(user_perm, user_id):
    return user_perm["may_delete_any_user"] and not permissions.user_owns_account(user_id)
