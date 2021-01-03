from abc import ABC, abstractmethod
from typing import Dict, List


class Object_(ABC):
    type: str = "object"
    id: int = 0
    scores = None
    coordinates: List[int] = []  # LDx, LDy, RUx, RUy
    centerDownCoordinates: List[int] = []  # CDx, CDy

    def __init__(self, detections):
        self.coordinates = detections['coordinates']
        self.scores = detections['scores']

    def __repr__(self):
        return f"{{type: {self.type}, scores: {self.scores}," \
               f"centerDownCoordinates: {self.centerDownCoordinates} }}"

    def json(self) -> dict:
        print(self.scores.item())
        print(self.coordinates.tolist())
        diction = {  # маски передавать не будем
            'id': self.id,
            'type': self.type,
            'scores': self.scores.item(), #TODO хаос тут исправить
            'coordinates': self.coordinates.tolist()  # почему-то тоже нулл. значения вроде таких 0.9981159
        }
        return diction

