'''
Written by Dann Bohn
Github: https://github.com/whereismyjetpack
Email: dannbohn@gmail.com
Clone a VM from template example
'''
from __future__ import print_function

from pyVmomi import vim


def wait_for_task(task):
    ''' wait for a vCenter task to finish '''
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print('there was an error cloning the VM')
            task_done = True


def get_obj(content, vimtype, name):
    '''
    Return an object by name, if name is None the
    first found object is returned
    '''
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj


def clone_vm(
        content, template, vmname, si,
        datacenter, vmfolder, datastore,
        cluster, rpool, power_on):
    '''
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    '''

    # if none git the first one
    datacenter = get_obj(content, [vim.Datacenter], datacenter)

    if vmfolder:
        destfolder = get_obj(content, [vim.Folder], vmfolder)
    else:
        destfolder = datacenter.vmFolder

    if datastore:
        datastore = get_obj(content, [vim.Datastore], datastore)
    else:
        datastore = get_obj(
            content, [vim.Datastore], template.datastore[0].info.name)

    # if None, get the first one
    cluster = get_obj(content, [vim.ClusterComputeResource], cluster)

    if rpool:
        rpool = get_obj(content, [vim.ResourcePool], rpool)
    else:
        rpool = cluster.resourcePool

    # set relospec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = rpool

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on

    print('cloning VM...')
    task = template.Clone(folder=destfolder, name=vmname, spec=clonespec)
    wait_for_task(task)
    print('clone complete')

def clone(si, template, vmname, datacenter, 
          vmfolder, datastore, cluster, rpool, power_on):
    
    '''
    release the Clone!!
    '''

    content = si.RetrieveContent()
    
    #template = None

    template = get_obj(content, [vim.VirtualMachine], template)

    if template:
        try:
            clone_vm(content, template, vmname, si, datacenter,
                     vmfolder, datastore, cluster, rpool, power_on)
        except:
            print('There was an error cloning the VM, please check vCenter logs')
    else:
        print('template not found')


# start this thing
if __name__ == "__main__":
    clone()
