import os
import shutil
from urllib.parse import unquote
from werkzeug.utils import secure_filename
import src.config as config
from ..services.helper_functions import *


def dir_exists(path):
    return os.path.exists(path) and os.path.isdir(path)


def file_exists(requested_path):
    return os.path.exists(requested_path) and not os.path.isdir(requested_path)


def move_valid(source_path, target_path, dir_path):
    print(source_path, target_path, dir_path)
    return dir_exists(source_path) and dir_exists(target_path) and not dir_exists(target_path + dir_path)


def delete_valid(folder_path):
    try:
        shutil.rmtree(folder_path)
        return True
    except:
        return False


def delete_folder_contents(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            move_file_to_archive(pathify(root, name), remove_references=True)


def get_project_path(project_id, version=None):
    if (version == "archive"):
        return str(project_id) + "archive"
    else:
        return str(project_id)


# This function adds a (1), (2), (3)... to the folder name if a folder with the same name already exists
def get_unique_folder_path(path_to_check, count):
    if count == 0:
        if dir_exists(path_to_check):
            return get_unique_folder_path(path_to_check, count + 1)
        return path_to_check
    else:
        if dir_exists(path_to_check + " (" + str(count) + ")"):
            return get_unique_folder_path(path_to_check, count + 1)
        return path_to_check + " (" + str(count) + ")"


# This function adds a (1), (2), (3)... to the filename if a file with the same name already exists
def get_unique_file_name(file_name_with_extension, current_path, count):
    index_split_name = file_name_with_extension.rfind('.')
    file_name = file_name_with_extension[0: index_split_name]
    file_extension = file_name_with_extension[index_split_name::]
    if count == 0:
        if os.path.exists(pathify(current_path, file_name + file_extension)):
            return get_unique_file_name(file_name_with_extension, current_path, count + 1)
        return file_name + file_extension
    else:
        if os.path.exists(pathify(current_path, file_name + " (" + str(count) + ")" + file_extension)):
            return get_unique_file_name(file_name_with_extension, current_path, count + 1)
        return file_name + " (" + str(count) + ")" + file_extension


def sanitize_name(name, object_type):
    file_extension = ""
    if object_type == "file":
        split_index = name.rfind('.')
        file_extension = name[split_index::]
        name = name[0: split_index].replace('.', '')

    name = secure_filename(name)
    name_length = len(name)
    if name_length == 0:
        return "Nieuw bestand" + file_extension if object_type == "file" else "Nieuwe map"
    if name_length > config.MAX_NAME_LENGTH:
        return name[0:config.MAX_NAME_LENGTH] + file_extension
    return name + file_extension


def move_folder(source_path, target_path):
    folder_name = source_path.rsplit("/", 1)[1]
    if dir_exists(target_path):
        if move_valid(source_path, target_path, folder_name):
            try:
                for root, dirs, files in os.walk(source_path, topdown=True):
                    subdir = root.replace(source_path, "")
                    for dir_to_move in dirs:
                        path = pathify(target_path, folder_name, subdir, dir_to_move)
                        if dir_exists(path):
                            path = get_unique_folder_path(path, 0)
                        os.makedirs(path)
                    for file_to_move in files:
                        file_name = get_unique_file_name(file_to_move, pathify(target_path, folder_name, subdir), 0)
                        move_file(pathify(root, file_name), pathify(target_path, folder_name, subdir), update_references=True)
                shutil.rmtree(source_path)
                return response("Map gewijzigd", 200)
            except:
                return response(
                    "Er ging iets mis tijdens de operatie; controleer of er bestanden zijn achtergebleven in de oorspronkelijke map!",
                    500)
        else:
            return response(
                "De map of locatie bestaat niet meer, of er is al een map met dezelfde naam op de gekozen locatie.", 400)
    else:
        os.makedirs(pathify(target_path))
        if move_valid(source_path, target_path, folder_name):
            try:
                for root, dirs, files in os.walk(source_path, topdown=True):
                    subdir = root.replace(source_path, "")
                    for dir_to_move in dirs:
                        path = pathify(target_path, folder_name, subdir, dir_to_move)
                        print(path)
                        if dir_exists(path):
                            path = get_unique_folder_path(path, 0)
                        os.makedirs(path)
                    for file_to_move in files:
                        file_name = get_unique_file_name(file_to_move, pathify(target_path, folder_name, subdir), 0)
                        move_file(pathify(root, file_name), pathify(target_path, folder_name, subdir), update_references=True)
                shutil.rmtree(source_path)
                return response("Map gewijzigd", 200)
            except:
                return response(
                    "Er ging iets mis tijdens de operatie; controleer of er bestanden zijn achtergebleven in de oorspronkelijke map!",
                    500)
        else:
            return response(
                "De map of locatie bestaat niet meer, of er is al een map met dezelfde naam op de gekozen locatie.", 400)



def switch_files(path1, path2):
    directory1, file_name1 = path1.rsplit('/', 1)
    directory2, file_name2 = path2.rsplit('/', 1)
    completed_step1 = False
    completed_step2 = False
    try:
        move_file(path1, config.FILE_STORAGE_ROOT)
        completed_step1 = True
        move_file(path2, directory1)
        completed_step2 = True
        move_file(pathify(config.FILE_STORAGE_ROOT, file_name1), directory2)
    except:
        if completed_step2:
            move_file(path1, directory2)
        if completed_step1:
            move_file(pathify(config.FILE_STORAGE_ROOT, file_name1), directory1)
        return False
    return True


def update_shared_files_entries(project_id, path_to_replace, new_path):
    data = query("SELECT childid, shared_files FROM projects_have_parents WHERE parentid = %(projectid)s",
                 {'projectid': project_id})
    for entry in data:
        if entry["shared_files"] is not None:
            shared_files_list = entry["shared_files"].split(' ')
            updated_list = [new_path if file == path_to_replace else file for file in shared_files_list]
            culled_list = [file for file in updated_list if file != '']
            new_shared_files_string = ' '.join(culled_list)
            if new_shared_files_string == "":
                new_shared_files_string = None
            query_update("UPDATE projects_have_parents SET shared_files = %(shared_files)s WHERE parentid = %(projectid)s "
                         "AND childid = %(childid)s",
                         {'shared_files': new_shared_files_string, 'projectid': project_id, 'childid': entry['childid']})


def move_file_to_archive(source_path, remove_references=False):
    sub_path = source_path.replace(config.FILE_STORAGE_ROOT, "")
    index = sub_path.find("/")

    if remove_references:
        update_shared_files_entries(sub_path[:index], sub_path[index:], "")

    archive_path = pathify(get_project_path(int(sub_path[:index]), "archive"), sub_path[index:])
    target_path = pathify(config.FILE_STORAGE_ROOT, archive_path)
    if file_exists(target_path):
        os.remove(target_path)
    target_folder = target_path.rsplit('/', 1)[0]
    move_file(source_path, target_folder)


def move_file(source_path, target_path, update_references=False):
    if not dir_exists(target_path):
        os.makedirs(target_path)

    file_name = source_path.rsplit('/', 1)[1]
    if update_references:
        sub_path = source_path.replace(config.FILE_STORAGE_ROOT, "")
        target_sub_path = target_path.replace(config.FILE_STORAGE_ROOT, "")
        index = sub_path.find("/")
        update_shared_files_entries(sub_path[:index], sub_path[index:], pathify(target_sub_path[index:], file_name))

    shutil.move(source_path, target_path)


def file_replace_valid(file, file_path):
    try:
        move_file_to_archive(file_path)
    except:
        return False
    return file_save_valid(file, file_path)


def file_save_valid(file, file_path):
    try:
        file.save(file_path)
        return True
    except:
        return False


def upload_file(file, full_path, may_overwrite):
    if not dir_exists(full_path):
        os.makedirs(full_path)
    file_name = sanitize_name(file.filename, "file")
    file_type = file_name.split('.')[1]
    file_path = pathify(full_path, file_name)
    if file_type.lower() in config.FILE_TYPE_BLACKLIST:
        return response(f"Bestand {file_name} is van een verboden bestandstype: "
                        f"{str(config.FILE_TYPE_BLACKLIST)}", 406)
    if os.fstat(file.fileno()).st_size > config.MAX_FILE_SIZE:
        return (f"Bestand {file_name} is te groot, de maximaal toegestane bestandsomvang is "
                f"{str(config.MAX_FILE_SIZE/1000/1000)}MB", 406)
    if file_exists(file_path):
        # REPLACE FILE?

        if may_overwrite == 'true':
            if not file_replace_valid(file, file_path):
                return response(f"Er ging iets fout bij het overschrijven van {file_name}", 424)
            return response("Bestand vervangen", 200)
        elif may_overwrite == 'false':
            numbered_file_name = get_unique_file_name(file_name, full_path, 0)
            numbered_file_path = pathify(full_path, numbered_file_name)
            if not file_save_valid(file, numbered_file_path):
                return response(f"Er ging iets fout bij het uploaden van {numbered_file_name}", 424)
            return response("Bestand geüpload", 200)
        else:
            return response("Er bestaat al een bestand genaamd " + file_name + " wil je deze vervangen?", 409)
    if not file_save_valid(file, file_path):
        return response(f"Er ging iets fout bij het uploaden van {file_name}", 424)

    return response("Bestand geüpload!", 200)


def file_rename_valid(file_path, new_name):
    directory, old_name = file_path.rsplit('/', 1)
    try:
        os.rename(file_path, pathify(directory, new_name))
        return True
    except:
        return False


def pathify(*paths):
    return "/".join([path.replace("\\", "/").strip("/") for path in paths if path.replace("\\", "/").strip("/") != ""])
