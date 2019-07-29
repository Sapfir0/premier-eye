from abc import ABC, abstractmethod


class Neural_network(ABC):

    @abstractmethod
    def pipeline(self, filename):
        print("Im you father, network")
        pass

    def extractImages(self):
        return NotImplemented

    def detectMyObjects(self):
        return NotImplemented

    def detectObjects(self):
        return NotImplemented

    def countObjects(self):
        return NotImplemented
