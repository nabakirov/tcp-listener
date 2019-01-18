from . import Adapter
from ..models import Message
from datetime import datetime


def DMCtoDD(coord):
    '''
    converts Degrees Minutes Seconds to Decimal Degrees
    :param coord: float - degreesMinutes.second
    :return: float - decimal degrees

    example:
    DMStoDD(07435.4832) -> 74.591387
    '''
    coord = float(coord)
    deg = int(coord / 100)
    mins = coord - (deg * 100)
    return round(deg + mins / 60, 6)


def to_timestamp(date):
    if len(date) != 6:
        return False
    time = int(datetime.strptime('{0}-{1}-{2} {3}:{4}:{5}'.format(*date), '%y-%m-%d %H:%M:%S').timestamp()) + 21600
    return time


def parse_date(date):
    a = int(date[0:2])
    b = int(date[2:4])
    c = int(date[4:6])
    return (a, b, c)


class TK103(Adapter):

    @classmethod
    def decode(cls, datastring):
        try:
            message = Message()
            message.lat = DMCtoDD(datastring[24:33])
            message.lng = DMCtoDD(datastring[34:44])
            message.id = datastring[1:13]
            message.timestamp = to_timestamp(parse_date(datastring[17:23]) + parse_date(datastring[50:56]))
            message.speed = float(datastring[45:48])
            message.bearing = int(datastring[56:59])
        except:
            return None
        else:
            return message

    @classmethod
    def response_to(cls, datastring):
        return None
