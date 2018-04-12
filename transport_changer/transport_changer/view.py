from transport_changer import app
from flask import request, abort, render_template, jsonify
from .utils import getargs
from .load_data.fetch import fetchData, fetchRoute, fetchLines
from transport_changer.configs import inobi_conn, traccar_conn
from .load_data.calculate import calc
from .notify import mail_send
import psycopg2




@app.route('/api/bus/route')
def getBusRoute():
    busId = getargs(request, 'id')[0]
    if not busId:
        return abort(400)

    with psycopg2.connect(traccar_conn) as conn:
        data = fetchData(busId, conn)
        l = []
        for point in data:
            l.append(list(point))
        return jsonify(l), 200


@app.route('/api/route/list')
def getRouteList():
    with psycopg2.connect(inobi_conn) as conn:
        data = fetchLines(conn) 
        return jsonify(data)


@app.route('/api/line/route')
def getLineRoute():
    line_id = getargs(request, 'id')[0]
    if not line_id:
        return abort(400)

    with psycopg2.connect(inobi_conn) as conn:
        data = fetchRoute(line_id, conn)

        return jsonify(data), 200


@app.route('/map')
def mapRender():
    return render_template('checkOnMap.html')


@app.route('/check', methods=['POST', 'GET'])
def change():
    emails = getargs(request, 'emails')[0]
    result = calc(short=False)
    msg = 'Subject: {} Changed\n\n'.format(result['changed'])
    for k, v in result['results'].items():
        if k == 'request':
            continue
        msg += '{}\n'.format(v['mac'])
        msg += 'Percent {} \n'.format(v['percent'])
        msg += '\tFrom {} {}\n'.format(v['from']['name'], v['from']['type'])
        msg += '\tTo   {} {}\n'.format(v['to']['name'], v['to']['type'])
        msg += '------------------------------------------------\n'
    msg += '\n{} Online\n{} Changed\n{} Offline'.format(result['online'], result['changed'], result['offline'])
    if emails:
        mail_send(msg, emails=emails)
    return jsonify(result), 200


@app.route('/checkOnTimer')
def checkOnTimer():
    result = calc()
    msg = 'Subject: {} Changed\n\n'.format(result['changed'])
    for k, v in result['results'].items():
        if k == 'request':
            continue
        msg += '{}\n'.format(v['mac'])
        msg += 'Percent {} \n'.format(v['percent'])
        msg += '\tFrom {} {}\n'.format(v['from']['name'], v['from']['type'])
        msg += '\tTo   {} {}\n'.format(v['to']['name'], v['to']['type'])
        msg += '------------------------------------------------\n'
    msg += 'Verify the changes http://transport.inobi.kg:4040/map\n'

    msg += '\n{} Online\n{} Changed\n{} Offline'.format(result['online'], result['changed'], result['offline'])

    mail_send(msg, emails=['nabakirov@gmail.com'])
    return msg, 200
