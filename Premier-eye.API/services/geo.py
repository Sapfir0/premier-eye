import math

imageWidth = 1920
imageHeight = 1080

def calibrateRect(A, B, C, D):
    calibratedImage = []
    latOffset = (A['lat'] - B['lat']) / imageWidth
    lonOffset = (A['lng'] - B['lng']) / imageWidth
    for w in range(1, imageWidth):
        row = []
        for h in range(1, imageHeight):
            row.append({'lat': A['lat'] + (latOffset * h ), 'lng': A['lng'] + (lonOffset * w)})
        calibratedImage.append(row)   
    return calibratedImage


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