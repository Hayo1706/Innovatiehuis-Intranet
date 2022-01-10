import mimetypes
from os.path import abspath

import src.config as config
import os
import json
import time

import connexion
from flask import Flask, request, send_file, send_from_directory
from ..endpoints.folders import *


def file_exists(path):
    if path_exists(path):
        return True
    else:
        return False


def get_full_file_path(path):
    return config.FILE_STORAGE_ROOT + path


def secure_file_name(filename):
    index_split_name = filename.rfind('.');
    file_type = filename[index_split_name::]
    file_name = filename[0: index_split_name]
    secure_name = secure_filename(file_name)

    #file_type in allowed_extentions, option
    if(len(secure_name) == 0):
        return "New File" + file_type
    return secure_name + file_type


def request_to_upload_file(project_id):
    files = connexion.request.files
    current_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + "/" + unquote(connexion.request.values.get('path'))
    confirmation = connexion.request.values.get('conf')

    for file in files.values():
        return upload_file(file, current_path, confirmation)


def upload_file(file, path, confirmation):
    if len(file.filename) > 0 and dir_exists(path):
        file_name = file.filename
        file_path = os.path.join(path, file_name)
        if file_exists(file_path):
            if confirmation == 'true':

                while file_exists(file_path):
                    try:
                        os.remove(file_path)
                    except:
                        return response("Failed to replace file", 400)
                else:
                   file.save(os.path.join(path, file_name))
                   return response("Succesfully replaced file", 200)

            elif confirmation == 'false':
                file_name = secure_file_name(file_name)
                new_file_name = get_unique_file_name(file_name, path, 0)
                file.save(os.path.join(path, new_file_name))
                return response("Succesfully uploaded file", 200)

            else:
                return response(file_name + " already exists would you like to replace it?", 409)

        else:
            file_name = secure_file_name(file_name)
            file.save(os.path.join(path, file_name))
            return response("Successfully uploaded file", 200)

    return response("Failed to upload file", 400)


def is_file_path_valid(requested_path):
    if path_exists(requested_path) and not os.path.isdir(requested_path):
        return True
    return False


def get_unique_file_name(file_name_type, current_path, count):
    index_split_name = file_name_type.rfind('.');
    file_name = file_name_type[0: index_split_name]
    file_type = file_name_type[index_split_name::]
    if count == 0:
        if file_exists(current_path + "/" + file_name + file_type):
            return get_unique_file_name(file_name_type, current_path, count + 1)
        return file_name + file_type
    else:
        if file_exists(current_path + "/" + file_name  + " (" + str(count) + ")" + file_type):
            return get_unique_file_name(file_name_type, current_path, count + 1)
        return file_name + " (" + str(count) + ")" + file_type


def get_files_in_path(project_id):
    folder_path = connexion.request.values.get('path')
    requested_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + folder_path
    list_of_files = []
    if path_exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        for path in paths_in_requested_path:
            if not os.path.isdir(requested_path + "/" + path):
                list_of_files.append(path)

    return list_of_files

def download_file(project_id):
    requested_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + connexion.request.values.get('path')
    requested_path = unquote(requested_path)
    [path_in_folder, file_name] = requested_path.rsplit('/', 1)
    path_in_folder = abspath(path_in_folder)

    if os.path.exists(requested_path):
        if is_file_path_valid(requested_path):
            print(requested_path)
            file_mimetype = mimetypes.guess_type(requested_path)[0]
            return send_from_directory(path_in_folder, filename=file_name, mimetype=file_mimetype, as_attachment=True)

    return response("Failed to download file", 400)


def move_file(project_id):
    source_path = unquote(connexion.request.json['from'])
    file_name = source_path.rsplit('/', 1)[1]
    source_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + source_path

    target_path = unquote(connexion.request.json['to'])
    target_folder_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + target_path
    target_path = target_folder_path + "/" + file_name

    if file_exists(source_path) and dir_exists(target_folder_path):
        if not file_exists(target_path):
            try:
                shutil.move(source_path, target_path)
                return response("Successfully moved file to target folder", 200)
            except:
                return response("Failed to move file", 400)

    return response("Failed to move file", 400)


def delete_file(project_id):
    requested_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + connexion.request.values.get('path')
    if is_file_path_valid(requested_path):
        os.remove(requested_path)
        return response("Successfully deleted file", 200)

    return response("Failed to delete file", 400)


def rename_file(project_id):
    requested_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + connexion.request.values.get('path')
    requested_path = unquote(requested_path)
    if is_file_path_valid(requested_path):
        folder_path = requested_path.rsplit('/', 1)[0]
        old_name = requested_path.rsplit('/', 1)[1]
        new_name = connexion.request.json['name']

        if old_name != new_name:
            new_name = get_unique_file_name(new_name, folder_path, 0)
            os.rename(folder_path + "/" + old_name, folder_path + "/" + new_name)
            return response("Successfully updated file name from: " + old_name + " to: " + new_name, 200)

        return response("New name is equal to old name", 400)

    return response("Original file path is invalid", 400)
