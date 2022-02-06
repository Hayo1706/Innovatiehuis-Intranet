import contextlib
import os
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime

from os import path
from threading import Thread

from .helper_functions import response

from .setup import create_app
from .. import config
from ..config import ON_DOCKER

app = create_app()
app.app.backup = False

# in docker change to 172.28.1.3
DB_HOST = '127.0.0.1'
if ON_DOCKER:
    DB_HOST = '172.28.1.3'
DB_USER = 'root@innovatieplatform'
DB_USER_PASSWORD = 'admin'
DB_NAME = 'innovatieplatform'


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

    filename = date+DB_NAME+".sql"
    dumpcmd = "services\mysqldump\mysqldump.exe --column-statistics=0 -P 3306 -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " > " + config.BACKUP_ROOT_PATH + "sql/"+filename

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
