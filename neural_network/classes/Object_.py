from abc import ABC, abstractmethod


class Object_(ABC):
    type: str = "object"
    id: int = None
    scores = None
    coordinates = []  # LDx, LDy, RUx, RUy
    centerDownCoordinates = []  # CDx, CDy
    masks = []

    def __init__(self, detections):
        self.coordinates = detections['coordinates']
        self.scores = detections['scores']
        self.masks = detections['masks']
        self.centerDownCoordinates = self.getCenterOfDown(self.coordinates)

    def __repr__(self):
        return f"{{type: {self.type}, scores: {self.scores}," \
               f" masks: {self.masks}, centerDownCoordinates: {self.centerDownCoordinates} }}"

    def json(self) -> dict:
        diction = {  # маски передавать не будем
            'id': self.id,
            'type': self.type,
            'scores': self.scores.item(), #TODO хаос тут исправить
            'coordinates': self.coordinates.tolist(),  # почему-то тоже нулл. значения вроде таких 0.9981159
            'CD': self.centerDownCoordinates # если есть лист, то в нем только первый элемент будет не налл
        }
        return diction

    def getCenterOfDown(self, boxes) -> list:
        y1, x1, y2, x2 = boxes  # задан левый нижний и правый верхний угол
        midleDownPoint = [(x1+x2)/2, y1]
        return midleDownPoint

    def getCenterOfDownOfRectangle(self, boxes: list) -> list:
        allCenters = []

        for i in boxes:
            y1, x1, y2, x2 = i  # задан левый нижний и правый верхний угол
            midleDownPoint = [(x1+x2)/2, y1]
            allCenters.append(midleDownPoint)
        return allCenters
