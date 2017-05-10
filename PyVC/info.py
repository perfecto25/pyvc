#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2015 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

''' Python program for listing the vms on an ESX / vCenter host '''

from __future__ import print_function
from pyVmomi import vim
import json


def PrintVmInfo(vm, vm_dict, depth=1):
    '''
    Print information for a particular virtual machine or recurse into a folder
    or vApp with depth protection
    '''
    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = vm.childEntity
        for c in vmList:
            PrintVmInfo(c, vm_dict, depth+1)
        return

   # if this is a vApp, it likely contains child VMs
   # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
    if isinstance(vm, vim.VirtualApp):
        vmList = vm.vm
        for c in vmList:
            PrintVmInfo(c, vm_dict, depth + 1)
        return

    summary = vm.summary

    # add data to JSON output
    vm_dict[summary.config.name] = {
        'path': summary.config.vmPathName, 
        'guest': summary.config.guestFullName,
        'state': summary.runtime.powerState
        }

    annotation = summary.config.annotation

    if annotation != None and annotation != "":
        vm_dict[summary.config.name]['annotation'] = annotation

    if summary.guest != None:
        ip = summary.guest.ipAddress
        if ip != None and ip != "":
            vm_dict[summary.config.name]['ip'] = ip

    if summary.runtime.question != None:
        vm_dict[summary.config.name]['question'] = summary.runtime.question.text

    return vm_dict

# main function
def get_all_vms(si):
    '''
    Simple command-line program for listing the virtual machines on a system.
    '''

    content = si.RetrieveContent()
    vm_dict = {}

    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmFolder = datacenter.vmFolder
            vmList = vmFolder.childEntity
            for vm in vmList:
                PrintVmInfo(vm, vm_dict)

    retval = json.dumps(vm_dict)
    return retval


# used by BOSS to display all VM info
def display_all(retval):
    data = json.loads(retval)
    for name in data:
        print('Name: %s' % name)
        print('Path: %s' % data[name]['path'])
        print('Guest: %s' % data[name]['guest'])
        if 'annotation' in data[name].keys():
            print('Annotation: %s' % data[name]['annotation'])
        if 'ip' in data[name].keys():
            print('IP: %s' % data[name]['ip'])
        if 'question' in data[name].keys():
            print('Question: %s' % data[name]['question'])
        print('-------------------------------------')

# used by BOSS to display specific VM info
def display_vm(retval, vmname):
    data = json.loads(retval)
    for name in data:
        if name == vmname:
            print('Name: %s' % name)
            print('Path: %s' % data[name]['path'])
            print('Guest: %s' % data[name]['guest'])
            if 'annotation' in data[name].keys():
                print('Annotation: %s' % data[name]['annotation'])
            if 'ip' in data[name].keys():
                print('IP: %s' % data[name]['ip'])
            if 'question' in data[name].keys():
                print('Question: %s' % data[name]['question'])
            print('-------------------------------------')