from dotenv import load_dotenv
import os 


load_dotenv()

class Config(object):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')