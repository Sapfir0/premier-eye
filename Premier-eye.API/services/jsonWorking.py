import datetime
from database.models.Cars import Cars
from database.models.Persons import Persons
from database.models.Objects_ import Objects_
from database.models.Images import Images, session
from database.models.Coordinates import Coordinates


def addObjectToSession(objects):
    countOfImagesInDB = session.query(Images).count() + 1  # imageId
    # +1 т.к. у нас возвращается текущее колво строк, а мы будем инсертить еще одну
    countOfObjectsInDB = session.query(Objects_).count() + 1  # objectId TODO
    for detected in objects:
        coordinates = Coordinates(detected['coordinates'])
        Object = Objects_(scores=detected['scores'], typesOfObject=detected['type'],
                          imageId=countOfImagesInDB, coordinatesId=countOfObjectsInDB)

        if detected['type'] == 'car':  # TODO кал
            car = Cars(carNumber=detected['licenseNumber'], objectId=countOfObjectsInDB)
            session.add(car)
        elif detected['type'] == 'person':
            person = Persons(objectId=countOfObjectsInDB)
            session.add(person)
        else:
            raise Exception("Undefined object")

        session.add(coordinates)
        session.add(Object)
