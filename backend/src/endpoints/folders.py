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
    requested_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + folder_path
    list_of_files = []
    if os.path.exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        for path in paths_in_requested_path:
            if os.path.isdir(requested_path + "/" + path):
                list_of_files.append(path)
    return list_of_files


# POST /projects/{project_id}/folders
@check_permissions(Projects.may_cud_files)
def create_dir(project_id):
    try:
        requested_path = connexion.request.values.get('path')
        requested_path = unquote(requested_path)
        current_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + requested_path
        new_dir_name = connexion.request.json['name']
        new_dir_name = fs_service.get_secure_name(new_dir_name)

        new_dir_path = fs_service.get_unique_dir_path(new_dir_name, current_path, 0)
        # fs_service.create_directory(new_dir_path) RECURSIVE
        os.makedirs(new_dir_path)
        return response("Map aangemaakt", 200)
    except KeyError as e:
        return response("Het verzoek aan de server miste belangrijke informatie; neem contact op met de beheerder!", 400)
    except Exception as e:
        return response("Map kon niet worden aangemaakt", 500)

# PUT /projects/{project_id}/folders
@check_permissions(Projects.may_cud_files)
def update_dir(project_id):
    new_name = connexion.request.json['rename']  # can be any string
    path = connexion.request.json['from']  # must be put as /example/example
    path = unquote(path)
    path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + path

    target_path = connexion.request.json['to']
    target_path = unquote(target_path)
    target_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + target_path

    if len(new_name) == 0 or new_name == None:
        # must be put as /example/example
        return fs_service.move_dir(path, target_path)
    else:
        return fs_service.rename_dir(new_name, path)


# DELETE /projects/{project_id}/folders
@check_permissions(Projects.may_cud_files)
def delete_dir(project_id):
    path_to_delete = connexion.request.values.get('path')
    path_to_delete = unquote(path_to_delete)

    may_delete_contents = connexion.request.values.get('may_delete_contents')

    requested_path = config.FILE_STORAGE_ROOT + fs_service.get_project_path(project_id) + path_to_delete
    if fs_service.dir_exists(requested_path):
        if fs_service.delete_valid(requested_path):
            return response("Map verwijderd", 200)
        else:
            if len(os.listdir(requested_path)) > 0:
                if may_delete_contents != 'true':
                    return response("Map kon niet verwijderd worden; is de map niet leeg?", 409)
                else:
                    if fs_service.delete_elements_in_dir_valid(requested_path):
                        return response("Map (inclusief inhoud) verwijderd", 200)
                    else:
                        return response("Een deel van de inhoud van deze map kon niet verwijderd worden", 409)
    return response("Map kon niet verwijderd worden; bestaat de map nog?", 409)
