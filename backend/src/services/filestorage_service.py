import os
import shutil
from urllib.parse import unquote
from werkzeug.utils import secure_filename
import src.config as config
from src.services.helper_functions import response


def dir_exists(path):
    return os.path.exists(path) and os.path.isdir(path)


def name_valid(path, new_name):
    return not dir_exists(os.path.join(path, new_name))


def move_valid(source_path, target_path, dir_path):
    if dir_exists(source_path) and dir_exists(target_path):
        return dir_exists(target_path + dir_path)
    return False


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


def get_project_path(project_id):
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
        if name_valid(sub_path, new_name):
            new_path = sub_path + "/" + new_name
            os.rename(path, new_path)
            return response("Foldernaam gewijzigd", 200)
    return response("Kon foldernaam niet wijzigen", 400)


def get_unique_file_name(file_name_type, current_path, count):
    index_split_name = file_name_type.rfind('.')
    file_name = file_name_type[0: index_split_name]
    file_type = file_name_type[index_split_name::]
    if count == 0:
        if os.path.exists(current_path + "/" + file_name + file_type):
            return get_unique_file_name(file_name_type, current_path, count + 1)
        return file_name + file_type
    else:
        if os.path.exists(current_path + "/" + file_name + " (" + str(count) + ")" + file_type):
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


def get_full_file_path(path):
    return config.FILE_STORAGE_ROOT + path


def file_path_valid(requested_path):
    return os.path.exists(requested_path) and not os.path.isdir(requested_path)


def size_valid(file):
    return not os.fstat(file.fileno()).st_size > config.MAX_FILE_SIZE


def file_move_valid(source_path, target_path):
    if not file_path_valid(target_path):
        try:
            shutil.move(source_path, target_path)
            return True
        except:
            return False
    return False


def file_replace_valid(file, file_path):
    while os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            return False
    return file_save_valid(file, file_path)


def file_save_valid(file, file_path):
    try:
        file.save(file_path)
        return True
    except:
        return False


def file_type_valid(file_type):
    return file_type.lower() in config.ALLOWED_FILE_TYPES


def file_valid(file, file_type):
    return file_type_valid(file_type) and size_valid(file)


def upload_file(file, path, confirmation):
    if dir_exists(path):
        file_name = file.filename
        file_type = file_name.split('.')[1]
        file_path = os.path.join(path, file_name)
        if file_valid(file, file_type):
            if file_path_valid(file_path) or file_path_valid(os.path.join(path, get_secure_file_name(file_name))):
                if not file_path_valid(file_path):
                    file_name = get_secure_file_name(file_name)
                    file_path = os.path.join(path, file_name)

                if confirmation == 'true':
                    if file_replace_valid(file, file_path):
                        return response("Bestand vervangen", 200)
                    else:
                        return response("Bestand kon niet vervangen worden", 424)
                elif confirmation == 'false':
                    new_file_name = get_unique_file_name(get_secure_file_name(file_name), path, 0)
                    new_file_path = os.path.join(path, new_file_name)
                    if file_save_valid(file, new_file_path):
                        return response("Bestand geupload", 200)
                else:
                    return response(file_name + " bestaat al, wil je deze vervangen?", 409)
            else:
                file_name = get_secure_file_name(file_name)
                file_path = os.path.join(path,
                                         file_name)  # Usage of get_secure_file_name because of (1) possibility beforehand
                if file_save_valid(file, file_path):
                    return response("Bestand geupload", 200)
        else:
            return response("Bedstandstype of grootte is fout van, " + file_name + ", de maximum grootte is: " + str(config.MAX_FILE_SIZE/1000/1000) + "MB, de toegestaande bestandstypes zijn " + str(config.ALLOWED_FILE_TYPES),
                            406)
    return response("Kon bestand niet uploaden", 424)


def file_rename_valid(old_path, new_path):
    if old_path != new_path:
        try:
            os.rename(old_path, new_path)
            return True
        except:
            return False
    return False