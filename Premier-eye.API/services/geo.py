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


def getLatLongDistance(lat1: int, lon1: int, lat2: int, lon2: int):
    R = 6371e3; # metres
    φ1 = (lat1 * math.pi) / 180; # φ, λ in radians
    φ2 = (lat2 * math.pi) / 180
    Δφ = ((lat2 - lat1) * math.pi) / 180
    Δλ = ((lon2 - lon1) * math.pi) / 180
    a = math.sin(Δφ / 2) * math.sin(Δφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ / 2) * math.sin(Δλ / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = R * c; # in metres
    return d

# лист из 4 элементов в нужном порядке
def getTrapeziumHeight(leftMinBaseViewLatLon, rightMinBaseViewLocation, leftMaxBaseViewLatLon, rightMaxBaseViewLocation):
    smallBase = getLatLongDistance(leftMinBaseViewLatLon.lat, leftMinBaseViewLatLon.lng, rightMinBaseViewLocation.lat, rightMinBaseViewLocation.lng)
    bigBase = getLatLongDistance(leftMaxBaseViewLatLon.lat, leftMaxBaseViewLatLon.lng, rightMaxBaseViewLocation.lat, rightMaxBaseViewLocation.lng);
    c = getLatLongDistance(rightMinBaseViewLocation.lat, rightMinBaseViewLocation.lng, leftMaxBaseViewLatLon.lat, leftMaxBaseViewLatLon.lng) # а вот тут можно ошибиться и получить диагонали
    d = getLatLongDistance(leftMinBaseViewLatLon.lat, leftMinBaseViewLatLon.lng, camera03[3].lat, camera03[3].lng)

    dividend = (bigBase - smallBase) ** 2 + c ** 2 - d ** 2
    divider = 2 * (bigBase - smallBase)
    inBigFract = (dividend / divider) ** 2

    res = c ** 2 - inBigFract
    return Math.sqrt(res)