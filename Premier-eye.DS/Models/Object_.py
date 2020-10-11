from abc import ABC, abstractmethod


class Object_(ABC):
    type: str = "object"
    id: int = None
    scores = None
    coordinates = []  # LDx, LDy, RUx, RUy
    centerDownCoordinates = []  # CDx, CDy

    def __init__(self, detections):
        self.coordinates = detections['coordinates']
        self.scores = detections['scores']

    def __repr__(self):
        return f"{{type: {self.type}, scores: {self.scores}," \
               f"centerDownCoordinates: {self.centerDownCoordinates} }}"

    def json(self) -> dict:
        diction = {  # маски передавать не будем
            'id': self.id,
            'type': self.type,
            'scores': self.scores.item(), #TODO хаос тут исправить
            'coordinates': self.coordinates.tolist()  # почему-то тоже нулл. значения вроде таких 0.9981159
        }
        return diction

