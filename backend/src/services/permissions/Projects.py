import connexion

import src.services.permissions.permissions as permissions
from src.services.helper_functions import query


def may_read_all(user_perm):
    return user_perm["may_read_any_project"]


def may_read(user_perm, project_id):
    return user_perm["may_read_any_project"] or (
            user_perm["may_read_own_project"] and permissions.user_owns_project(project_id))


def may_create(user_perm):
    return user_perm["may_create_project"]


def may_update(user_perm, *ids):
    return user_perm["may_update_any_project"] or (
            user_perm["may_update_own_project"] and permissions.user_owns_project(ids[0]))


def may_archive(user_perm, project_id):
    return user_perm["may_archive_any_project"]


def may_delete(user_perm, project_id):
    return user_perm["may_delete_any_project"]


def may_read_files(user_perm, project_id):
    return permissions.user_owns_project(project_id) or user_perm["may_read_any_project"]


def may_cud_files(user_perm, project_id):
    return user_perm["may_update_any_file"] or \
           user_perm["may_update_file_in_own_project"] and permissions.user_owns_project(project_id)


def may_read_shared_files(user_perm, project_id):
    if permissions.user_owns_project(project_id) or user_perm["may_read_any_project"]:
        return True

    path = connexion.request.values.get('path')
    child_projects = query("SELECT childid, shared_files FROM projects_have_parents WHERE parentid = %(parentid)s",
                           {'parentid': project_id})
    for child in [{'id': project.childid, 'shared_files': project.shared_files} for project in child_projects]:
        if permissions.user_owns_project(child['id']):
            if path in child['shared_files']:
                return True
    return False
