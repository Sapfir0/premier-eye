from neural_network.classes.Object_ import Object_


class Car(Object_):
    type = "car"
    licenseNumber: str = None

    def json(self):
        objectJson = super().json()
        objectJson.update({'licenseNumber': self.licenseNumber })


