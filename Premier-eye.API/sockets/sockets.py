from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins='*')

def initSocket(app):
    socketio.init_app(app)
