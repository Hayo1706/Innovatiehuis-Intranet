from multiprocessing import Process
from threading import Thread

from services import app

from src.services.backup import run_backup

if __name__ == "__main__":
    Thread(target=run_backup).start()
    app.app.run(host='127.0.0.1', debug=True)

