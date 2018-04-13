from twisted.internet import reactor, endpoints
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.client import Agent
import time
from datetime import datetime
import json

agent = Agent(reactor)
configs = dict()

from math import radians, cos, sin, asin, sqrt, atan2, degrees


import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='log.log', level=logging.INFO)

def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r



def getSpeed(point1, point2):
    dist = haversine(point1['lng'], point1['lat'], point2['lng'], point2['lat'])
    time_s = point2['timestamp'] - point1['timestamp']
    time_h = time_s / 3600
    if time_h != 0:
        speed_kph = dist / time_h
    else:
        speed_kph = 0
    return round(speed_kph, 3)

def getBearing(point1, point2):

    lng1, lat1, lng2, lat2 = map(radians, [point1['lng'], point1['lat'], point2['lng'], point2['lat']])

    dlng = lng2 - lng1
    y = sin(dlng) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlng)
    bearing = degrees(atan2(y, x))
    return round((bearing + 360) % 360, 3)


Points = dict()

class ClockPage(Resource):
    isLeaf = True

    def render_GET(self, request):
        return 'send POST'    

    def render_POST(self, request):
        bytedata = request.content.getvalue()
        try:
            newdata = json.loads(bytedata.decode())
        except:
            return 'invalid data'
        null = False
        if int(newdata['lat']) != 0 or int(newdata['lng']) != 0:
            oldPoint = Points.get(newdata['id'])
            if oldPoint:
                newdata['timestamp'] = int(time.time())
                newdata['speed'] = getSpeed(oldPoint, newdata)
                newdata['bearing'] = getBearing(oldPoint, newdata)
            else:
                newdata['timestamp'] = int(time.time())
                newdata['speed'] = 0
                newdata['bearing'] = 0
            Points[newdata['id']] = newdata
           
        else:
            null = True
            newdata['timestamp'] = int(time.time())
            newdata['speed'] = 0
            newdata['bearing'] = 0
            
        item = configs['send_to']
        id, lat, lng, timestamp, speed, bearing = item['var']['id'], item['var']['lat'], item['var']['lng'], item['var'].get('timestamp'), item['var'].get('speed'), item['var'].get('bearing')
        data = {
            id: newdata['id'],
            lat: newdata['lat'],
            lng: newdata['lng']
        }
        if timestamp:
            data[timestamp] = newdata['timestamp']
        if speed:
            data[speed] = newdata['speed']
        if bearing:
            data[bearing] = newdata['bearing']
        for k, v in newdata.items():
            if k not in ['id', 'lat', 'lng', 'timestamp', 'speed', 'bearing']:
                data[k] = v
        if item['send_nulls']:
            send = True
        elif not null:
            send = True
        elif null and not item['send_nulls']:
            send = False
        else:
            send = True
        if send:
            
            try:
                logging.info(' '.join(['{}={}'.format(k, v) for k, v in data.items()]))
                # logging.debug('{} {} {} {} {}'.format(datetime.now(), item['method'], newdata['id'], newdata['lat'], newdata['lng']))
                if item['method'] == 'POST':
                    newbytes = json.dumps(data).encode()
                    d = agent.request(item['method'].encode(), item['url'].encode(), request.requestHeaders, BytesProducer(bytedata))
                elif item['method'] == 'GET':
                    url = item['url'] + '?' + '&'.join(['{}={}'.format(a, b) for a, b in data.items()])
                    d = agent.request(item['method'].encode(), url.encode())
                timeoutCall = reactor.callLater(2, d.cancel)
                def completed(passthrough):
                    if timeoutCall.active():
                        timeoutCall.cancel()
                    return passthrough
                d.addBoth(completed)
                d.addErrback(lambda *args, **kwargs: logging.exception("@errback:{args} {kwargs}".format(args=args, kwargs=kwargs)))
            except:
                logging.info('error cant send data {}'.format(newdata))
            
        return b'ok'




from zope.interface import implementer

from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer

@implementer(IBodyProducer)
class BytesProducer(object):
    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass



if __name__ == '__main__':
    required = ['var', 'url', 'method', 'name', 'send_nulls']
    var_required = ['lat', 'lng', 'id']
    import sys, imp

    try:
        configs_filepath = sys.argv[1]
    except Exception as e:
        print('config parameter needed')
        sys.exit(0)
    raw_configs = imp.load_source(configs_filepath, configs_filepath)
    
    for item in ['port_to_listen', 'send_to']:
        try:
            configs[item] = raw_configs.__dict__[item]
        except:
            raise Exception(item, 'is missing')
    
    
    for item in required:
        if item not in configs['send_to']:
            raise Exception(item, 'is missing')
    for var in var_required:
        if var not in configs['send_to']['var']:
            raise Exception(var, 'is missing in var')

    print('STARTED LISTEN PORT {}'.format(configs['port_to_listen']))
    resource = ClockPage()
    factory = Site(resource)
    endpoint = endpoints.TCP4ServerEndpoint(reactor, configs['port_to_listen'])
    endpoint.listen(factory)
    reactor.run()
