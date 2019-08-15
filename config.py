# configuration file config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'mysql://root:numan@localhost:3306/'
database_name = 'web_chat_task'

class BaseConfig:
    """Base configuration."""
    DEBUG = False
    SECRET_KEY = 'Secret'
    TOKEN_VAILD_SEC = 86400 #Seconds
    # database settings
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # file upload definitions
    UPLOAD_FOLDER = basedir + '/files'  # top level upload folder # To do sil eger dosya yuklemiceksek
    ALLOWED_EXTENSIONS = set(['gcode', 'stl'])  # allow gcode and stl file extensions # To do sil
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024  # max file size for upload: 1 GB # To do sil
    REST_URL_PREFIX = ''
    # User password settings
    KEY_LENGTH = 32
    HASH_FUNCTION = 'sha512'
    COST_FACTOR = 10000

    REST_URL_TESTING = 'http://localhost:5000/'

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
