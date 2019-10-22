from neural_network.modules.decart import DecartCoordinates
from abc import ABC, abstractmethod


class Object_(ABC):
    id: int = None
    scores = None
    coordinates = []  # LDx, LDy, RUx, RUy
    centerDownCoordinates = []  # CDx, CDy
    masks = []

    def __init__(self, detections):
        self.coordinates = detections['coordinates']
        self.scores = detections['scores']
        self.masks = detections['masks']
        decart = DecartCoordinates()  # мне не нравится когда один конструктор инитит другой неявно
        self.centerDownCoordinates = decart.getCenterOfDown(self.coordinates)

    def __repr__(self):
        return "type: {}".format(self.type)

    def json(self):
        diction = {
            'id': self.id,
            'scores': self.scores,
            'coordinates': self.coordinates,
            'CD': self.centerDownCoordinates,
            'masks': self.masks
        }
        return diction
