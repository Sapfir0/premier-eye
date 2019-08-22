import os
import requests

import helpers.dateHelper as dh
import services.database_controller as db
import services.file_controller as file_controller
import helpers.others as others
import helpers.directory as dirs
from neural_network.classes import Image
from settings import Settings as cfg


if cfg.ALGORITHM:
    from neural_network.maskCNN import Mask
    mask = Mask()
else:
    from neural_network.imageAi import ImageAI
    imageAI = ImageAI()

from neural_network.modules.decart import DecartCoordinates
decart = DecartCoordinates()

currentImageDir = os.path.join(os.getcwd(), cfg.IMAGE_DIR)


def predicated( numberOfCam: int, filenames: list, processedFrames: dict):
    """
        Сакральный алгоритм:

        Глава I. Dictionary from images directory.
            Проходимся по папке с изображениями и цепляемся за головы. Головой в нашем случае назовем самое раннее
            изображение с каждой камеры. Как мы это сделаем? Добавим все в словарь типа
            dict{numberOfCamera:arrayOfImages[numberOfCamera_image1, numberOfCamera_image2, .., numberOfCamera_imageN]},
            и отсортируем эти массивы по устареванию. Соответственно, нулевой элемент каждого массива - это голова.
        Глава II. Processed Frames.
            После успешного завершения алогритма мы добавляем название изображения в словарь processedFrames с такой же структурой, как и предыдущий.
            Если в processedFrames уже находится имя файла, которое мы взяли из словаря из прошлой главы,
            то изображение уже обработано, и мы пропускаем его. После успешной обработки, мы записываем словарь в файл.
            Если стоит опция в настройках checkOldProcessedFrames, то при запуске программы, мы читаем из файла наш словарь,
            соответственно, мы не обработаем файл, который был уже обработан при предыдущих запусках.
            Если у двух словарей идентичны массивы, ассоцирующуюся с одной камерой, то мы спим(спит поток:( )
        Глава III. То, чего нет.
            Потоки. В первоначальном задумке потоков(вероятнее всего, демонов) должно быть столько же, сколько и голов.
            И мы бы проходились по их чахлым телесам в n потоков. Но почему-то тензорфлоу(или керас) не может запуститься в мультитреде.
            Псевдокод многопоточки:
                * Добавить к масиву потоков функцию со всем доступными аргументами в словаре №1
                * После цикла пройтись по этому массиву и начать выполнение всех потоков
                - коммит #9106cbe
        Глава IV. лнениеАссин выпохронное.
            Дает меньший прирост, чем потоки.
    """
    for filename in filenames:
        if numberOfCam not in processedFrames.keys():
            processedFrames.update({numberOfCam: []})

        if filename in processedFrames[numberOfCam]:
            if processedFrames[numberOfCam] == filenames:
                import time
                print(f"Thread {numberOfCam} sleeping")
                #time.sleep(2.5)
            continue  # если файлы еще есть, то переходим к следующему

        detections = detectObjects(filename)
        processedFrames[numberOfCam].append(filename)
        file_controller.writeInFile(cfg.DATE_FILE, str(processedFrames))
        # будет стирать содержимое файла каждый кадр
        return detections

def _maskCnnDetect( inputFile, outputFile):
    image = mask.pipeline(inputFile, outputFile)
    return image

def _imageAiDetect( inputFile, outputFile):
    detections = imageAI.pipeline(inputFile, outputFile)
    rectCoordinates = others.parseImageAiData(detections)
    return detections, rectCoordinates

def _carNumberDetector( numberOfCam, humanizedOutput, outputFile, filename):
    from neural_network.car_number import car_detect
    carNumbers = []
    if humanizedOutput and numberOfCam in [str(1), str(2)]:
        # если камера №2 или №1 и присутсвует хотя бы один объект на кадре, то запускем тест на номера
        imD = os.path.join(os.path.split(outputFile)[0], "objectsOn" + filename.split(".")[0])
        carNumbers = car_detect(imD)
    return carNumbers

def _dblogging( image: Image):
    for i, item in enumerate(image.objects):  # для каждого объекта, найденного на кадре
        frameObject = image.objects[i]
        try:  # если сработает исключение, то это либо не машина либо номер не определен
            frameObject.licenseNumber  # тупо проверка наличия
        except:
            frameObject.licenseNumber = None

        db.writeInfoForObjectInDB(image.numberOfCam,
                                  frameObject.type,
                                  image.fixationDatetime,
                                  frameObject.coordinates,
                                  frameObject.centerDownCoordinates,
                                  frameObject.licenseNumber)

def _requestToServer( filename):
    r = requests.post(cfg.pyfrontDevelopmentLink, {"filename": filename})
    if not r.status_code == 200:
        raise ValueError("Server isn't available")

def detectObjects( filename):
    inputFile, outputFile, dateTime = others.getIOdirs(filename, cfg.IMAGE_DIR, cfg.OUTPUT_DIR_MASKCNN)
    numberOfCam = dh.parseFilename(filename, getNumberOfCamera=True, getDate=False)

    if cfg.ALGORITHM:
        image = _maskCnnDetect(inputFile, outputFile)
    else:
        detections, rectCoordinates = _imageAiDetect(inputFile, outputFile)

    if cfg.CAR_NUMBER_DETECTOR:
        carNumber = _carNumberDetector(numberOfCam, humanizedOutput, outputFile, filename)

    if cfg.loggingInDB:
        _dblogging(image)

    if cfg.sendRequestToServer:
        _requestToServer(filename)

    dirs.removeDirectoriesFromPath(os.path.split(outputFile)[0])
    return image
