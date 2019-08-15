from neural_network.modules.decart import DecartCoordinates


class Object_(object):
    id: int = None
    type = "obj"
    scores = None
    LDx: int = None
    LDy: int = None
    RUx: int = None
    RUy: int = None
    CDx: int = None
    CDy: int = None

    def __init__(self, detections):
        self.LDx, self.LDy, self.RUx, self.RUy = detections['coordinates']
        self.scores = detections['scores']
        decart = DecartCoordinates()  # мне не нравится когда один конструктор инитит другой неявно
        self.CDx, self.CDy = decart.getCenterOfDown(detections['coordinates'])

    def __repr__(self):
        return "id = {}, type: {}".format(self.id, self.type)
