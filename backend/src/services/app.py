import contextlib
import os
import shutil
import subprocess
import time
import traceback
from datetime import datetime

from os import path
from threading import Thread

from .helper_functions import response
from .setup import create_app
import src.config as config

app = create_app()
app.app.backup = False


@app.app.errorhandler(Exception)
def handle_error(e):
    print("An Exception occurred!")
    print(traceback.format_exc())
    return response(traceback.format_exc(), 500)


def backup():
    app.app.backup = True
    print("Backup started, don't stop the API.")

    time.sleep(10)

    if path.exists(config.BACKUP_ROOT_PATH + "data"):
        shutil.rmtree(config.BACKUP_ROOT_PATH + "data")
    shutil.copytree(config.FILE_STORAGE_ROOT, config.BACKUP_ROOT_PATH + "data")

    # generate sql

    if not path.exists(config.BACKUP_ROOT_PATH + "sql/"):
        os.mkdir(config.BACKUP_ROOT_PATH + "sql/")

    date = datetime.now().strftime("%d-%m-%Y__%H_%M-")

    filename = f"{date}{config.DB_NAME}.sql"
    dumpcmd = f"services\mysqldump\mysqldump.exe --column-statistics=0 -P 3306 -h {config.DB_HOST} -u {config.DB_USER} -p{config.DB_USER_PASSWORD} " \
              f" {config.DB_NAME} > {config.BACKUP_ROOT_PATH}sql/{filename}"

    syscmd(dumpcmd, "utf8")

    app.app.backup = False
    print("Backup complete. "
          "In " + str(config.BACKUP_FREQUENCY) + " minutes, the backup will start again.")


def run_backup():
    while True:
        try:
            time.sleep(config.BACKUP_FREQUENCY * 60)
            backup()
        except KeyboardInterrupt:
            break


Thread(target=run_backup).start()


def syscmd(cmd, encoding=''):
    """
    source: stackoverflow
    Runs a command on the system, waits for the command to finish, and then
    returns the text output of the command. If the command produces no text
    output, the command's return code will be returned instead.
    """
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         close_fds=True)
    p.wait()
    output = p.stdout.read()
    if len(output) > 1:
        if encoding:
            return output.decode(encoding)
        else:
            return output
    return p.returncode
