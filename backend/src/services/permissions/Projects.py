import src.services.permissions.permissions as permissions


def may_read_all(user_perm):
    return user_perm["may_read_any_project"]


def may_read(user_perm, project_id):
    return user_perm["may_read_any_project"] or (
            user_perm["may_read_own_project"] and permissions.user_owns_project(project_id))


def may_create(user_perm):
    return user_perm["may_create_project"]


def may_update(user_perm, resource_id):
    return user_perm["may_update_any_project"] or (
            user_perm["may_update_own_project"] and permissions.user_owns_project(resource_id))


def may_archive(user_perm):
    return user_perm["may_archive_any_project"]


def may_delete(user_perm):
    return user_perm["may_delete_any_project"]


def may_read_files(user_perm, project_id):
    return permissions.user_owns_project(project_id) or user_perm["may_read_any_project"]


def may_cud_files(user_perm, project_id):
    return user_perm["may_update_any_file"] or \
           user_perm["may_update_file_in_own_project"] and permissions.user_owns_project(project_id)
