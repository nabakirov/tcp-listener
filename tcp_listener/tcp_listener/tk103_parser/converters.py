from datetime import datetime
KNOT = 1.851999999984


def dateToEpoch(date):

    if len(date) != 6:
        return False
    time = int(datetime.strptime('{0}-{1}-{2} {3}:{4}:{5}'.format(*date), '%y-%m-%d %H:%M:%S').timestamp()) + 21600
    return time
    # return int(datetime.strptime('{0}-{1}-{2} {3}:{4}:{5} -0000'.format(*date), '%y-%m-%d %H:%M:%S %z').timestamp())


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


def parseDate(date):
    a = int(date[0:2])
    b = int(date[2:4])
    c = int(date[4:6])
    return (a, b, c)

def knotToKm(knot):
    if not isinstance(knot, float):
        knot = float(knot)
    return round(knot * KNOT, 6)

if __name__ == '__main__':
    print(knotToKm(69))
