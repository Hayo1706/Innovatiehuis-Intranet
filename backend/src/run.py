from multiprocessing import Process
from threading import Thread

from src import app

if __name__ == "__main__":
    # change to 0.0.0.0 when using docker
    app.app.run(host='127.0.0.1', debug=False)

