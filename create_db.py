#!env/bin/python

from src.server import app, db
from src.database import models

db.create_all()
