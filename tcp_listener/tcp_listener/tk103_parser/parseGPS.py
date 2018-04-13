from .tracker import parseData


def Parse(raw_gps):

    raw_gps = raw_gps.decode('utf-8')
    if raw_gps[0] == '(' and raw_gps[-1] == ')':
        id = raw_gps[1:13]
        cmd = raw_gps[13:17]
        if cmd == 'BP00':
            # hand shake

            result = dict(request_type='HandShake', code='BP00', data='({}AP01HSO)'.format(id))
        elif cmd == 'BP05':
            # hand shake

            result = dict(request_type='HandShake', code='BP05', data='({}AP05)'.format(id))
        elif cmd == 'BZ00':
            # network
            print('network')
            result = dict(request_type='Network', code='BZ00')
        elif cmd == 'ZC20':
            # battery
            print('battery')
            result = dict(request_type='Battery', code='ZC20')
        elif cmd == 'BR00' or cmd == 'BR01':
            if raw_gps[23] == 'A':
                tracker = parseData(raw_gps)
                if cmd == 'BR00':
                    result = dict(request_type='Data', code='BR00', data=tracker)
                else:
                    result = dict(request_type='Data', code='BR01', data=tracker)
            else:
                result = dict(request_type='BadRequest', code='', data='')
        else:
            result = dict(request_type='Unknown', code='', data='')

    else:
        result = dict(request_type='Unknown', code='', data='')

    return result
