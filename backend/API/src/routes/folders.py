import os
import json

import connexion
from flask import Flask, render_template, request, send_file, make_response
from werkzeug.utils import secure_filename

root = '../../../filestorage/root/'

def path_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False

def dir_exists(path):
    if path_exists(path) and os.path.isdir(path):
        return True
    else:
        return False

def getFoldersInPath(id):
    requested_path = root + id
    list_of_files = []
    if path_exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        for path in paths_in_requested_path:
            if os.path.isdir(requested_path + "/" + path):
                list_of_files.append(path)
    print(list_of_files)
    return list_of_files

def getUniqueDirPath(new_dir, current_path, count):
    if count == 0:
        if dir_exists(root + current_path + new_dir):
            return getUniqueDirPath(new_dir, current_path, count + 1)
        return current_path + new_dir
    else:
        if dir_exists(root + current_path + new_dir  + " (" + str(count) + ")"):
            return getUniqueDirPath(new_dir, current_path, count + 1)
        return current_path + new_dir + " (" + str(count) + ")"

def createDirFromRequest(id):
    current_path = connexion.request.json['current_path']
    current_path = current_path.split("/project/")[1] + "/"

    new_dir_name = connexion.request.json['new_dir_name']
    new_dir_name = secureFolderName(new_dir_name)

    new_dir_path = getUniqueDirPath(new_dir_name, current_path, 0)

    if current_path == None or new_dir_name == None:
        return make_response("Failed to create new folder", 400)
    print(current_path)

    print(new_dir_path)
    os.mkdir(root + new_dir_path)
    return make_response("Succesfully created new folder", 200)

def deleteDir(id):
    current_path = connexion.request.json['current_path']
    current_path = current_path.split("/project/")[1] + "/"
    dir_name = connexion.request.json['dir_name']
    confirmation = connexion.request.json['confirmation']

    if dir_exists(root + current_path + dir_name) and confirmation == True:
        os.rmdir(root + current_path + dir_name)
        return make_response("Succesfully deleted folder", 200)
        print("yes")

    else:
        return make_response("Folder could not be deleted, please refresh.", 400)

def createDir(new_dir, current_path):
    new_dir_path = getUniqueDirPath(new_dir, current_path, 0)
    os.mkdir(root + new_dir_path)
    return new_dir_path

def secureFolderName(file_name):
    secure_name = secure_filename(file_name)
    if(len(secure_name) == 0):
        return "New Folder"
    return secure_name

# TODO os.path.join("c:\\", "temp", "new folder") Joins zijn Safer nog naar kijken !
if not dir_exists(root):
    if not dir_exists("../../../filestorage"):
        os.mkdir("../../../filestorage");
    if not dir_exists("../../../filestorage/root"):
        os.mkdir("../../../filestorage/root")

