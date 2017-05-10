'''
PYVC UTILITIES
'''

from __future__ import print_function
from pyVim.connect import SmartConnectNoSSL, Disconnect
import atexit
import sys
import os
import yaml
import argparse

def connect(host, user, password):
    # Connect to VCENTER
    try:
        si = SmartConnectNoSSL(host=host, user=user, pwd=password)
        atexit.register(Disconnect, si)
        return si
    except vim.fault.InvalidLogin:
        raise SystemExit("Unable to connect to host with supplied credentials.")

def get_config(*args):
    conf_file = args[0]

    # check if config file is present
    if not os.path.exists(conf_file):
        print('No config file present: %s' % conf_file)
        sys.exit()

    # read YAML
    try:
        with open(conf_file, 'r') as f:
            conf = yaml.load(f)
            argList = list(args)  # convert tuple to list
            argList.pop(0)  # remove conf file from list

            # create lookup path
            parsepath = "conf"

            for arg in argList:
                parsepath = parsepath + "['" + arg + "']"

            try:
                return eval(parsepath)
            except:
                print('Error reading value for %s' % parsepath)
                sys.exit()
    except:
        print('Error reading creds file')
        sys.exit()


# get arguments
def get_args():
    ''' Get arguments '''
    parser = argparse.ArgumentParser(
        prog='pyvc.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='arguments for PyVC',
        epilog='''\
        usage:
            get info for specific VM
                >> ./pyvc -vc $vCenterName -a info -v $VM-Name
            
            get info on all VMs
                >> ./pyvc -vc $vCenterName -a infoall
            
            clone a VM
                >> ./pyvc -vc $vCenterName -a clone -vm $TargetName -t $TemplateName 
                optional arguments:-dc $DataCenterName -vmf $VM-FolderName -ds $DataStoreName -cn $ClusterName -rp $ResourcePool --power-on 
            
            etc etc

        ''')

    parser.add_argument('-vc', '-vcenter',
                        required=True,
                        action='store',
                        help='name of vcenter to connect to, stored in your creds.yaml')

    parser.add_argument('-a', '--action',
                        required=True,
                        action='store',
                        help='action to take: "info", "clone", "delete", etc')

    parser.add_argument('-vm', '--vm-name',
                        required=False,
                        dest='vmname',
                        default=None,
                        action='store',
                        help='Name of the target VM')
    
    parser.add_argument('-g', '--get',
                        required=False,
                        dest='get',
                        default=None,
                        action='store',
                        help='get values for:')

    parser.add_argument('-t', '--template',
                        required=False,
                        action='store',
                        help='Name of the template/VM you are cloning from')

    parser.add_argument('-dc', '--datacenter',
                        required=False,
                        dest='datacenter',
                        action='store',
                        default=None,
                        help='Name of the Datacenter you\
                            wish to use. If omitted, the first\
                            datacenter will be used.')

    parser.add_argument('-vmf', '--vm-folder',
                        required=False,
                        dest='vmfolder',
                        action='store',
                        default=None,
                        help='Name of the VMFolder you wish\
                            the VM to be dumped in. If left blank\
                            The datacenter VM folder will be used')

    parser.add_argument('-ds', '--datastore',
                        required=False,
                        dest='datastore',
                        action='store',
                        default=None,
                        help='Datastore you wish the VM to end up on\
                            If left blank, VM will be put on the same \
                            datastore as the template')

    parser.add_argument('-c', '--cluster',
                        required=False,
                        dest='cluster',
                        action='store',
                        default=None,
                        help='Name of the cluster you wish the VM to\
                            end up on. If left blank the first cluster found\
                            will be used')

    parser.add_argument('-rp', '--resource-pool',
                        required=False,
                        dest='rpool',
                        action='store',
                        default=None,
                        help='Resource Pool to use. If left blank the first\
                            resource pool found will be used')

    parser.add_argument('--power-on',
                        dest='power_on',
                        required=False,
                        action='store_true',
                        help='power on the VM after creation, default is Power Off')




    parser.set_defaults(power_on=False)
    args = parser.parse_args()

    return args