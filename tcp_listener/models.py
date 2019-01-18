from . import settings


class Message:
    id_key = settings.ID_KEY
    raw_key = settings.RAW_KEY
    lat_key = settings.LAT_KEY
    lng_key = settings.LNG_KEY
    speed_key = settings.SPEED_KEY
    bearing_key = settings.BEARING_KEY
    timestamp_key = settings.TIMESTAMP_KEY

    def __init__(self, id=None, type=None, raw=None, lat=None, lng=None, speed=None, bearing=None, timestamp=None):
        self.id = id
        self.type = type
        self.raw = raw
        self.lat = lat
        self.lng = lng
        self.speed = speed
        self.bearing = bearing
        self.timestamp = timestamp
        self.is_full = False

    def as_dict(self):
        return {
            self.id_key: self.id,
            self.lat_key: self.lat,
            self.lng_key: self.lng,
            self.speed_key: self.speed,
            self.bearing_key: self.bearing,
            self.timestamp_key: self.timestamp
        }

    @property
    def query_params(self):
        return "&".join(["{}={}".format(k, v) for k, v in self.as_dict().items() if v])

    @property
    def full_url(self):
        return "{}?{}".format(settings.REQUEST_URL, self.query_params)
