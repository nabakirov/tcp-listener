import re
from .adapter import Adapter
from tcp_listener.models import Message
from time import time as now


class MessageTypes:
    INIT = 'init'
    HEARTBEAT = 'heartbeat'
    LOCATION_FULL = 'location_full'
    LOCATION_LOW = 'location_low'


# e.g. ##,imei:865328021048409,A;
re_init = '^##,imei:(?P<imei>\d+),A'
re_init_compiler = re.compile(re_init)

# e.g. 865328021048409;
re_heartbeat = '^(?P<imei>\d+)'
re_heartbeat_compiler = re.compile(re_heartbeat)

# e.g. imei:864180034536487,tracker,180924184758,,F,104752.000,A,3543.6957,N,05129.6419,E,0.00,0;
re_location_full = "^imei:(?P<imei>\d+)," \
                   "tracker,(?P<local_date>\d*)," \
                   "(?P<local_time>\d*)," \
                   "F," \
                   "(?P<time_utc>\d+\.\d+)," \
                   "(?P<validity>[AV])," \
                   "(?P<latitude>\d+\.\d+)," \
                   "(?P<latitude_hemisphere>[NS])," \
                   "(?P<longitude>\d+\.\d+)," \
                   "(?P<longitude_hemisphere>[EW])," \
                   "(?P<speed>\d+\.\d+)," \
                   "(?P<bearing>\d+)"
re_location_full_compile = re.compile(re_location_full)

re_location_low = '^imei:(?P<imei>\d+),' + \
                  'tracker,' + \
                  '(?P<local_date>\d*),' + \
                  '(?P<local_time>\d*),' + \
                  'L,' + \
                  '[^,]*,' + \
                  '[^,]*,' + \
                  '(?P<unknown_1>\w*),' + \
                  '[^,]*,' + \
                  '(?P<unknown_2>\w*),'
re_location_low_compile = re.compile(re_location_low)


class TK102(Adapter):
    @classmethod
    def decode(cls, datastring):
        if re_init_compiler.match(datastring):
            imei = re.match(re_init, datastring).group('imei')
            message = Message(id=imei, type=MessageTypes.INIT, raw=datastring)
        elif re_heartbeat_compiler.match(datastring):
            imei = re.match(re_heartbeat, datastring).group('imei')
            message = Message(id=imei, type=MessageTypes.HEARTBEAT, raw=datastring)
        elif re_location_low_compile.match(datastring):
            match = re_location_low_compile.match(datastring)
            imei = match.group('imei')
            message = Message(id=imei, type=MessageTypes.LOCATION_LOW, raw=datastring)
        elif re_location_full_compile.match(datastring):
            match = re_location_full_compile.match(datastring)
            imei = match.group('imei')
            message = Message(id=imei, type=MessageTypes.LOCATION_FULL, raw=datastring)

            latitude = match.group('latitude')
            latitude_hemisphere = match.group('latitude_hemisphere')
            longitude = match.group('longitude')
            longitude_hemisphere = match.group('longitude_hemisphere')

            # Latitude and Longitude need to be converted from this proto's spec to standard decimal
            # Locations come as HHHHMM.MMMM
            # hours are any number of digits, followed by
            # seconds which are 2-digit integer part, period, fractional part
            re_location = '^(\d+)(\d{2}\.\d+)$'

            (h, m) = re.match(re_location, latitude).groups()
            h = float(h)
            m = float(m)
            latitude = h + m/60
            if 'S' == latitude_hemisphere:
                latitude = -latitude

            (h, m) = re.match(re_location, longitude).groups()
            h = float(h)
            m = float(m)
            longitude = h + m/60
            if 'W' == longitude_hemisphere:
                longitude = -longitude

            message.lat = latitude
            message.lng = longitude

            speed = match.group('speed')
            try:
                speed = float(speed)
            except ValueError:
                speed = None

            bearing = match.group('bearing')
            try:
                bearing = float(bearing)
            except ValueError:
                bearing = None

            message.speed = speed
            message.bearing = bearing
            message.timestamp = int(now())
        else:
            return None
        return message

    @classmethod
    def response_to(cls, message: Message):
        if MessageTypes.INIT == message.type:
            return 'LOAD'
        elif MessageTypes.HEARTBEAT == message.type:
            return 'ON'

        return None

