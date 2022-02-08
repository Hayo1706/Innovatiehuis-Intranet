from multiprocessing import Process
from threading import Thread

import waitress

from src import app
from src.config import ON_DOCKER

if __name__ == "__main__":
    # change to 0.0.0.0 when using docker
    if ON_DOCKER:
        waitress.serve(app.app, host='0.0.0.0', port=5000)
    else:
        waitress.serve(app.app, host='127.0.0.1', port=5000)
