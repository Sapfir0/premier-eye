import math
from services.functionalTools import compose

imageWidth = 1920
imageHeight = 1080

def addLatLon(A, B):
    return {'lat': (A['lat'] + B['lat']), 'lng': (A['lng'] + B['lng']) }

def subLatLon(A, B):
    return {'lat': (A['lat'] - B['lat']), 'lng': (A['lng'] - B['lng']) }

def divLatLonToNumber(A, divider):
    return {'lat': A['lat'] / divider, 'lng': A['lng'] / divider }

def mulLatLonToNumber(A, multiplier):
    return {'lat': A['lat'] * multiplier, 'lng': A['lng'] * multiplier }

def calibrateRect(A, B, C, D, X, Y):
    vBC = divLatLonToNumber(subLatLon(C, B), imageHeight)
    vAD = divLatLonToNumber(subLatLon(D, A), imageHeight)
    latlonPixel1 = addLatLon(mulLatLonToNumber(vBC, imageHeight- Y), B)
    latlonPixel2 = addLatLon(mulLatLonToNumber(vAD, imageHeight - Y), A)
    vG = divLatLonToNumber(subLatLon(latlonPixel2, latlonPixel1), imageWidth)
    G = addLatLon(mulLatLonToNumber(vG, X), latlonPixel1)
    return G

