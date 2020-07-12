import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_EXPIRY = 60 * 60 * 4

class Development(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class Testing(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

configs = {"testing": Testing,
           "development": Development}
