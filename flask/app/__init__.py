from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv



db = SQLAlchemy()
ma = Marshmallow()

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aleksyniemir:haslo123@localhost:5432/inzynierka_db'
    if test_config is None:
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object('app.config.TestConfig')

    from app.api.user import bp as user_bp
    from app.api.auth import bp as auth_bp
    app.register_blueprint(user_bp, url_prefix='/user') 
    app.register_blueprint(auth_bp, url_prefix='/auth') 

    db.init_app(app)
    ma.init_app(app)

    return app
