

from tcp_listener import configs
import json
from twisted.web.client import Headers

from .bytesprod import BytesProducer


def Request(tracker, agent):
    if tracker['request_type'] == 'Data':
        gps = tracker['data']

        header = dict()

        if configs['request_method'] == 'POST':
            if configs['TOKEN']:
                header['Authorization'] = [configs['TOKEN']]
            header['Content-Type'] = ['application/json']
            body = BytesProducer(json.dumps(gps).encode())
            request = agent.request(b'POST',
                                    configs['URL'].encode(),
                                    Headers(header),
                                    body)
            request.addErrback(print)
            request.addCallback(lambda status: dict(status='ok', data=status))
        elif configs['request_method'] == 'GET':
            args_string = '?' + '&'.join('{0}={1}'.format(k, v) for k, v in gps.items())
            url = configs['URL'] + args_string

            if configs['TOKEN']:
                header['Authorization'] = [configs['TOKEN']]
                request = agent.request(b'GET',
                                        url.encode(),
                                        Headers(header))
                request.addErrback(print)
                request.addCallback(lambda status: dict(status='ok', data=status))
            else:
                request = agent.request(b'GET',
                                        url.encode())
                request.addErrback(print)
                request.addCallback(lambda status: dict(status='ok', data=status))


def testReq(agent):
    d = agent.request(b'GET', b'http://176.123.244.5/v1/admin/login')
    d.addBoth(print)


