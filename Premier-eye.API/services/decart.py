import os
import tempfile



def hasOnePointInside(bigRect, minRect):  # хотя бы одна точка лежит внутри
    minY, minX, maxY, maxX = bigRect
    y1, x1, y2, x2 = minRect

    a = (minY <= y1 <= maxY)
    b = (minX <= x1 <= maxX)
    c = (minY <= y2 <= maxY)
    d = (minX <= x2 <= maxX)

    return a or b or c or d


def isCompletelyInside(bigRect, minRect):  # объект полностью внутри прямоугольника
    minY, minX, maxY, maxX = bigRect

    y1, x1, y2, x2 = minRect

    a = (minY <= y1 <= maxY)
    b = (minX <= x1 <= maxX)
    c = (minY <= y2 <= maxY)
    d = (minX <= x2 <= maxX)

    return a and b and c and d # если тру, то объект полностью внутри большого прямоугольника


def isPartiallyInside(bigRect, minRect, innerPercent=0.5):  # объект частично внутри прямоугольника
    bigLUy, bigLUx, bigRDy, bigRDx = bigRect
    minLUy, minLUx, minRDy, minRDx = minRect
    fullSquare = (minLUy - minRDy) * (minRDx - minLUx)  # не уверен что правильно
    # Не уверен в ифах
    if bigLUy < minLUy:
        minLUy = bigLUy
    if bigRDy < minRDy:
        minRDy = bigRDy
    if bigLUx > minLUx:
        minLUx = bigLUx
    if bigRDx > minRDx:
        minRDx = bigRDx
    inObjSquare = (minLUy - minRDy) * (minRDx - minLUx)
    return inObjSquare / fullSquare >= innerPercent


def createGraphic(imagePath: str, searchRect: list, objectsListRect: list):
    import matplotlib.pyplot as plt
    from PIL import Image
    import numpy as np
    import matplotlib.patches as patches

    im = np.array(Image.open(imagePath), dtype=np.uint8)
    fig, ax = plt.subplots(1)
    ax.imshow(im)

    bigRect = Rectangle(searchRect)
    minRects = [Rectangle(i) for i in objectsListRect]

    rect = patches.Rectangle(*bigRect.getMTparam(), linewidth=1, edgecolor='g', facecolor='None')
    ax.add_patch(rect)

    for i in minRects:
        rect = patches.Rectangle(*i.getMTparam(), linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    temp = tempfile.NamedTemporaryFile()
    path = os.path.join(os.getcwd(), temp.name)
    plt.savefig(path)

    return os.path.split(temp.name + ".png")


class Rectangle:
    LUx = 0
    LUy = 0
    RDx = 0
    RDy = 0

    def __init__(self, coordinates: list):
        if len(coordinates) != 4:
            raise ValueError("Нужно подавать координаты(х,у) двух противоложных вершин")
        if coordinates[0] >= coordinates[2] or coordinates[1] >= coordinates[3]:
            raise ValueError(
                "Неверно заданы вершины, сначала подаются 2 координаты нижнего левого угла, потом верхнего правого")
        self.LUy, self.LUx, self.RDy, self.RDx = coordinates

    def getCenterOfDown(self):
        return [(self.LUx + self.RDx) / 2, self.RDy]

