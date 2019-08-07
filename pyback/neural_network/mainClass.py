import os
import requests

import helpers.dateHelper as dh
import services.database_controller as db
import services.file_controller as file_controller
import helpers.others as others
import helpers.directory as dirs


class MainClass(object):
    from settings import Settings
    cfg = Settings()  # единственный раз, когда мы создаем инстанс

    if cfg.ALGORITHM:
        from neural_network.maskCNN import Mask
        mask = Mask()
    else:
        from neural_network.imageAi import ImageAI
        imageAI = ImageAI()

    from neural_network.modules.decart import DecartCoordinates
    decart = DecartCoordinates()

    currentImageDir = os.path.join(os.getcwd(), cfg.IMAGE_DIR)
    def __init__(self, numberOfCam: int, filenames: list, processedFrames: dict):
        self.detectObjects(numberOfCam, filenames, processedFrames)

    def detectObjects(self, numberOfCam: int, filenames: list, processedFrames: dict):
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
                    #time.sleep(2.5)  # засыпает поток исполнения
                continue  # если файлы еще есть, то переходим к следующему

            inputFile, outputFile, dateTime = others.getIOdirs(filename, self.cfg.IMAGE_DIR, self.cfg.OUTPUT_DIR_MASKCNN)

            if self.cfg.ALGORITHM:  # Mask CNN
                detections,  humanizedOutput = self.mask.pipeline(inputFile, outputFile)
                rectCoordinates = detections['rois']
            else:  # image ai # этот алгоритмы всегда остают в нововведениях
                detections = self.imageAI.pipeline(inputFile, outputFile)
                rectCoordinates = others.parseImageAiData(detections)

            # car detector
            carNumbers = []
            if self.cfg.CAR_NUMBER_DETECTOR:
                from neural_network.car_number import car_detect
                if numberOfCam in [str(1), str(2)] and humanizedOutput:  # если камера №2 или №1 и присутсвует хотя бы один объект на кадре, то запускем тест на номера
                    imD = os.path.join(os.path.split(outputFile)[0], "objectsOn" + filename.split(".")[0])
                    carNumbers = car_detect(imD)

            processedFrames[numberOfCam].append(filename)

            file_controller.writeInFile(self.cfg.DATE_FILE, str(processedFrames))  # будет стирать содержимое файла каждый кадр

            # DB
            if self.cfg.loggingInDB:
                castingCarNumber = None
                iterator = 0
                centerDown = self.decart.getCenterOfDownOfRectangle(rectCoordinates)  # массив массивов(массив координат центра нижней стороны прямоугольника у найденных объектов вида [[x1,y1],[x2,y2]..[xn,yn]])
                for i, item in enumerate(humanizedOutput):  # для каждого объекта, найденного на кадре
                    if item == "car" and carNumbers:
                        if carNumbers[iterator] == [] or carNumbers[iterator] == ['']:
                            castingCarNumber = None
                        else:
                            castingCarNumber = carNumbers[iterator][0]
                        iterator += 1

                    db.writeInfoForObjectInDB(numberOfCam, humanizedOutput[i], dateTime, rectCoordinates[i], centerDown[i], castingCarNumber)

            # checkConnections with Pyfront
            if self.cfg.sendRequestToServer:
                r = requests.post(self.cfg.pyfrontDevelopmentLink, {"filename": filename})
                if not r.status_code == 200:
                    raise ValueError("Server isn't available")

            dirs.removeDirectoriesFromPath(os.path.split(outputFile)[0])
            return detections