import mimetypes

from os.path import abspath
from flask import send_from_directory
from ..endpoints.folders import *


# GET /projects/{project_id}/files
@check_permissions(Projects.may_read)
def get_files_in_path(project_id):
    folder_path = connexion.request.values.get('path')
    requested_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + folder_path
    list_of_files = []
    if os.path.exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        for path in paths_in_requested_path:
            if not os.path.isdir(requested_path + "/" + path):
                list_of_files.append(path)

    return list_of_files


# POST /projects/{project_id}/files
@check_permissions(Projects.may_cud_files)
def request_to_upload_file(project_id):
    files = connexion.request.files
    current_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + "/" + unquote(
        connexion.request.values.get('path')
    )
    confirmation = connexion.request.values.get('conf')

    file = list(files.values())[0]
    return fs_service.upload_file(file, current_path, confirmation)


# PUT /projects/{project_id}/files
@check_permissions(Projects.may_cud_files)
def move_file(project_id):
    source_path = unquote(connexion.request.json['from'])
    file_name = source_path.rsplit('/', 1)[1]
    source_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + source_path

    target_path = unquote(connexion.request.json['to'])
    target_folder_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + target_path
    target_path = target_folder_path + "/" + file_name

    if fs_service.file_path_valid(source_path) and fs_service.dir_exists(target_folder_path):
        if (fs_service.file_move_valid(source_path, target_path)):
            return response("Bestand verplaatst", 200)

    return response("Bestand kon niet verplaatst worden", 400)


# GET /projects/{project_id}/file
#TODO schrijf permissie
@check_permissions(Projects.may_read_shared_files)
def download_file(project_id):
    requested_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + connexion.request.values.get('path')
    requested_path = unquote(requested_path)
    [path_in_folder, file_name] = requested_path.rsplit('/', 1)
    path_in_folder = abspath(path_in_folder)

    if fs_service.file_path_valid(requested_path):
        file_mimetype = mimetypes.guess_type(requested_path)[0]
        return send_from_directory(path_in_folder, filename=file_name, mimetype=file_mimetype, as_attachment=True)

    return response("Dit bestand lijkt niet (meer) te bestaan!", 400)


# PUT /projects/{project_id}/file
@check_permissions(Projects.may_cud_files)
def rename_file(project_id):
    requested_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + connexion.request.values.get('path')
    requested_path = unquote(requested_path)
    if fs_service.file_path_valid(requested_path):
        folder_path = requested_path.rsplit('/', 1)[0]
        new_name = fs_service.get_secure_file_name(connexion.request.json['name'])
        new_path = os.path.join(folder_path, new_name)
        if fs_service.file_rename_valid(abspath(requested_path), abspath(new_path)):
            return response("Bestandsnaam gewijzigd", 200)
    else:
        return response("Pad van bestand niet gevonden", 400)

    return response("Bestandsnaam wijzigen mislukt", 400)


# DELETE /projects/{project_id}/file
@check_permissions(Projects.may_cud_files)
def delete_file(project_id):
    requested_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + connexion.request.values.get('path')
    if fs_service.file_path_valid(requested_path):
        os.remove(requested_path)
        return response("Bestand verwijderd", 200)

    return response("Bestand kon niet verwijderd worden", 400)
