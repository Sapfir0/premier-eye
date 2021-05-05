import unittest
from services.geo import calibrateRect, divLatLonToNumber, subLatLon, addLatLon, mulLatLonToNumber, imageHeight, imageWidth
from cameraLocations import cameras

def getLatLonCoordinates(A, B, C, D, X, Y):
    vBC = divLatLonToNumber(subLatLon(C, B), imageHeight)
    vAD = divLatLonToNumber(subLatLon(D, A), imageHeight)
    latlonPixel1 = addLatLon(mulLatLonToNumber(vBC, imageHeight- Y), B)
    latlonPixel2 = addLatLon(mulLatLonToNumber(vAD, imageHeight - Y), A)
    vG = divLatLonToNumber(subLatLon(latlonPixel2, latlonPixel1), imageWidth)
    G = addLatLon(mulLatLonToNumber(vG, X), latlonPixel1)
    return G



class Test_Math(unittest.TestCase):
    def test_isMathEqual(self):
        etalon = getLatLonCoordinates(*cameras[3]['view'], int(917.5), int(540))
        newRes = calibrateRect(*cameras[3]['view'], int(917.5), int(540))
        self.assertEqual(etalon, newRes)


if __name__ == '__main__':
    unittest.main()