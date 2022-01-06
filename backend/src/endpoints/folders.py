import os
import shutil
import json
from urllib.parse import unquote

import connexion
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from src.services.helper_functions import response

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

def getFoldersInPath(project_id):
    folder_path = connexion.request.values.get('path')
    requested_path = root + getProjectPath(project_id) + folder_path
    list_of_files = []
    if path_exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        for path in paths_in_requested_path:
            if os.path.isdir(requested_path + "/" + path):
                list_of_files.append(path)
    return list_of_files

def getUniqueDirPath(new_dir, current_path, count):
    current_path = unquote(current_path)
    path_to_check = current_path + "/" + new_dir
    if count == 0:
        if dir_exists(path_to_check):
            return getUniqueDirPath(new_dir, current_path, count + 1)
        return path_to_check
    else:
        if dir_exists(path_to_check  + " (" + str(count) + ")"):
            return getUniqueDirPath(new_dir, current_path, count + 1)
        return path_to_check + " (" + str(count) + ")"

def checkFolderNameValid(path, new_name):
    if dir_exists(path + "/" + new_name):
        return False
    return True



def checkFolderPutRequest(project_id):
    new_name = connexion.request.json['rename'] # can be any string
    path = connexion.request.json['from'] # must be put as /example/example
    path = unquote(path)
    path = root + getProjectPath(project_id) + path

    target_path = connexion.request.json['to']
    target_path = unquote(target_path)
    target_path = root + getProjectPath(project_id) + target_path

    if len(new_name) == 0 or new_name == None:
         # must be put as /example/example

        moveDirFromRequest(path, target_path)
    else:
        changeFolderName(new_name, path)


def changeFolderName(new_name, path):
    new_name = secureFolderName(new_name)
    path = unquote(path)

    if dir_exists(path):
        sub_path = path.rsplit("/", 1)[0]

        if checkFolderNameValid(sub_path, new_name):
            new_path = sub_path + "/" + new_name
            os.rename(path, new_path)
            return response("Succesfully renamed folder", 200)

        return response("Failed to rename folder", 400)

    else:

        return response("Failed to rename folder", 400)

def moveDirFromRequest(source_path, target_path):
    dir_path = "/" + source_path.rsplit("/", 1)[1] #this is the path of the directory that's going to move, required to check later if this actually happend or already exists.
    if dir_exists(source_path) and dir_exists(target_path):
        if dir_exists(target_path + dir_path):
            print("Failed to move folder, there is a folder with the same name in target directory")
            return response("Failed to move folder, there is a folder with the same name in target directory", 400)
        else:
            try:
                shutil.move(source_path, target_path, copy_function = shutil.copytree)
                if dir_exists(target_path + dir_path):
                    return response("Succesfully moved folder", 200)
                else:
                    return response("Something went wrong, please try again", 400)
            except:
                print("Failed to move folder")
                return response("Failed to move folder", 400)

        return response("Succesfully move folder", 200)

    return response("Failed to moved folder", 400)


def getProjectPath(project_id):
    return str(project_id)


def isDirMoveValid(from_path, to_path):

    return

def createDirFromRequest(project_id):
    requested_path = connexion.request.values.get('path')
    requested_path = unquote(requested_path)
    current_path = root + getProjectPath(project_id) + requested_path

    new_dir_name = connexion.request.json['name']
    new_dir_name = secureFolderName(new_dir_name)

    new_dir_path = getUniqueDirPath(new_dir_name, current_path, 0)

    if new_dir_path == None or new_dir_name == None:
        print("Failed to create new folder")
        return response("Failed to create new folder", 400)

    try:
        os.mkdir(new_dir_path)
        print("Succesfully created new folder")
        return response("Succesfully created new folder", 200)
    except:
        print("Failed to created new folder")
        return response("Failed to created new folder", 400)


def deleteDir(project_id):
    path_to_delete = connexion.request.values.get('path')
    path_to_delete = unquote(path_to_delete)

    confirmation = connexion.request.values.get('conf')

    requested_path = root + getProjectPath(project_id) + path_to_delete
    if dir_exists(requested_path):
        if len(os.listdir(requested_path)) > 0:
            if confirmation != 'true':
                return response("An error occured when trying to delete folder, there are folders inside", 409)
            else:
                deleteElementsInDir(requested_path)
        else:
            removeFolder(requested_path)
    else:
        print("Folder could not be deleted, please refresh.")
        return response("Folder could not be deleted, please refresh.", 400)

def removeFolder(folder_path):
    try:
        os.rmdir(folder_path)
        print("Succesfully deleted folder")
        return response("Succesfully deleted folder", 200)
    except:
        print("An error occured when trying to delete folder, there are folders inside")
        return response("An error occured when trying to delete folder, there are folders inside", 409)

def deleteElementsInDir(dir_path):
    try:
        shutil.rmtree(dir_path)
        print("Succesfully deleted folder")
        return response("Succesfully deleted folder", 200)
    except:
        print("An error occured when trying to delete elements in folder")
        return response("An error occured when trying to delete elements in folder", 400)

def secureFolderName(file_name):
    secure_name = secure_filename(file_name)
    if(len(secure_name) == 0):
        return "Nieuwe_Map"
    return secure_name

# TODO os.path.join("c:\\", "temp", "new folder") Joins zijn Safer nog naar kijken !
if not dir_exists(root):
    if not dir_exists("../../filestorage"):
        os.mkdir("../../filestorage");
    if not dir_exists("../../filestorage/root"):
        os.mkdir("../../filestorage/root")

