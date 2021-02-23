from flask_socketio import send, emit
from flask_restplus import Namespace, Resource


def createConnectSocket(socketio):
    
    @socketio.event('connect')
    def test_connect(self):
        emit('my response', {'data': 'Connected'})



