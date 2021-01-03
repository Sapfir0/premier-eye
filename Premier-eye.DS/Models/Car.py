from Models.Object_ import Object_


class Car(Object_):
    type = "car"
    vehiclePlate: str = ""

    def json(self) -> dict:
        objectJson = super().json()
        objectJson.update({'vehiclePlate': self.vehiclePlate })
        objectJson.update({'type': self.type})
        return objectJson

