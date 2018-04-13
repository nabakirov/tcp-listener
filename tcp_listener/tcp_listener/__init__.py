

configs = dict()
import logging
logging.basicConfig(filename='log.log', level=logging.DEBUG)

def run(configs_module=None):
    require = ['LISTENER_PORT', 'URL', 'request_method', 'id', 'lat', 'lng', 'timestamp', 'speed', 'bearing']

    for check in require:
        if check not in configs_module.__dict__.keys():
            print('require {} in configs'.format(check))
            return

    global configs

    for item in require:
        configs[item] = configs_module.__dict__[item]

    token = configs_module.__dict__.get('TOKEN', False)
    if token:
        configs['TOKEN'] = token
    else:
        configs['TOKEN'] = None
    logging.info('TCP Listener port {}'.format(configs['LISTENER_PORT']))
    logging.info('URL to send requests {}'.format(configs['URL']))
    from .listener import start
    start()
