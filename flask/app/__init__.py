from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv

from app.api.user import bp as user_bp
from app.api.auth import bp as auth_bp
import app.config as config

load_dotenv()


db = SQLAlchemy()
ma = Marshmallow()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object('app.config')

    print(app.config)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aleksyniemir:haslo123@localhost:5432/inzynierka_db'
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    app.register_blueprint(user_bp, url_prefix='/user') 
    app.register_blueprint(auth_bp, url_prefix='/auth') 

    db.init_app(app)
    ma.init_app(app)

    return app