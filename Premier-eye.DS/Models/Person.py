from Models.Object_ import Object_


class Person(Object_):
    type = "person"

    def json(self) -> dict:
        objectJson = super().json()
        objectJson.update({'type': self.type})
        return objectJson

