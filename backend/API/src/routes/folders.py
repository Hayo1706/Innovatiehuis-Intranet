import os
import json

import connexion
from flask import Flask, render_template, request, send_file
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

def checkValidRootProjectFolder(id):
    print("yes")
    requested_path = root + id
    if not dir_exists(requested_path):
        createDir(id, root)
    return True

def getRequestedPath(requested_path, type):
    requested_path = (root + requested_path)
    if path_exists(requested_path):
        paths_in_requested_path = os.listdir(requested_path)
        list_of_directories = []
        list_of_files = []
        for path in paths_in_requested_path:
            if os.path.isdir(requested_path + path):
                list_of_directories.append(path)
            else:
                list_of_files.append(path)

        if type == "file":
            return json.dumps(list_of_files)
        if type == "dir":
            return json.dumps(list_of_directories)

    return None

def isDirUnique(new_dir, current_path, count):
    if count == 0:
        if dir_exists(root + current_path + new_dir):
            return isDirUnique(new_dir, current_path, count + 1)
        return current_path + new_dir
    else:
        if dir_exists(root + current_path + new_dir  + " (" + str(count) + ")"):
            return isDirUnique(new_dir, current_path, count + 1)
        return current_path + new_dir + " (" + str(count) + ")"

def createDir(new_dir, current_path):
    new_dir_path = isDirUnique(new_dir, current_path, 0)
    os.mkdir(root + new_dir_path)
    return new_dir_path

def createDirFromRequest():
    projectid = connexion.request.values.get('projectid')
    path = connexion.request.values.get('path')
    new_dir_name = connexion.request.values.get('name')
    new_dir_path = isDirUnique(new_dir_name, projectid, 0)
    os.mkdir(root + new_dir_path)
    return new_dir_path



def deleteDir(dir_path, confirm):
    if dir_exists(dir_path):
        if not len(os.listdir(dir_path)) == 0:
            if confirm == True:
                os.rmdir(dir_path)
                return 0
            else:
                return 1 #There are files in the directory
        else:
            os.rmdir(dir_path)
            return 0
    else:
        return -1

if not dir_exists(root):
    if not dir_exists("../../../filestorage"):
        os.mkdir("../../../filestorage");
    if not dir_exists("../../../filestorage/root"):
        os.mkdir("../../../filestorage/root")




#os.path.join("c:\\", "temp", "new folder") Joins zijn Safer nog naar kijken !