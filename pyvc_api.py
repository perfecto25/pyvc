#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from flask import Flask, request, abort
import os
import sys
import io
import json
import logging


#from PyVC import *
from PyVC.info import get_info_json, display_all, display_vm
from PyVC.clone import clone
from PyVC.utils import connect, get_config



cred_file = os.getcwd() + '/creds.yaml'

def get_si(vc):
    # get login for vcenter
    host = get_config(cred_file, vc, 'hostname')
    user = get_config(cred_file, vc, 'user')
    password = get_config(cred_file, vc, 'password')

    # connection object 'si'
    return connect(host, user, password)


app = Flask(__name__)

''' ROUTE API actions '''


# ERROR & EXCEPTION
@app.errorhandler(404)
def page_not_found(error):
	app.logger.error('Page not found: %s', (request.path))
	return 'Error with request, please check your request call'

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return 'Error with request, please check your request call'


# INFO -------------------------------------------
@app.route('/api/info', methods=['POST'])
def info():

    # check incoming request for params
    required_params = ['vc', 'get']
    for param in required_params:
        if not param in request.json:
            return 'missing parameter: %s' % param

    if not request.json:
        abort(400)

    si = get_si(request.json['vc'])
    jsonval = get_info_json(si) # get total JSON object

    # NAMES
    if request.json['get'] == 'names':
        data = json.loads(jsonval)
        names = ''
        for name in data:
            names = names + '\n' + name
        return names

    # ALL
    elif request.json['get'] == 'all':
        return display_all(jsonval)

    # JSON
    elif request.json['get'] == 'json':
        return jsonval

    # VM Name
    else:
        return display_vm(jsonval, request.json['get'])

#--------------------------------------------- INFO

# CLONE -------------------------------------------
@app.route('/api/clone', methods=['POST'])
def make_clone():

    # check incoming request for params
    required_params = ['vc', 'template', 'vm']
    for r_param in required_params:
        if not r_param in request.json:
            return 'missing parameter: %s' % r_param

    if not request.json:
        abort(400)

    si = get_si(request.json['vc'])

    # Return Message dict
    val = {}
    val['VM TEMPLATE'] = request.json['template']
    val['TARGET NAME'] = request.json['vm']

    # add additional parameters to return message
    optional_params = ['datacenter', 'vmfolder', 'datastore', 'cluster', 'rpool', 'power_on']
    for o_param in optional_params:
        if o_param in request.json:
            val[o_param.upper()] = request.json[o_param]
        else:
            val[o_param.upper()] = None

    # if no power_on provided, set power_on = Flase
    if not val['POWER_ON']:
        val['POWER_ON'] = False
    else:
        val['POWER_ON'] = True

    # Clone it!
    try:
        clone(si, request.json['template'], request.json['vm'], val['DATACENTER'], val['VMFOLDER'], 
                val['DATASTORE'], val['CLUSTER'], val['RPOOL'], val['POWER_ON'])
    except:
        return 'error cloning VM'
    else:
        val['RESULT'] = 'clone done'
        return json.dumps(val)


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    logging.basicConfig(filename='log/pyvc.log', format=log_format, level=logging.DEBUG)
    handler = logging.FileHandler('log/pyvc.log')
    log.addHandler(handler)

    app.run(host='0.0.0.0', port=8320, debug=True, threaded=True)
