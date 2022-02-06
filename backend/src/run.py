from multiprocessing import Process
from threading import Thread

from src import app
from src.config import ON_DOCKER

if __name__ == "__main__":
    # change to 0.0.0.0 when using docker
    if ON_DOCKER:
        app.app.run(host='0.0.0.0', debug=False)
    else:
        app.app.run(host='127.0.0.1', debug=False)
