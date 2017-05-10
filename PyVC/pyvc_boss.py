#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
from PyVC import *


''' This script is the main router for all actions '''

args = get_args()

allowed_actions = ['info', 'infoall', 'clone']

# check action
if not args.action in allowed_actions:
    print('please use a valid action:')
    for a in allowed_actions:
        print('- '+a)
    sys.exit()


cred_file = os.getcwd() + '/creds.yaml'

# get login for vcenter
host = get_config(cred_file, args.vc, 'hostname')
user = get_config(cred_file, args.vc, 'user')
password = get_config(cred_file, args.vc, 'password')

# connection object 'si'
si = connect(host, user, password )


##  ROUTE ACTIONS

# info
if args.action == 'info':
    if not args.vmname:
        print('please provide target VM name: -vm VM-Name')
    else:
        print('getting VM info for %s' % args.vmname)
        get_vm_info(args.vmname, si)

# infoall
if args.action == 'infoall':
    print('getting info for all VMs..')
    get_all_vms(si)

# clone
if args.action == 'clone':
    if not args.template:
        print('please provide a VM template to clone from: -t TemplateName')
    elif not args.vmname:
        print('please provide a target VM clone name: -vm TargetName')
    else:
        print('VM Template: %s' % args.template)
        print('Target VM name: %s' % args.vmname)
        print('Datacenter: %s' % args.datacenter)
        print('VM Folder: %s' % args.vmfolder)
        print('Datastore: %s' % args.datastore)
        print('Cluster: %s' % args.cluster)
        print('Resource Pool: %s' % args.rpool)
        print('Power On: %s' % args.power_on)

        clone(si, args.template, args.vmname, args.datacenter, args.vmfolder, 
              args.datastore, args.cluster, args.rpool, args.power_on)
# etc