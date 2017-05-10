#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, abort
import os
import sys
import io
from contextlib import contextmanager # stdout in memory

from PyVC.infoall import get_all_vms
from PyVC import utils

@contextmanager
def stdout_redirector(stream):
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout


cred_file = os.getcwd() + '/creds.yaml'

def get_si(vc):
    # get login for vcenter
    host = utils.get_config(cred_file, vc, 'hostname')
    user = utils.get_config(cred_file, vc, 'user')
    password = utils.get_config(cred_file, vc, 'password')

    # connection object 'si'
    return utils.connect(host, user, password )


app = Flask(__name__)

''' ROUTE api actions '''

# INFOALL
@app.route('/api/infoall', methods=['POST'])
def infoall():
    if not request.json or not 'vc' in request.json:
        abort(400)
    si = get_si(request.json['vc'])

    f = io.StringIO()
    with stdout_redirector(f):
        get_all_vms(si)
    return f.getvalue


    
    
    return sys.stdout #return value

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8320, debug=True)