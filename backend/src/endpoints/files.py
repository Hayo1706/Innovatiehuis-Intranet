import mimetypes
from os.path import abspath

import src.config as config
import os
import json
import time

import connexion
from flask import Flask, request, send_file, send_from_directory
from ..endpoints.folders import *

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

def get_secure_file_name(filename):
    index_split_name = filename.rfind('.');
    file_type = filename[index_split_name::]
    file_name = filename[0: index_split_name].replace('.', '')

    secure_name = secure_filename(file_name)
    length_file_name = len(secure_name)

    if length_file_name == 0:
        return "New_File" + file_type
    elif length_file_name > config.MAX_FILE_NAME:
        return secure_name[0:config.MAX_FILE_NAME] + file_type

    return secure_name + file_type

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

def get_full_file_path(path):
    return config.FILE_STORAGE_ROOT + path

def file_exists(path):
    if path_exists(path):
        return True
    else:
        return False

def file_path_valid(requested_path):
    if path_exists(requested_path) and not os.path.isdir(requested_path):
        return True
    else:
        return False

def size_valid(file):
    if not os.fstat(file.fileno()).st_size > config.MAX_FILE_SIZE:
        return True
    else:
        return False

def file_move_valid(source_path, target_path):
    if not file_path_valid(target_path):
        try:
            shutil.move(source_path, target_path)
            return True
        except:
            return False
    return False

def file_replace_valid(file, file_path):
    while file_exists(file_path):
        try:
            os.remove(file_path)
        except:
            return False
    else:
        return file_save_valid(file, file_path)

def file_save_valid(file, file_path):
    try:
        file.save(file_path)
        return True
    except:
        return False


def delete_file(project_id):
    requested_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + connexion.request.values.get('path')
    if file_path_valid(requested_path):
        os.remove(requested_path)
        return response("Successfully deleted file", 200)

    return response("Failed to delete file", 400)

def request_to_upload_file(project_id):
    files = connexion.request.files
    current_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + "/" + unquote(connexion.request.values.get('path'))
    confirmation = connexion.request.values.get('conf')

    if len(files) > 0:
        file = list(files.values())[0]
        if size_valid(file):
            return upload_file(file, current_path, confirmation)
        else:
            print("Uploaded file is too big, maximum size of files is " + str(config.MAX_FILE_SIZE) + " bytes.")
            return response("Uploaded file is too big, maximum size of files is " + str(config.MAX_FILE_SIZE) + " bytes.", 406)

def upload_file(file, path, confirmation):
    if dir_exists(path):
        file_name = file.filename
        file_path = os.path.join(path, file_name)
        if file_path_valid(file_path):
            if confirmation == 'true':
                if file_replace_valid(file, file_path):
                    print("Succesfully replaced file")
                    return response("Succesfully replaced file", 200)
                else:
                    print("Failed to replace file")
                    return response("Failed to replace file", 424)
            elif confirmation == 'false':
                new_file_name = get_unique_file_name(get_secure_file_name(file_name), path, 0)
                new_file_path = os.path.join(path, new_file_name)
                if file_save_valid(file, new_file_path):
                    print("Succesfully uploaded file")
                    return response("Succesfully uploaded file", 200)
            else:
                print(file_name + " already exists would you like to replace it?")
                return response(file_name + " already exists would you like to replace it?", 409)
        else:
            file_name = get_secure_file_name(file_name)
            file_path = os.path.join(path, file_name)
            if file_save_valid(file, file_path):
                print("Succesfully uploaded file")
                return response("Successfully uploaded file", 200)
    return response("Failed to upload file", 424)

def download_file(project_id):
    requested_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + connexion.request.values.get('path')
    requested_path = unquote(requested_path)
    [path_in_folder, file_name] = requested_path.rsplit('/', 1)
    path_in_folder = abspath(path_in_folder)

    if file_path_valid(requested_path):
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

    if file_path_valid(source_path) and dir_exists(target_folder_path):
        if(file_move_valid(source_path, target_path)):
            print("Succesfully moved file to target folder")
            return response("Successfully moved file to target folder", 200)


    return response("Failed to move file", 400)

def rename_file(project_id):
    requested_path = config.FILE_STORAGE_ROOT + get_project_path(project_id) + connexion.request.values.get('path')
    requested_path = unquote(requested_path)
    if file_path_valid(requested_path):
        folder_path = requested_path.rsplit('/', 1)[0]
        new_name = get_secure_file_name(connexion.request.json['name'])
        new_path = os.path.join(folder_path, new_name)
        if file_rename_valid(abspath(requested_path), abspath(new_path)):
            print("Succesfully updated file name")
            return response("Successfully updated file name", 200)
        else:
            print("Failed to update file name")
            return response("Failed to update file name", 400)
    else:
        print("Original file path is invalid")
        return response("Original file path is invalid", 400)

    print("Failed to update filename")
    return response("Failed to update filename", 400)

def file_rename_valid(old_path, new_path):
    print(old_path)
    print(new_path)
    if old_path != new_path:
        try:
            os.rename(old_path, new_path)
            return True
        except:
            return False
    return False