import os
import shutil
import src.config as config
from urllib.parse import unquote

import connexion
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from src.services.helper_functions import response
from src.services.permissions import Projects
from src.services.permissions.permissions import check_permissions


def dir_exists(path):
    return os.path.exists(path) and os.path.isdir(path)


def name_valid(path, new_name):
    return not dir_exists(os.path.join(path, new_name))


def move_valid(source_path, target_path, dir_path):
    if dir_exists(source_path) and dir_exists(target_path):
        return dir_exists(target_path + dir_path)
    return False


def delete_valid(folder_path):
    try:
        os.rmdir(folder_path)
        return True
    except:
        return False


def delete_elements_in_dir_valid(dir_path):
    try:
        shutil.rmtree(dir_path)
        return True
    except:
        return False


def get_project_path(project_id):
    return str(project_id)


def get_unique_dir_path(new_dir, current_path, count):
    current_path = unquote(current_path)
    path_to_check = current_path + "/" + new_dir
    if count == 0:
        if dir_exists(path_to_check):
            return get_unique_dir_path(new_dir, current_path, count + 1)
        return path_to_check
    else:
        if dir_exists(path_to_check + " (" + str(count) + ")"):
            return get_unique_dir_path(new_dir, current_path, count + 1)
        return path_to_check + " (" + str(count) + ")"


def get_secure_name(name):
    secure_folder_name = secure_filename(name)
    length_folder_name = len(secure_folder_name)
    if length_folder_name == 0:
        return "Nieuwe_Map"
    elif length_folder_name > config.MAX_DIR_NAME:
        return secure_folder_name[0:config.MAX_DIR_NAME]

    return secure_folder_name

@check_permissions(Projects.may_read_files)
def get_folders_in_path(project_id):
    folder_path = connexion.request.values.get('path')
    requested_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + folder_path
    list_of_files = []
    if os.path.exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        for path in paths_in_requested_path:
            if os.path.isdir(requested_path + "/" + path):
                list_of_files.append(path)
    return list_of_files

def move_dir(source_path, target_path):
    dir_path = "/" + source_path.rsplit("/", 1)[1]
    if move_valid(source_path, target_path, dir_path):
        try:
            shutil.move(source_path, target_path, copy_function=shutil.copytree)
            if dir_exists(target_path + dir_path):
                return response("Successfully moved folder", 200)
        except:
            return response("Kon de folder niet verplaatsen", 400)
    return response("Kon de folder niet verplaatsen", 400)

def rename_dir(new_name, path):
    new_name = get_secure_name(new_name)
    path = unquote(path)
    if dir_exists(path):
        sub_path = path.rsplit("/", 1)[0]
        if name_valid(sub_path, new_name):
            new_path = sub_path + "/" + new_name
            os.rename(path, new_path)
            return response("Foldernaam gewijzigd", 200)
    return response("Kon foldernaam niet wijzigen", 400)

@check_permissions(Projects.may_cud_files)
def create_dir(project_id):
    try:
        requested_path = connexion.request.values.get('path')
        requested_path = unquote(requested_path)
        current_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + requested_path
        new_dir_name = connexion.request.json['name']
        new_dir_name = get_secure_name(new_dir_name)

        new_dir_path = get_unique_dir_path(new_dir_name, current_path, 0)
        os.mkdir(new_dir_path)
        return response("Folder aangemaakt", 200)
    except KeyError as e:
        return response("Foute aanvraag", 400)
    except Exception as e:
        return response("Kon geen folder aanmaken", 400)

@check_permissions(Projects.may_cud_files)
def delete_dir(project_id):
    path_to_delete = connexion.request.values.get('path')
    path_to_delete = unquote(path_to_delete)

    confirmation = connexion.request.values.get('conf')

    requested_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + path_to_delete
    if dir_exists(requested_path):
        if delete_valid(requested_path):
            return response("Folder verwijderd", 200)
        else:
            if len(os.listdir(requested_path)) > 0:
                if confirmation != 'true':
                    return response("Folder niet verwijderd, er zitten elenenten in", 409)
                else:
                    if delete_elements_in_dir_valid(requested_path):
                        return response("Folder met elementen verwijderd", 200)
                    else:
                        return response("Element in de folder konden niet verwijderd worden", 400)
    return response("Folder kon niet verwijderd worden, herlaad de pagina", 400)

@check_permissions(Projects.may_cud_files)
def update_dir(project_id):
    new_name = connexion.request.json['rename']  # can be any string
    path = connexion.request.json['from']  # must be put as /example/example
    path = unquote(path)
    path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + path

    target_path = connexion.request.json['to']
    target_path = unquote(target_path)
    target_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + target_path

    if len(new_name) == 0 or new_name == None:
        # must be put as /example/example
        return move_dir(path, target_path)
    else:
        return rename_dir(new_name, path)


if not dir_exists(config.FILE_STORAGE_ROOT):
    if not dir_exists("../filestorage"):
        os.mkdir("../filestorage");
    if not dir_exists("../filestorage/root"):
        os.mkdir("../filestorage/root")
