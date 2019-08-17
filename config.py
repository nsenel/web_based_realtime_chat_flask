# configuration file config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """Base configuration."""
    DEBUG = False
    SECRET_KEY = 'Secret'
    TOKEN_VAILD_SEC = 86400 #Seconds
    # database settings
    SQLALCHEMY_DATABASE_URI = 'postgres://hwvymydjjtnnwu:e8e82c2a3234b3a8e53a46d318e5f4d27d6568889f7eddf27a35ec5c23b25b3d@ec2-54-83-36-37.compute-1.amazonaws.com:5432/da2upp3ugr79up'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REST_URL_PREFIX = ''
    # User password settings
    KEY_LENGTH = 32
    HASH_FUNCTION = 'sha512'
    COST_FACTOR = 10000

    REST_URL_TESTING = 'http://localhost:5000/'

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
