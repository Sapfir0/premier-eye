

class DecartCoordinates():

    def hasOnePointInside(self, bigRect, minRect): # хотя бы одна точка лежит внутри
        minY, minX, maxY, maxX  = bigRect
        y1, x1, y2, x2 = minRect

        a = (y1 >= minY and y1 <= maxY)
        b = (x1 >= minX and x1 <= maxX)
        c = (y2 >= minY and y2 <= maxY)
        d = (x2 >= minX and x2 <= maxX)

        if (a or b or c or d):
            return True
        return False


    def isCompletelyInside(self, bigRect, minRect): # объект полностью внутри прямоугольника
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


    def isPartiallyInside(self, bigRect, minRect): # объект частично внутри прямоугольника
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

