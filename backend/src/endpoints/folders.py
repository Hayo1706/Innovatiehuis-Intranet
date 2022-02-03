import os
import connexion

import src.config as config
import src.services.filestorage_service as fs_service
from urllib.parse import unquote
from src.services.helper_functions import response
from src.services.permissions import Projects
from src.services.permissions.permissions import check_permissions


# GET /projects/{project_id}/folders
@check_permissions(Projects.may_read_files)
def get_folders_in_path(project_id):
    folder_path = connexion.request.values.get('path')
    requested_path = fs_service.pathify(config.FILE_STORAGE_ROOT, fs_service.get_project_path(project_id), folder_path)
    list_of_files = []
    if os.path.exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        for path in paths_in_requested_path:
            if os.path.isdir(fs_service.pathify(requested_path, path)):
                list_of_files.append(path)
    return list_of_files


# POST /projects/{project_id}/folders
@check_permissions(Projects.may_cud_files)
def create_folder(project_id):
    try:
        requested_path = unquote(connexion.request.values.get('path'))
        current_path = fs_service.pathify(config.FILE_STORAGE_ROOT, fs_service.get_project_path(project_id), requested_path)
        new_folder_name = fs_service.sanitize_name(connexion.request.json['name'], "folder")

        new_dir_path = fs_service.get_unique_folder_path(fs_service.pathify(current_path, new_folder_name), 0)
        os.makedirs(new_dir_path)
        return response("Map aangemaakt", 200)
    except KeyError as e:
        return response("Het verzoek aan de server miste belangrijke informatie; neem contact op met de beheerder!", 400)
    except Exception as e:
        return response("Map kon niet worden aangemaakt", 500)


# PUT /projects/{project_id}/folders
@check_permissions(Projects.may_cud_files)
def update_folder(project_id):
    new_name = connexion.request.json['rename']  # can be any string
    path = unquote(connexion.request.json['from'])  # must be structured like: /example/example
    path = fs_service.pathify(config.FILE_STORAGE_ROOT, fs_service.get_project_path(project_id), path)

    if len(new_name) == 0 or new_name == None:
        target_path = unquote(connexion.request.json['to'])
        target_path = fs_service.pathify(config.FILE_STORAGE_ROOT, fs_service.get_project_path(project_id), target_path)
        return fs_service.move_folder(path, target_path)
    else:
        folder_location = path.rsplit("/", 1)[0]
        new_path = fs_service.pathify(folder_location, new_name)
        return fs_service.move_folder(path, new_path)


# DELETE /projects/{project_id}/folders
@check_permissions(Projects.may_cud_files)
def delete_folder(project_id):
    path_to_delete = unquote(connexion.request.values.get('path'))
    may_delete_contents = connexion.request.values.get('may_delete_contents')

    requested_path = fs_service.pathify(config.FILE_STORAGE_ROOT, fs_service.get_project_path(project_id), path_to_delete)
    if not fs_service.dir_exists(requested_path):
        return response("Map kon niet verwijderd worden; bestaat de map nog?", 409)
    if len(os.listdir(requested_path)) > 0:
        if may_delete_contents != 'true':
            return response(
                "Map kon niet verwijderd worden omdat er recent bestanden zijn toegevoegd; herlaad de pagina", 409)
        else:
            try:
                fs_service.delete_folder_contents(requested_path)
            except:
                return response("Een deel van de inhoud van deze map kon niet verwijderd worden", 409)
    if not fs_service.delete_valid(requested_path):
        return response(
            "Map kon niet verwijderd worden, waarschijnlijk omdat iemand anders ermee bezig is; herlaad de pagina", 409)
    return response("Map verwijderd", 200)

