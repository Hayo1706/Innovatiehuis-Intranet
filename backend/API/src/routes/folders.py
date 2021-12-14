import os
import json

from flask import Flask, render_template, request, send_file

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

def isFilePathValid(requested_path):
    requested_path = (root + requested_path)
    if path_exists(requested_path) and not os.path.isdir(requested_path):
        return True
    return False

def isDirUnique(new_dir, current_path, count):
    print(count)
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

deleteDir(root+"1", False)

#os.path.join("c:\\", "temp", "new folder") Joins zijn Safer nog naar kijken !