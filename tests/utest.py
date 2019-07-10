import unittest
#import sys, os
# sys.path.append("../neural_network")
# import maskCNN

class FunctionTest(unittest.TestCase):
    objectsInFrame = [
        [ 299, 658, 539,  1173],
        [ 422,   0, 714,   331],
        [  68, 1032, 131, 1111]
    ]
    highlightedArea = [
        [0, 800, 0, 1200],
        [0, 0, 0, 0],
        [200, 400, 600, 1000]
    ]
    expected_output = [True, False , True]

    def testCompletelyInside(self):
        for i in range(0, len(self.objectsInFrame)):
            res = isCompletelyInside(self.highlightedArea[i], self.objectsInFrame[i])
            self.assertEqual(res, self.expected_output[i])

    def testPartiallyInside(self):
        for i in range(0, len(self.objectsInFrame)):
            res = isPartiallyInside(self.highlightedArea[i], self.objectsInFrame[i])
            self.assertEqual(res, self.expected_output[i])

if __name__ == '__main__':
    unittest.main()



def getObjectFromRect(highlightedRect, objectsRect, startTime, endTime): # координаты прямоугольника, в котором начинаем искать объекты
    for obj in objectsRect:
        if ( isPartiallyInside(highlightedRect, obj) ):
            print("Объект попадает в кадр")

    return foundedObjects # массив координат всех объектов в кадре



def isCompletelyInside(bigRect, minRect):
    y1, x1, y2, x2 = bigRect
    minX = x1; minY = y1 # вроде верно
    maxX = x2; maxY = y2
    
    y1, x1, y2, x2 = minRect

    a = (y1 >= minY and y1 <= maxY)
    b = (x1 >= minX and x1 <= maxX)
    c = (y2 >= minY and y2 <= maxY)
    d = (x2 >= minX and x2 <= maxX)

    if (a and b and c and d):
        return True # объект полностью внутри большого прямоугольника
    return False


def isPartiallyInside(bigRect, minRect):
    bigLUy, bigLUx, bigRDy, bigRDx = bigRect
    minLUy, minLUx, minRDy, minRDx = minRect
    full_square = (minLUy - minRDy) * (minRDx - minLUx) ## не уверен что правильно
    # Не уверен в ифах
    if (bigLUy < minLUy):
        minLUy = bigLUy
    if (bigRDy < minRDy):
        minRDy = bigRDy
    if (bigLUx > minLUx):
        minLUx = bigLUx
    if (bigRDx > minRDx):
        minRDx = bigRDx
    in_obj_square = (minLUy - minRDy) * (minRDx - minLUx)
    return in_obj_square / full_square >= 0.5


