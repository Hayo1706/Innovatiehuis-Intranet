def check_role_permissions(user_perm, *args):
    return user_perm["may_crud_roles"]
