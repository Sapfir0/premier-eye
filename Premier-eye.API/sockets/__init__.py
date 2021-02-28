from flask_socketio import SocketIO
from sockets.onImageUpdateSocket import OnImageUpdateSocket

socketio = SocketIO(cors_allowed_origins="*")

socketio.on_namespace(OnImageUpdateSocket('/image'))
