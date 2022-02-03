from multiprocessing import Process
from threading import Thread

from src import app

if __name__ == "__main__":
    app.app.run(host='127.0.0.1', debug=False)

