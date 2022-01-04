import mimetypes
import os
import json

import connexion
from flask import Flask, request, send_file, send_from_directory
from ..endpoints.folders import *

root = '../../../filestorage/root/'


def file_exists(path):
    if path_exists(path):
        return True
    else:
        return False


def getFullFilePath(path):
    return root + path


def secureFileName(filename):
    index_split_name = filename.rfind('.');
    file_type = filename[index_split_name::]
    file_name = filename[0: index_split_name]
    secure_name = secure_filename(file_name)

    #file_type in allowed_extentions, option
    if(len(secure_name) == 0):
        return "New File" + file_type
    return secure_name + file_type


def uploadFiles(project_id):
    files = connexion.request.files
    current_path = root + getProjectPath(project_id) + "/" + connexion.request.values.get('path')

    for k, v in files.items():
        upload_file(v, current_path)

    return response('file(s) uploaded successfully', 200)


def isFilePathValid(requested_path):
    if path_exists(requested_path) and not os.path.isdir(requested_path):
        return True
    return False


def getUniqueFileName(file_name_type, current_path, count):
    index_split_name = file_name_type.rfind('.');
    file_name = file_name_type[0: index_split_name]
    file_type = file_name_type[index_split_name::]
    if count == 0:
        if file_exists(current_path + "/" + file_name + file_type):
            return getUniqueFileName(file_name_type, current_path, count + 1)
        return file_name + file_type
    else:
        if file_exists(current_path + "/" + file_name  + " (" + str(count) + ")" + file_type):
            return getUniqueFileName(file_name_type, current_path, count + 1)
        return file_name + " (" + str(count) + ")" + file_type


def upload_file(file, path):
    if len(file.filename) > 0:
        file_name = secureFileName(file.filename)
        new_file_name = getUniqueFileName(file_name, path, 0)
        if not dir_exists(path):
            return response("File upload failed, directory doesn't exist", 400)
        else:
            file.save(os.path.join(path, new_file_name))  # this will save the file
            return response('file uploaded successfully', 200)  # Display message after uploading
    return response('file upload failed, no file was selected', 400)

def getFilesInPath(project_id):
    folder_path = connexion.request.values.get('path')
    requested_path = root + getProjectPath(project_id) + folder_path
    list_of_files = []
    if path_exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        for path in paths_in_requested_path:
            if not os.path.isdir(requested_path + "/" + path):
                list_of_files.append(path)

    return list_of_files

def moveFile(project_id):
    source_path = connexion.request.json['from']
    target_path = connexion.request.json['to']

    source_path = root + getProjectPath(project_id) + "/" + source_path
    target_path = root + getProjectPath(project_id) + "/" + target_path

    if isFilePathValid(getProjectPath(project_id) + "/" + source_path) and dir_exists(target_path):
        try:
            shutil.move(source_path, target_path)
        except:
            return response("Failed to move file", 400)

        return response("Succesfully moved file to target folder", 200)

    return response("Failed to move file", 400)


def downloadFile(project_id):
    requested_path = root + getProjectPath(project_id) + connexion.request.values.get('path')
    requested_path = unquote(requested_path)
    file_name = requested_path.rsplit('/', 1)[1]
    path_in_folder = requested_path.rsplit('/', 1)[0]
    if os.path.exists(requested_path):
        if isFilePathValid(requested_path):
            file_mimetype = mimetypes.guess_type(requested_path)[0]
            return send_from_directory(root + path_in_folder, filename=file_name, mimetype=file_mimetype, as_attachment=True)

def moveFile(project_id):
    source_path = unquote(connexion.request.json['from'])
    source_path = root + getProjectPath(project_id) + source_path
    file_name = source_path.rsplit('/', 1)[1]

    target_path = unquote(connexion.request.json['to'])
    target_folder_path = root + getProjectPath(project_id) + target_path
    target_path = target_folder_path + "/" + file_name

    print(source_path, target_path, target_folder_path)
    if file_exists(source_path) and dir_exists(target_folder_path):
        if not file_exists(target_path):
            shutil.move(source_path, target_path)
            return response("Succesfully moved file", 200)
    return response("Failed to move file", 400)




def deleteFile(project_id):
    requested_path = root + getProjectPath(project_id) + connexion.request.values.get('path')
    if isFilePathValid(requested_path):
        os.remove(requested_path)
        return response("Succesfully deleted file", 200)

    return response("Failed to delete file", 400)


def renameFile(project_id):
    requested_path = root + getProjectPath(project_id) + connexion.request.values.get('path')
    requested_path = unquote(requested_path)
    if isFilePathValid(requested_path):
        folder_path = requested_path.rsplit('/', 1)[0]
        old_name = requested_path.rsplit('/', 1)[1]
        new_name = connexion.request.json['name']

        if old_name != new_name:
            new_name = getUniqueFileName(new_name, folder_path, 0)
            os.rename(folder_path + "/" + old_name, folder_path + "/" + new_name)
            return response("Succesfully updated file name from: " + old_name + " to: " + new_name , 200)

        return response("New name is equal to old name", 400)

    return response("Original file path is invalid", 400)




