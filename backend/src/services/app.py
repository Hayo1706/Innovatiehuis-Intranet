import os
import shutil
import time

from os import path
from threading import Thread

from .setup import create_app
from .. import config

app = create_app()
app.app.backup = False

DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'admin'
DB_NAME = 'innovatieplatform'


def backup():
    app.app.backup = True
    print("Backup started, don't stop the API.")

    time.sleep(10)

    if path.exists(config.BACKUP_ROOT_PATH + "/data"):
        shutil.rmtree(config.BACKUP_ROOT_PATH + "/data")
    shutil.copytree(config.FILE_STORAGE_ROOT, config.BACKUP_ROOT_PATH + "/data")

    # backup the database
    # TODO when in docker, store correctly
    dumpcmd = "mysqldump -u " + DB_USER + " -p" + " " + DB_NAME + " > " + config.BACKUP_ROOT_PATH + "/sql/" + DB_NAME + ".sql; " + DB_USER_PASSWORD
    os.system(dumpcmd)

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
