import waitress

from src import app
from src.config import ON_DOCKER

if __name__ == "__main__":
    if ON_DOCKER:
        waitress.serve(app.app, host='0.0.0.0', port=5000)
    else:
        app.app.run(host='127.0.0.1', debug=False)
