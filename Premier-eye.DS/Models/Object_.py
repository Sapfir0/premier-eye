from abc import ABC, abstractmethod
from typing import Dict, List


class Object_(ABC):
    type: str = "object"
    id: int = 0
    scores: List[float] = []
    coordinates: List[int] = []  # LDx, LDy, RUx, RUy
    masks: List[bool] = []

    def __init__(self, detections):
        self.coordinates = detections['coordinates'].tolist()
        self.scores = detections['scores'].item()
        self.masks = detections['masks']

    def __repr__(self):
        return f"type: {self.type}, scores: {self.scores}"

    def json(self) -> dict:
        diction = {  # маски передавать не будем
            'id': self.id,
            'type': self.type,
            'scores': self.scores,
            'coordinates': self.coordinates
        }
        return diction

