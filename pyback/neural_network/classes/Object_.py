from neural_network.modules.decart import DecartCoordinates


class Object_(object):
    id: int = None
    type = "obj"
    scores = None
    coordinates = []  # LDx, LDy, RUx, RUy
    CDx: int = None
    CDy: int = None
    masks = []

    def __init__(self, detections):
        self.coordinates = detections['coordinates']
        self.scores = detections['scores']
        self.masks = detections['masks']
        print(type(self.coordinates), self.coordinates)
        decart = DecartCoordinates()  # мне не нравится когда один конструктор инитит другой неявно
        self.CDx, self.CDy = decart.getCenterOfDown(self.coordinates)

    def __repr__(self):
        return "id = {}, type: {}".format(self.id, self.type)
