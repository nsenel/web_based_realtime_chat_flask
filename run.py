#!env/bin/python

from src.server import app, socketio

#app(debug=True)

if __name__ == '__main__':
    socketio.run(app, port=5000)