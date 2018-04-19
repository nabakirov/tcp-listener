
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import requests
import logging
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='log.log', level=logging.INFO)


inobi_url = 'http://inobi:4325'
InobiServer = inobi_url + '/transport'
Changer = 'http://transport_changer:4040'

s = requests.Session()

def get_token(username='transport_changer',pwd='transport_changer'):
    r = s.get(inobi_url + '/app/v2/login', params=dict(username=username, pwd=pwd))
    if r.status_code != 200:
        logging.info('login failed {}'.format(r.json))
        return None
    else:
        return r.json()['token']


def refresh():
    r = s.get(InobiServer + '/socketio/check')
    if r.status_code == 200:
        time.sleep(3)
        s.get(InobiServer + '/socketio/delete')


def check_transport(on_timer=False):
    try:
        if on_timer:
            r = s.get(Changer + '/checkOnTimer')
        else:
            r = s.get(Changer + '/check')
        if r.status_code == 200:
            token = get_token()
            if not token:
                raise Exception('login failed')
            data = r.json()
            results = data['results']

            logging.info('CHANGED {} | ONLINE {} | OFFLINE {}'.format(data['changed'], data['online'], data['offline']))
            for k, v in results.items():

                save = s.patch(InobiServer + '/v2/buses', params=dict(jwt=token), json=v['request'])
                logging.info('{} {} {}'.format(k, v['from']['id'], v['to']['id']))
        else:
            logging.info('SERVER UNSWERED {}'.format(r.text))
    except Exception as e:
        logging.info('error {}'.format(e))




if __name__ == '__main__':
    now = datetime.datetime.now()
    date = now + datetime.timedelta(days=1)
    hour10 = date.replace(hour=10, minute=0, second=0, microsecond=0)
    hour13 = date.replace(hour=13, minute=0, second=0, microsecond=0)
    hour18 = date.replace(hour=18, minute=0, second=0, microsecond=0)

    sched = BlockingScheduler()
    sched.add_job(check_transport, 'interval', days=1, start_date=hour10, kwargs=dict(on_timer=True))
    sched.add_job(check_transport, 'interval', days=1, start_date=hour13)
    sched.add_job(check_transport, 'interval', days=1, start_date=hour18)
    sched.add_job(refresh, 'interval', seconds=30)
    sched.start()


    
    

    


