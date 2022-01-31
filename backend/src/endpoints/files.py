import mimetypes
import shutil

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
            if not os.path.isdir(os.sep.join([requested_path, path])):
                list_of_files.append(path)
    return list_of_files


# POST /projects/{project_id}/files
@check_permissions(Projects.may_cud_files)
def request_to_upload_file(project_id):
    current_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + "/" + unquote(
        connexion.request.values.get('path')
    )
    may_overwrite = connexion.request.values.get('may_overwrite')

    file = list(connexion.request.files.values())[0]
    return fs_service.upload_file(file, current_path, may_overwrite)


# PUT /projects/{project_id}/files
@check_permissions(Projects.may_cud_files)
def move_file(project_id):
    source_path = unquote(connexion.request.json['from'])
    source_path_full = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + source_path
    backup_path_full = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id, "backup") + source_path

    target_path = unquote(connexion.request.json['to'])
    target_folder = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + target_path
    backup_target_folder = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id, "backup") + target_path

    if not fs_service.file_exists(source_path_full):
        return response("Verplaatsen mislukt - Het te verplaatsen bestand kon niet worden gevonden!", 404)
    if not fs_service.dir_exists(target_folder):
        return response("Verplaatsen mislukt - De doelmap kon niet worden gevonden!", 404)

    directory, file_name = source_path_full.rsplit('/', 1)
    if fs_service.file_exists(os.sep.join([target_folder, file_name])):
        return response(f"Verplaatsen mislukt - Er bestaat al een bestand met de naam {file_name} in de doelmap!", 400)

    # Check if a backup version exists, if so, move it accordingly
    if fs_service.file_exists(backup_path_full):
        fs_service.update_shared_files_entries(project_id, source_path, target_path)
        try:
            shutil.move(backup_path_full, backup_target_folder)
        except:
            return response("Bestand kon niet worden verplaatst", 500)

    try:
        shutil.move(source_path_full, target_folder)
        return response("Bestand verplaatst", 200)
    except:
        # Undo moving backup version
        try:
            backup_source_folder, file_name = backup_path_full.rsplit('/', 1)
            shutil.move(os.sep.join([backup_target_folder, file_name]), backup_source_folder)
            return response("Bestand kon niet worden verplaatst, en backup is verdwenen!", 500)
        except:
            return response("Bestand kon niet worden verplaatst", 500)


# PUT /projects/{project_id}/file
@check_permissions(Projects.may_cud_files)
def rename_file(project_id):
    new_name = fs_service.sanitize_name(connexion.request.json['name'])
    file_path = unquote(
        config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + connexion.request.values.get('path')
    )
    backup_file_path =  unquote(
        config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id, "backup") + connexion.request.values.get('path')
    )
    if not fs_service.file_exists(file_path):
        return response("Bestand niet gevonden", 404)
    # check if a version exists in backup, and if so, rename it
    if fs_service.file_exists(backup_file_path):
        if not fs_service.file_rename_valid(abspath(backup_file_path), new_name):
            return response("Bestandsnaam wijzigen mislukt", 500)
    if not fs_service.file_rename_valid(abspath(file_path), new_name):
        # undo renaming of backup version
        directory, old_name = abspath(backup_file_path).rsplit('/', 1)[1]
        if not fs_service.file_rename_valid(os.sep.join([directory, new_name]), old_name):
            return response("Bestandsnaam wijzigen mislukt, en backup kwijtgeraakt!", 500)
        return response("Bestandsnaam wijzigen mislukt", 500)
    return response("Bestandsnaam gewijzigd", 200)


# GET /projects/{project_id}/file
#TODO schrijf permissie
@check_permissions(Projects.may_read_shared_files)
def download_file(project_id):
    try:
        version = connexion.request.values.get('version')
    except KeyError:
        version = None

    if (version):
        requested_path = unquote(
            config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id, version) + connexion.request.values.get('path')
        )
        [subdir, file_name] = requested_path.rsplit('/', 1)
        subdir = abspath(subdir)

        if fs_service.file_exists(requested_path):
            file_mimetype = mimetypes.guess_type(requested_path)[0]
            return send_from_directory(subdir, filename=file_name, mimetype=file_mimetype, as_attachment=True)

        return response("Dit bestand lijkt niet (meer) te bestaan!", 404)
    else:
        requested_path = unquote(
            config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + connexion.request.values.get('path')
        )
        [path_in_folder, file_name] = requested_path.rsplit('/', 1)
        path_in_folder = abspath(path_in_folder)

        if fs_service.file_exists(requested_path):
            file_mimetype = mimetypes.guess_type(requested_path)[0]
            return send_from_directory(path_in_folder, filename=file_name, mimetype=file_mimetype, as_attachment=True)

        return response("Dit bestand lijkt niet (meer) te bestaan!", 404)


# DELETE /projects/{project_id}/file
@check_permissions(Projects.may_cud_files)
def delete_file(project_id):
    target_path = connexion.request.values.get('path')
    full_target_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + target_path
    if not fs_service.file_exists(full_target_path):
        return response("Bestand kon niet worden gevonden", 404)
    fs_service.update_shared_files_entries(project_id, target_path, new_path='')
    fs_service.move_file_to_backup(full_target_path)
    return response("Bestand verwijderd", 200)


# GET /projects/{project_id}/files/deleted
@check_permissions(Projects.may_read)
def read_deleted(project_id):
    project_root = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id)
    project_backup_root = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id, "backup")

    list_of_files = []
    for root, dirs, files in os.walk(project_backup_root):
        for name in files:
            relative_dir = root.replace(project_backup_root, "")
            if not fs_service.file_exists(os.sep.join([project_root, relative_dir, name])):
                list_of_files.append(os.sep.join([relative_dir, name]))
    return list_of_files


# PATCH /projects/{project_id}/file/restore
@check_permissions(Projects.may_cud_files)
def restore_file(project_id):
    path = connexion.request.values.get('path')
    project_root = os.sep.join([config.FILE_STORAGE_ROOT, project_id])

    active_path = os.sep.join([project_root, path])
    backup_path = os.sep.join([project_root, "backup", path])
    if not fs_service.file_exists(active_path):
        # restore a deleted file
        fs_service.move_file(backup_path, active_path)
    else:
        if not fs_service.file_exists(backup_path):
            return response("Er is geen eerdere versie van dit bestand beschikbaar", 404)
        # revert file to a previous version
        if fs_service.switch_files(active_path, backup_path):
            return response("Bestand is teruggezet naar de vorige versie", 200)
        else:
            return response("Er ging iets mis bij het ophalen van de vorige versie", 500)
