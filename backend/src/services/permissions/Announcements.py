import src.services.permissions.permissions as permissions


def may_read(user_perm, announcement_id):
    return user_perm['may_read_any_project'] or permissions.user_owns_announcement_associated_project(
        announcement_id)


def may_read_all_from_project(user_perm, project_id):
    return permissions.user_owns_project(project_id)


def may_create_in_project(user_perm, project_id):
    return user_perm["may_create_announcement_anywhere"] or \
           (user_perm["may_create_announcement_in_own_project"] and permissions.user_owns_project(
               project_id))


def may_create_global(user_perm):
    return user_perm["may_create_announcement_anywhere"]


def may_update_delete(user_perm, announcement_id):
    return user_perm["may_update_any_announcement"] or \
           user_perm["may_update_own_content"] and permissions.user_owns_announcement(announcement_id)


def may_add_reply(user_perm, announcement_id):
    return user_perm['may_create_reply_anywhere'] or (user_perm['may_create_reply_in_own_project']
        and permissions.user_owns_announcement_associated_project(announcement_id))


def may_read_reply(user_perm, announcement_id):
    return user_perm['may_read_any_project'] or permissions.user_owns_announcement_associated_project(
        announcement_id)


def may_update_delete_reply(user_perm, reply_id):
    return user_perm["may_update_any_reply"] or (
            user_perm["may_update_own_content"] and permissions.user_owns_reply(reply_id))
