import shutil
import time


from src import config


def backup():
    print("Backup started, don't stop the program.")
    shutil.rmtree(config.BACKUP_ROOT_PATH)
    shutil.copytree(config.FILE_STORAGE_ROOT, config.BACKUP_ROOT_PATH)
    print("Backup complete, "
          "in " + str(config.BACKUP_FREQUENCY) + " minutes, the backup will start again.")


def run_backup():
    while True:
        try:
            backup()
            time.sleep(config.BACKUP_FREQUENCY * 60)
        except KeyboardInterrupt:
            break




