from dotenv import load_dotenv
import os 


load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config): 
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    TESTING = False

class TestConfig(Config): 
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
    TESTING = True