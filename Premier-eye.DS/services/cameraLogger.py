import logging

class CameraLogger:
    logger = None
    def __init__(self, cameraId):
        customFormat = '%(asctime)-15s %(cameraId)s %(date)s %(objectType)s %(message)s'
        logging.basicConfig(level=logging.INFO, filename='app.log', )
        self.logger = logging.getLogger(f'camera {cameraId}')

    def log(self, message, cameraId, datetime):
        d = {'cameraId': cameraId, 'date': datetime, }
        self.logger.info(message, extra=d)

    def enterPerson(self, cameraId, datetime):
        self.log('человек вошел в кадр', cameraId, date)
    
    def leftPerson(self, cameraId, datetime):
        self.log('человек пропал', cameraId, date)

    def enterCar(self, cameraId, datetime):
        self.log('автомобиль вошел в кадр', cameraId, date)

    def leftCar(self, cameraId, datetime):
        self.log('автомобиль пропал', cameraId, date)

