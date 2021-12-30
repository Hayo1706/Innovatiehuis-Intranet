# from helper_functions import *
#
# ###### HOW TO CHECK ######
# ####### 1 RESOURCE #######
# # if !user_has_permission(userid, "READ", "project", projectid):
# #   abort(403, "Access Forbidden")
# # return query("SQL")
# ###### HOW TO CHECK ######
# ### MULTIPLE RESOURCES ###
# # data = query("SQL")
# # for project in data:
# #   if !user_has_permission(userid, "READ", "project", project["projectid"]):
# #       remove project (with iteration?)
# # if data.length = 0:
# #   abort(403, "Access Forbidden")
# # return data
# ###### HOW TO CHECK ######
# ######## FOR FILE ########
# # use projectid as resource_id!!!
#
# # TODO: permission_type enum and resource_type classes?
# def user_has_permission(user_id, permission_type, resource_type, resource_id):
#     permissions = query("SELECT roles.* FROM users JOIN roles ON users.roleid = roles.roleid WHERE userid = %(user_id)s",
#                         {'user_id': user_id})[0]
#
#     def user_owns_resource():
#         if resource_type == "project":
#             return user_id in projects.read_one(resource_id)[0]["users"] #todo: remove circularity
#         if resource_type == "user":
#             return user_id == resource_id
#         if resource_type == "announcement":
#             return user_id == announcements.read_one(resource_id)[0]["userid"] #todo: remove circularity
#         if resource_type == "reply":
#             return user_id == replies.read_one(resource_id)[0]["userid"] #todo: remove circularity
#         abort(500, "Internal Server Error while checking permissions")
#
#     def user_owns_associated_project(project_ids):
#         if resource_type in ("user", "announcement", "reply", "file"):
#             ids_to_check = []
#             for project_id in project_ids:
#                 ids_to_check.append(projects.read_one(project_id)[0]["users"]) #todo: remove circularity
#             return user_id in ids_to_check
#
#     def check_project_permissions():
#         if permission_type == "READ":
#             return permissions["may_read_any_project"] or \
#                    permissions["may_read_own_project"] and user_owns_resource()
#         if permission_type == "READ ALL":
#             return permissions["may_read_any_project"]
#         if permission_type == "CREATE":
#             return permissions["may_create_project"]
#         if permission_type == "UPDATE":
#             return permissions["may_update_any_project"] or \
#                    permissions["may_update_own_project"] and user_owns_resource()
#         if permission_type == "DELETE":
#             return permissions["may_delete_any_project"]
#
#     def check_user_permissions():
#         if permission_type == "READ":
#             return permissions["may_read_any_user"] or \
#                    user_owns_resource() or \
#                    permissions["may_read_user_in_own_project"] and \
#                    user_owns_associated_project(users.read_one(resource_id)[0]["projects"]) #todo: remove circularity
#         if permission_type == "READ ALL":
#             return permissions["may_read_any_user"]
#         if permission_type == "CREATE":
#             return permissions["may_create_user"]
#         if permission_type == "UPDATE":
#             return permissions["may_update_any_user"] or \
#                    permissions["may_update_own_account"] and user_owns_resource()
#         if permission_type == "UPDATE PASSWORD":
#             return permissions["may_update_any_password"] or \
#                    permissions["may_update_own_password"] and user_owns_resource()
#         if permission_type == "UPDATE ROLE":
#             return permissions["may_update_any_user_role"]
#         if permission_type == "UPDATE ROLE PROTECTED":
#             return permissions["may_elevate_to_protected_role"]
#         if permission_type == "DELETE":
#             return permissions["may_delete_any_user"] and user_id != resource_id
#
#     def check_announcement_permissions():
#         if permission_type == "READ":
#             return user_owns_associated_project(announcements.read_one(resource_id)[0]["projectid"]) #todo: remove circularity
#         if permission_type == "CREATE":
#             return permissions["may_create_announcement_anywhere"] or \
#                    permissions["may_create_announcement_in_own_project"] and user_owns_resource()
#         if permission_type in ("UPDATE", "DELETE"):
#             return permissions["may_update_any_announcement"] or \
#                    permissions["may_update_own_content"] and user_owns_resource()
#
#     def check_reply_permissions():
#         if permission_type == "READ":
#             return user_owns_associated_project(
#                 announcements.read_one(
#                     replies.read_one(resource_id)[0]["announcementid"] #todo: remove circularity
#                 )[0]["projectid"])
#         if permission_type == "CREATE":
#             return permissions["may_create_reply_anywhere"] or \
#                    permissions["may_create_reply_in_own_project"] and user_owns_resource()
#         if permission_type in ("UPDATE", "DELETE"):
#             return permissions["may_update_any_announcement"] or \
#                    permissions["may_update_own_content"] and user_owns_resource()
#
#     def check_role_permissions():
#         if permission_type in ("CREATE", "READ", "UPDATE", "DELETE"):
#             return permissions["may_crud_roles"]
#
#     def check_file_permissions():
#         if permission_type == "READ":
#             return user_owns_resource(resource_id)
#         if permission_type in ("CREATE", "READ", "DELETE"):
#             return permissions["may_update_any_file"] or \
#                 permissions["may_update_file_in_own_project"] and user_owns_resource(resource_id)
#
#     resource_checks = {
#         "project": check_project_permissions,
#         "user": check_user_permissions,
#         "announcement": check_announcement_permissions,
#         "reply": check_reply_permissions,
#         "role": check_role_permissions(),
#         "file": check_file_permissions
#     }
#     try:
#         resource_checks[resource_type]()
#     except:
#         abort(500, "Internal Server Error")
#     abort(500, "Internal Server Error")
