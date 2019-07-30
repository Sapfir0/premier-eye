import sqlalchemy as sql
import services.database_controller as db


class DecartCoordinates():
    """
        Класс для 2 задания
        getConcentration - основной метод
    """
    def getCenterOfDownOfRectangle(self, boxes: list) -> list:
        allCenters = []

        for i in boxes:
            y1, x1, y2, x2 = i  # задан левый нижний и правый верхний угол
            midleDownPoint = [(x1+x2)/2, y1]
            allCenters.append(midleDownPoint)
        return allCenters

    def getConcentration(self, highlightedRect, startTime, endTime):
        """
            highlightedRectкоординаты прямоугольника, в котором начинаем искать объекты
        """
        foundedObjects = []
        a = db.Objects.fixationDatetime >= startTime
        b = db.Objects.fixationDatetime <= endTime
        for obj in db.session.query(db.Objects).filter(sql.and_(a, b)).all():
            minRect = [obj.LDy, obj.LDx, obj.RUy, obj.RUx]
            if (self.hasOnePointInside(highlightedRect, minRect)):
                foundedObjects.append(obj)

        return foundedObjects  # массив координат всех объектов в кадре

    def hasOnePointInside(self, bigRect, minRect):  # хотя бы одна точка лежит внутри
        minY, minX, maxY, maxX = bigRect
        y1, x1, y2, x2 = minRect

        a = (minY <= y1 <= maxY)
        b = (minX <= x1 <= maxX)
        c = (minY <= y2 <= maxY)
        d = (minX <= x2 <= maxX)

        if (a or b or c or d):
            return True
        return False


    def isCompletelyInside(self, bigRect, minRect): # объект полностью внутри прямоугольника
        y1, x1, y2, x2 = bigRect
        minX = x1; minY = y1  # вроде верно
        maxX = x2; maxY = y2
        
        y1, x1, y2, x2 = minRect

        a = (minY <= y1 <= maxY)
        b = (minX <= x1 <= maxX)
        c = (minY <= y2 <= maxY)
        d = (minX <= x2 <= maxX)

        if (a and b and c and d):
            return True  # объект полностью внутри большого прямоугольника
        return False

    def isPartiallyInside(self, bigRect, minRect, innerPercent=0.5):  # объект частично внутри прямоугольника
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

