import polyline
from datetime import datetime


def fetchData(id, conn):
    with conn.cursor() as cursor:
        sql = '''
        SELECT 
            p.latitude, 
            p.longitude
        FROM positions p
            INNER JOIN devices d
            ON d.id = p.deviceid
        WHERE 
            d.uniqueid = %s AND
            p.fixtime between %s AND %s
    '''
        fromDate = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
        toDate = datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
        params = (id, fromDate, toDate)
        cursor.execute(sql, params)
        data = cursor.fetchall()
        return data


def fetchBusList(conn):
    from json import loads
    with conn.cursor() as cursor:
        sql = '''
        select 
            id,
            device_id,
            line_id,
        from transports
        '''
        cursor.execute(sql)
        data = cursor.fetchall()
        l = []
        for bus in data:
            l.append(
                {
                    "id": bus[0],
                    "mac": bus[1],
                    "line_id": bus[2]
                }
            )
        return l


def fetchRoute(route_id, conn):
    with conn.cursor() as cursor:
        SQL_directions = '''
            select d.line from routes as r
                inner join route_directions as rd
                    on rd.id = r.id
                inner join directions as d
                    on rd.entry_id = d.id
                where r.id = %s
                order by rd.pos
            '''
        cursor = conn.cursor()
        cursor.execute(SQL_directions, (route_id,))
        directions = cursor.fetchall()
        l = []
        for dir in directions:
            l.append(polyline.decode(dir[0]))
        return l


def fetchLineData(line_id, conn):
    SQL = '''
        SELECT id
              ,type
              ,name
        FROM routes
        WHERE id = %s
    '''

    cursor = conn.cursor()
    cursor.execute(SQL, (line_id,))
    raw = cursor.fetchone()
    if raw:
        return dict(
            id=raw[0],
            type=raw[1],
            name=raw[2]
        )
    else:
        return {}


def fetchLines(conn):
    SQL = '''
        SELECT id
              ,type
              ,name
        FROM routes
        WHERE type = 'bus' or type = 'trolleybus'
    '''
    cursor = conn.cursor()
    cursor.execute(SQL)
    data = cursor.fetchall()
    routes = []
    for item in data:
        if item[0] in [3083, 3089, 2678]:
            continue
        routes.append(dict(
            id=item[0],
            type=item[1],
            name=item[2]
        ))
    return routes