# b'(027044720621BR00171107A4252.9237N07434.5465E028.1085345192.1200000001L00000000)'

from .converters import DMCtoDD, dateToEpoch, parseDate, knotToKm
from tcp_listener import configs

def parseData(raw_gps: str):
    lat = DMCtoDD(raw_gps[24:33])
    lng = DMCtoDD(raw_gps[34:44])
    id = raw_gps[1:13]
    timestamp = dateToEpoch(parseDate(raw_gps[17:23]) + parseDate(raw_gps[50:56]))
    speed = knotToKm(raw_gps[45:48])
    bearing = int(raw_gps[56:59])
    gps = {
        configs['id']: id,
        configs['lat']: lat,
        configs['lng']: lng,
        configs['timestamp']: timestamp,
        configs['bearing']: bearing,
        configs['speed']: speed
    }
    return gps
