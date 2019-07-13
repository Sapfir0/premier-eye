import sqlalchemy as sql
import services.database_controller as db
from colorama import Fore

class DecartCoordinates():

    def getCenterOfDownOfRectangle(self, boxes): # задан левый нижний и правый верхний угол
        allCenters = []
        for i in range(boxes.shape[0]):
            y1, x1, y2, x2 = boxes[i]
            midleDownPoint = [ (x1+x2)/2, y1]
            allCenters.append(midleDownPoint)
        return allCenters

    def getConcetration(self, highlightedRect, startTime, endTime): # координаты прямоугольника, в котором начинаем искать объекты
        foundedObjects = []
        # запрос к бд
        for obj in db.session.query(db.Objects).filter(sql.and_(db.Objects.fixationDatetime >= startTime, db.Objects.fixationDatetime <= endTime)).all():
            minRect = [obj.LDy, obj.LDx, obj.RUy, obj.RUx]
            if ( self.hasOnePointInside(highlightedRect, minRect )):
                foundedObjects.append(obj)

        return foundedObjects # массив координат всех объектов в кадре

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


    def isPartiallyInside(self, bigRect, minRect, innerPercent=0.5): # объект частично внутри прямоугольника
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
        return in_obj_square / full_square >= innerPercent

