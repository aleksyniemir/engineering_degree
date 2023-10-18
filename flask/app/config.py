from dotenv import load_dotenv
import os 


load_dotenv()

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config): 
    TESTING = False

class TestConfig(Config): 
    TESTING = True