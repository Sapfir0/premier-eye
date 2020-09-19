import datetime
from database.models.Cars import Cars
from database.models.Persons import Persons
from database.models.Objects_ import Objects_
from database.models.Images import Images, session
from database.models.Coordinates import Coordinates


def parseJson(deserjson):
    """
    Фактически, эта функция занимается приведением типов, т.к. в джсоне все прилетает строками,
    и мы тут восстанавиваем правильные типы и возвращаем словарь
    :param jsonPremier:
    :return:
    """
    hasObjects = '0' in deserjson  # 0 - первый найденный на кадре объект, опеределено на другой стороне
    dateTime = datetime.datetime.strptime(deserjson['fixationDatetime'], '%Y-%m-%d %H:%M:%S')
    numberOfCam = int(deserjson['numberOfCam'])
    filename: str = deserjson['filename']
    return filename, numberOfCam, dateTime, hasObjects


def addObjectToSession(deserializedJson):
    countOfImagesInDB = session.query(Images).count() + 1  # imageId
    # +1 т.к. у нас возвращается текущее колво строк, а мы будем инсертить еще одну
    countOfObjectsInDB = session.query(Objects_).count() + 1  # objectId TODO
    for key, value in deserializedJson.items():
        if key.isdigit():  # навзания объектов будут в таком виде
            coordinates = Coordinates(value['coordinates'])
            Object = Objects_(scores=value['scores'], typesOfObject=value['type'],
                              imageId=countOfImagesInDB, coordinatesId=countOfObjectsInDB)

            if value['type'] == 'car':  # TODO кал
                car = Cars(carNumber=value['licenseNumber'], objectId=countOfObjectsInDB)
                session.add(car)
            elif value['type'] == 'person':
                person = Persons(objectId=countOfObjectsInDB)
                session.add(person)
            else:
                raise Exception("Undefined object")

            session.add(coordinates)
            session.add(Object)


#def getRowFromDb(table, id):
#    session.query
