from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object('app.config.TestConfig')

    from app.api.user import bp as user_bp
    from app.api.auth import bp as auth_bp
    from app.api.gpt import bp as gpt_bp
    app.register_blueprint(user_bp, url_prefix='/user') 
    app.register_blueprint(auth_bp, url_prefix='/auth') 
    app.register_blueprint(gpt_bp, url_prefix='/gpt')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database."""
        with app.app_context():
            db.create_all()
        print("Initialized the database.")

    return app
