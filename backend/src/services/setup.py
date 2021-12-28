import connexion
from flask_cors import CORS
from sqlalchemy import create_engine

from .extensions import db, login_manager

url = 'mariadb+mariadbconnector://root:admin@127.0.0.1:3306/innovatieplatform'


def create_app():
    app = connexion.App(__name__, specification_dir="../")
    # Read the API.yml file to configure the endpoints
    app.add_api("API.yml")
    app.app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.app.config['SQLALCHEMY_POOL_SIZE'] = 20
    app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app.config['SQLALCHEMY_DATABASE_URI'] = url
    CORS(app.app)
    db.init_app(app.app)
    with app.app.app_context():
        db.create_engine(url, {})
        # login_manager.init_app(app.app)
        return app
