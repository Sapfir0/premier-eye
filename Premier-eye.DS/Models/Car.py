from Models.Object_ import Object_


class Car(Object_):
    type = "car"
    licenseNumber: str = None

    def json(self) -> dict:
        objectJson = super().json()
        objectJson.update({'licenseNumber': self.licenseNumber })
        objectJson.update({'type': self.type})
        return objectJson

