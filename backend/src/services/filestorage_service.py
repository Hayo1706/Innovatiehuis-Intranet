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
    return dir_exists(source_path) and dir_exists(target_path) and not dir_exists(target_path + dir_path)


def delete_valid(folder_path):
    try:
        os.rmdir(folder_path)
        return True
    except:
        return False


def delete_elements_in_dir_valid(dir_path):
    try:
        shutil.rmtree(dir_path)
        return True
    except:
        return False


def get_project_path(project_id, version=None):
    if (version):
        return str(project_id) + "backup"
    else:
        return str(project_id)


def get_unique_dir_path(new_dir, current_path, count):
    current_path = unquote(current_path)
    path_to_check = current_path + "/" + new_dir
    if count == 0:
        if dir_exists(path_to_check):
            return get_unique_dir_path(new_dir, current_path, count + 1)
        return path_to_check
    else:
        if dir_exists(path_to_check + " (" + str(count) + ")"):
            return get_unique_dir_path(new_dir, current_path, count + 1)
        return path_to_check + " (" + str(count) + ")"


def get_secure_name(name):
    secure_folder_name = secure_filename(name)
    length_folder_name = len(secure_folder_name)
    if length_folder_name == 0:
        return "Nieuwe_Map"
    elif length_folder_name > config.MAX_DIR_NAME:
        return secure_folder_name[0:config.MAX_DIR_NAME]

    return secure_folder_name


def move_dir(source_path, target_path):
    dir_path = "/" + source_path.rsplit("/", 1)[1]
    if move_valid(source_path, target_path, dir_path):
        try:
            shutil.move(source_path, target_path, copy_function=shutil.copytree)
            if dir_exists(target_path + dir_path):
                return response("Successfully moved folder", 200)
        except:
            return response("Kon de folder niet verplaatsen", 400)
    return response("Kon de folder niet verplaatsen", 400)


def rename_dir(new_name, path):
    new_name = get_secure_name(new_name)
    path = unquote(path)
    if dir_exists(path):
        sub_path = path.rsplit("/", 1)[0]
        if not dir_exists(os.sep.join([path, new_name])):
            new_path = sub_path + "/" + new_name
            os.rename(path, new_path)
            return response("Foldernaam gewijzigd", 200)
    return response("Kon foldernaam niet wijzigen", 400)


# This function adds a (1), (2), (3)... to the filename if a file with the same name already exists
def get_unique_file_name(file_name_with_type, current_path, count):
    index_split_name = file_name_with_type.rfind('.')
    file_name = file_name_with_type[0: index_split_name]
    file_type = file_name_with_type[index_split_name::]
    if count == 0:
        if os.path.exists(current_path + "/" + file_name + file_type):
            return get_unique_file_name(file_name_with_type, current_path, count + 1)
        return file_name + file_type
    else:
        if os.path.exists(current_path + "/" + file_name + " (" + str(count) + ")" + file_type):
            return get_unique_file_name(file_name_with_type, current_path, count + 1)
        return file_name + " (" + str(count) + ")" + file_type


def sanitize_name(filename):
    index_split_name = filename.rfind('.');
    file_type = filename[index_split_name::]
    sanitized_name = filename[0: index_split_name].replace('.', '')

    sanitized_name = secure_filename(sanitized_name)
    length_file_name = len(sanitized_name)

    if length_file_name == 0:
        return "New_File" + file_type
    elif length_file_name > config.MAX_FILE_NAME:
        return sanitized_name[0:config.MAX_FILE_NAME] + file_type

    return sanitized_name + file_type


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
        move_file(os.sep.join([config.FILE_STORAGE_ROOT, file_name1]), directory2)
    except:
        if completed_step2:
            move_file(path1, directory2)
        if completed_step1:
            move_file(os.sep.join([config.FILE_STORAGE_ROOT, file_name1]), directory1)
        return False
    else:
        return True


def update_shared_files_entries(project_id, path_to_replace, new_path):
    data = query("SELECT childid, shared_files FROM projects_have_parents WHERE parentid = %(projectid)s",
                 {'projectid': project_id})
    for entry in data:
        shared_files_list = entry["shared_files"].split(' ')
        updated_list = [new_path if file == path_to_replace else file for file in shared_files_list]
        culled_list = [file for file in updated_list if file != '']
        new_shared_files_string = ' '.join(culled_list)
        query_update("UPDATE projects_have_parents SET shared_files = %(shared_files)s WHERE parentid = %(projectid)s "
                     "AND childid = %(childid)s",
                     {'shared_files': new_shared_files_string, 'projectid': project_id, 'childid': entry['childid']})


def move_file_to_backup(source_path):
    sub_path = source_path.replace(config.FILE_STORAGE_ROOT, "")
    index = sub_path.find("/")
    backup_path = sub_path[:index] + "backup" + sub_path[index:]
    target_path = os.sep.join([config.FILE_STORAGE_ROOT, backup_path])
    if file_exists(target_path):
        os.remove(target_path)
    target_folder = target_path.rsplit('/', 1)[0]
    move_file(source_path, target_folder)


def move_file(source_path, target_path):
    if not dir_exists(target_path):
        os.makedirs(target_path)
    shutil.move(source_path, target_path)


def file_replace_valid(file, file_path):
    try:
        move_file_to_backup(file_path)
    except:
        return False
    return file_save_valid(file, file_path)


def file_save_valid(file, file_path):
    try:
        file.save(file_path)
        return True
    except:
        return False


def upload_file(file, path, may_overwrite):
    if not dir_exists(path):
        os.makedirs(path)
    file_name = sanitize_name(file.filename)
    file_type = file_name.split('.')[1]
    file_path = os.sep.join([path, file_name])
    if file_type.lower() not in config.ALLOWED_FILE_TYPES:
        return response(f"Bestand {file_name} is van een verboden bestandstype, de toegestaande bestandstypes zijn: "
                        f"{str(config.ALLOWED_FILE_TYPES)}", 406)
    if os.fstat(file.fileno()).st_size > config.MAX_FILE_SIZE:
        return (f"Bestand {file_name} is te groot, de maximaal toegestane bestandsomvang is "
                f"{str(config.MAX_FILE_SIZE/1000/1000)}MB", 406)
    if file_exists(file_path):
        # REPLACE FILE
        if may_overwrite:
            if not file_replace_valid(file, file_path):
                return response(f"Er ging iets fout bij het overschrijven van {file_name}", 424)
            return response("Bestand vervangen", 200)
        else:
            numbered_file_name = get_unique_file_name(file_name, path, 0)
            numbered_file_path = os.sep.join([path, numbered_file_name])
            if not file_save_valid(file, numbered_file_path):
                return response(f"Er ging iets fout bij het uploaden van {numbered_file_name}", 424)
            return response("Bestand geüpload", 200)

    # SAVE NEW FILE
    if not file_save_valid(file, file_path):
        return response(f"Er ging iets fout bij het uploaden van {file_name}", 424)

    return response("Bestand geüpload!", 200)




def file_rename_valid(file_path, new_name):
    directory, old_name = file_path.rsplit('/', 1)
    try:
        os.rename(file_path, os.sep.join([directory, new_name]))
        return True
    except:
        return False