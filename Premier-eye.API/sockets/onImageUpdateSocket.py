from flask_socketio import Namespace, emit


class OnImageUpdateSocket(Namespace):
    def on_connect(self):
        emit('my response', {'data': 'Connected'})

    def on_disconnect(self):
        emit('my response', {'data': 'Disconnected'})

    def on_my_event(self, data):
        emit('my_response', data)






