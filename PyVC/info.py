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

'''
Python program for listing the vms on an ESX / vCenter host
'''

from __future__ import print_function

def print_info(vm, target, depth=1):
    '''
    Print information for a particular virtual machine or recurse into a folder
    or vApp with depth protection
    '''
    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return connect(host, user, password )
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = vm.childEntity
        for c in vmList:
            print_info(c, target, depth+1)
        return

    summary = vm.summary
    if summary.config.name == target:
        print("Name        : ", summary.config.name)
        print("Path        : ", summary.config.vmPathName)
        print("Guest       : ", summary.config.guestFullName)
        annotation = summary.config.annotation
        
        if annotation != None and annotation != "":
            print("Annotation : ", annotation)
        
        print("State       : ", summary.runtime.powerState)

        if summary.guest != None:
            ip = summary.guest.ipAddress

        if ip != None and ip != "":
            print("IP          : ", ip)

        if summary.runtime.question != None:
            print("Question  : ", summary.runtime.question.text)
            print("")

def get_vm_info(target, si):
    print('---------------------------------------------')
    content = si.RetrieveContent()

    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmFolder = datacenter.vmFolder
            vmList = vmFolder.childEntity
            for vm in vmList:
                print_info(vm, target)

