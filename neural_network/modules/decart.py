
class DecartCoordinates(object):
    """
        Класс для 2 задания
        getConcentration - основной метод
    """
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
