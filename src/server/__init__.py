# src/server/__init__.py

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO


app = Flask(__name__)
CORS(app)#, resorces={r'/d/*': {"origins": '*'}})

# set application wide configuration parameters
app_settings = os.getenv(
    'APP_SETTINGS',
    'config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
socketio = SocketIO()



import src.database
import src.server.sockets

socketio.init_app(app)