import shutil
import time
from threading import Thread

from src import config

def backup():
    print("Backup started, don't stop the program.")
    shutil.rmtree(config.BACKUP_ROOT_PATH)
    shutil.copytree(config.FILE_STORAGE_ROOT, config.BACKUP_ROOT_PATH)
    print("Backup complete, program can be stopped now, "
          "in " + str(config.BACKUP_FREQUENCY) + " minutes, the backup will start again.")


class BackupRunner(Thread):
    done = False

    def start(self):
        while not self.done:
            backup()
            try:
                time.sleep(config.BACKUP_FREQUENCY * 60)
            except KeyboardInterrupt:
                print("Backup program stopped")

    def set_done(self):
        self.done = True


if __name__ == '__main__':
    backupRunner = BackupRunner()
    backupRunner.start()
