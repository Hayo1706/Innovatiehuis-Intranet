import os
import shutil
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
    folder_path = connexion.request.values.get('path')
    if folder_path == id:
        requested_path = root + getProjectPath(id)
    else:
        requested_path = root + folder_path

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

def checkFolderNameValid(path, new_name):
    if dir_exists(path + "/" + new_name):
        return False
    return True



def checkFolderPutRequest(id):
    new_name = connexion.request.json['rename'] # can be any string
    source_path = connexion.request.json['from'] # must be put as /example/example

    source_path = root + getProjectPath(id) + source_path

    if len(new_name) == 0 or new_name == None:
        target_path = connexion.request.json['to'] # must be put as /example/example
        target_path = root + getProjectPath(id) + target_path
        moveDirFromRequest(id, source_path, target_path)
    else:
        changeFolderName(new_name, source_path)


def changeFolderName(new_name, source_path):
    print(new_name)
    print(source_path)
    new_name = secureFolderName(new_name)
    if dir_exists(source_path):
        sub_path = source_path.rsplit("/", 1)[0]

        if checkFolderNameValid(sub_path, new_name):
            new_path = sub_path + "/" + new_name
            os.rename(source_path, new_path)
            return make_response("Succesfully renamed folder", 200)

        return make_response("Failed to rename folder", 400)

    else:

        return make_response("Failed to rename folder", 400)

def moveDirFromRequest(id, source_path, target_path):
    print(source_path)
    if dir_exists(source_path) and dir_exists(target_path):
        try:
            shutil.move(source_path, target_path)
        except:
            return make_response("Failed to move folder", 400)

        return make_response("Succesfully move folder", 200)

    return make_response("Failed to moved folder", 400)


def getProjectPath(id):
    return str(id)


def isDirMoveValid(from_path, to_path):

    return

def createDirFromRequest(id):
    path_in_project = connexion.request.values.get('path')
    if path_in_project == "/":
        path_in_project = ""

    full_path = getProjectPath(id) + "/" + path_in_project

    new_dir_name = connexion.request.json['name']
    new_dir_name = secureFolderName(new_dir_name)

    new_dir_path = getUniqueDirPath(new_dir_name, full_path, 0)

    if full_path == None or new_dir_name == None:
        print("Failed to create new folder")
        return make_response("Failed to create new folder", 400)

    os.mkdir(root + new_dir_path)
    print("Succesfully created new folder")
    return make_response("Succesfully created new folder", 200)

def deleteDir(id):
    #TODO get root path of project by id
    root_path_project = getProjectPath(id) + "/"
    path_to_delete = connexion.request.values.get('path')
    if dir_exists(root + root_path_project + path_to_delete):
        os.rmdir(root + root_path_project + path_to_delete)
        print("Succesfully deleted folder")
        return make_response("Succesfully deleted folder", 200)
    else:
        print("Folder could not be deleted, please refresh.")
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
    if not dir_exists("../../filestorage"):
        os.mkdir("../../filestorage");
    if not dir_exists("../../filestorage/root"):
        os.mkdir("../../filestorage/root")

