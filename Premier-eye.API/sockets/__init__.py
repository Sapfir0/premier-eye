from flask_socketio import SocketIO
from sockets.onImageUpdateSocket import createConnectSocket

def getSocketIO(app):
    socketio = SocketIO(app, cors_allowed_origins="*")
    createConnectSocket(socketio)
    return socketio