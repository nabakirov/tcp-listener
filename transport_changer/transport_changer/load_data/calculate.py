from .fetch import fetchBusList, fetchData, fetchRoute, fetchLineData
from .base_line_init import lineInit
from collections import Counter
import psycopg2
import operator
from transport_changer.configs import PERCENT_SCALE, inobi_conn, traccar_conn



def calc(short=True):
    with psycopg2.connect(inobi_conn) as iconn:
    
        with psycopg2.connect(traccar_conn) as tconn:

            busList = fetchBusList(iconn)
            response = dict()
            results = dict()
            baseLine = dict()
            linePoints = dict()
            onlineCounter = 0
            offlineCounter = 0
            changedCounter = 0
            for bus in busList:
                route = fetchRoute(bus['line_id'], iconn)
                lineInit(route, bus['line_id'], baseLine, linePoints)

            for i, bus in enumerate(busList):

                counter = Counter()
                traccarBus = bus['mac']

                busHistory = fetchData(traccarBus, tconn)

                coordsList = set()
                for position in busHistory:
                    coords = (round(position[0], 3), round(position[1], 3))
                    coordsList.add(coords)
                for coords in coordsList:
                    for lineId in baseLine.get(coords, []):
                        counter[lineId] += 1
                if counter:
                    onlineCounter += 1
                    p = dict()
                    tmp = dict()
                    for c in counter.most_common(5):
                        id, cnt = c

                        percent = cnt * 100 / (linePoints[id] / 2)
                        cres = dict(count=cnt,
                                    percent=percent)
                        tmp[id] = cres

                        p[id] = percent
                    sortedP = sorted(p.items(), key=operator.itemgetter(1), reverse=True)
                    id, percent = sortedP[0]
                    if bus['line_id'] != id and percent >= PERCENT_SCALE and tmp[id]['count'] >= 100:
                        changedCounter += 1
                        fromLine = fetchLineData(bus['line_id'], iconn)
                        toLine = fetchLineData(id, iconn)
                        results[bus['mac']] = dict(mac=bus['mac'], data=dict())
                        results[bus['mac']]['from'] = fromLine
                        results[bus['mac']]['to'] = toLine
                        if not short:
                            results[bus['mac']]['data'] = tmp
                        results[bus['mac']]['percent'] = percent

                        if not short:
                            bus['line_id'] = toLine['id']
                            results[bus['mac']]['request'] = bus
                else:
                    offlineCounter += 1
            iconn.close()
            tconn.close()
            response['results'] = results
            response['online'] = onlineCounter
            response['changed'] = changedCounter
            response['offline'] = offlineCounter
            return response




