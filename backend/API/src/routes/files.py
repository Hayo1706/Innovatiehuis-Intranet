import os
import json

import connexion
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from backend.API.src.routes.folders import *

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

def uploadFiles():
    current_path = connexion.request.values.get('projectid')
    files = connexion.request.files.getlist('files')
    print(files)
    for file in files:
        upload_file(file, current_path)


def isFilePathValid(requested_path):
    requested_path = (root + requested_path)
    if path_exists(requested_path) and not os.path.isdir(requested_path):
        return True
    return False

def getUniqueFileName(file_name_type, current_path, count):
    index_split_name = file_name_type.rfind('.');
    file_name = file_name_type[0: index_split_name]
    file_type = file_name_type[index_split_name::]
    if count == 0:
        if file_exists(root + current_path + "/" + file_name + file_type):
            return getUniqueFileName(file_name_type, current_path, count + 1)
        return file_name + file_type
    else:
        if file_exists(root + current_path + "/" + file_name  + " (" + str(count) + ")" + file_type):
            return getUniqueFileName(file_name_type, current_path, count + 1)
        return file_name + " (" + str(count) + ")" + file_type

def upload_file(file, current_path):
    if len(file.filename) > 0:
        file_name = secureFileName(file.filename)
        new_file_name = getUniqueFileName(file_name, current_path, 0)
        print(root + current_path)
        if not dir_exists(root + current_path):
            print("File upload failed, directory doesn't exist")
            return None
        else:
            file.save(os.path.join(root + current_path, new_file_name))  # this will save the file
            print("File uploaded succesfully")
            return 'file uploaded successfully'  # Display message after uploading
    return 'file upload failed, no file was selected'

def getFilesInPath(id):
    requested_path = root + id
    list_of_files = []
    if path_exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        for path in paths_in_requested_path:
            if not os.path.isdir(requested_path + "/" + path):
                list_of_files.append(path)
    return list_of_files




