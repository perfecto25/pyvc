# PyVC
## Background
PyVC is a Python framework for accessing and manipulating VMs inside a vCenter. Its based on VMWare's PyVMOMI package and community samples: [PyVMOMI](https://github.com/vmware/pyvmomi-community-samples)

I found the community samples to be a bit scattered and hard to pick up for first time users, so I made PyVC as a centralized, focused framework for easily accessing vCenter and working with VMs via a single Python script. 

### Requirements
 - Linux OS
 - Python 2.7+
 - PIP installed (Python package manager)


### Installation
Git clone this repository
```bash
cd /home/user
git clone git@github.com:perfecto25/pyvc.git
``` 

Run to install necessary Python packages
```bash
pip install -r requirements.txt
```
Open up **creds.yaml** and edit the vCenter login information, for example

```yaml
# NYC vcenter
NYC:
  hostname: nyc01.company.com
  user: vcuser
  password: C0w@bung@!

# BOSTON vcenter
BOS:
  hostname: bos04.company.com
  user: vcbos
  password: F@ncyP@nts
```
Optional: add the 'pyvc' script to your /usr/bin
```bash
sudo ln -s /home/user/pyvc/pyvc /usr/bin/pyvc
```

## Usage
```./pyvc (vCenter) (action) (additional)```

---
### List of Available Actions

> **INFO** - returns information for VMs in datacenter
> 
>  Parameters: 
> - all
> - vm-name
> - json
> - names
  
  **Examples:**
  
  Get all VMs
  
  ```./pyvc -vc NYC -a info --get all```
  
  ```bash
    Name       :  nycdb06
    Path       :  [nycesx-vol7] nyc_build/win2008r2.vmx
    Guest      :  Microsoft Windows Server 2008 R2 (64-bit)
    State      :  poweredOn
    IP         :  12.125.20.129
    ----------------------------------------------
    Name       :  nycapp01
    Path       :  [nycesx-vol6] nyc_build/win2008r2.vmx
    Guest      :  Microsoft Windows Server 2008 R2 (64-bit
    etc
  ```

  Get specific VM name
  
  ```./pyvc -vc NYC -a info --get nycweb01```
  ```bash
    Name       :  nycweb01
    Path       :  [nycesx-vol7] nyc_build/win2008r2.vmx
    Guest      :  Microsoft Windows Server 2008 R2 (64-bit)
    State      :  poweredOn
    IP         :  12.125.20.129
  ```

  Get just names of all VMs
  
  ```./pyvc -vc NYC -a info --get names```
  ```bash
    nycweb01
    nycdb02
    nycdb03
    nycapp07
    etc
  ```

  Get JSON output for all VMs
  
  ```./pyvc -vc NYC -a info --get json```
  ```json
    {"nycweb01": {"ip": "12.135.25.134", "path": "[nycesx-vol7] vSphere Replication Appliance/vSphere Replication Appliance.vmx", "state": "poweredOn", "guest": "SUSE Linux Enterprise 11 (64-bit)", "annotation": "vSphere Replication Appliance"}, "centos6.4": {"path": "[nycesx-ssd] centos7.2/centos7.2.vmx", "state": "poweredOff",  etc etc
  ```
    
  You can also prettify the json output

    pyvc -a infoall -vc NJO --get json | jq .


___


**CLONE** - clones an existing VM or Template
> 
>  Parameters: 
> - -t, --template (VM Template)
> - -dc, --datacenter (DC to clone to)
> - -vm
> - names

- Example: ```./pyvc -vc NYC -a clone -t ubuntu_template
     -vm nycapp04 -dc NYC5```
    ```bash
    VM Template: ubuntu_template
    Target VM name: nycapp04
    Datacenter: NYC5
    VM Folder: None
    Datastore: None
    Cluster: None
    Resource Pool: None
    Power On: False
    cloning VM...
    ```
  Required parameters
  - *-vc, --vcenter* Name of vCenter to connect to (from creds.yaml)
  - *-a, --action* Action to take
  - *-t, --template* Name of VM or Template from which to clone from
  - *-vm, --vm-name* Name of target VM to be created
  
  Optional parameters

  - *-dc, --datacenter* Datacenter name of target cloned VM
  - *-vmf, --vm-folder* VM folder name of target cloned VM
  - *-ds, --datastore* Datastore name of target cloned VM
  - *-c, --cluster* Cluster name of target cloned VM
  - *-rp, --resource-pool* Resource Pool name of target cloned VM
  - *--power-on* Turn cloned VM on after cloning (Default is off)
---
## PyVC API
PyVC can also be used via API calls.

PyVC uses Python Flask web framework to run a web listener which actively listens on default port 8320. Whenever a request comes in, Flask routes the request to a specific function which then runs vCenter PyVMOMI modules

To run PyVC across the network, set the listener to run on 0.0.0.0 instead of 127.0.0.1 (localhost)

## Usage:
to start the Flask web listener, run ```./restartAPI.sh```

This will start the web listener on port 8320. Once the listener is up, you can send API requests to it.

### INFO 
get info on VMs

Example: get all VMs
```bash
curl -H 'Content-Type: application/json' -X POST http://localhost:8320/api/info -d '{"vc":"NYC", "get":"all"}'
```
to get JSON output use ```"get":"json"```

to get a specific VM use ```"get":"VM-Name"```

to get only Names use ```"get":"names"```


---
### CLONE
Clone an existing VM

Required parameters
  - *"vc"* Name of vCenter to connect to (from creds.yaml)
  - *"template"* Name of VM or Template from which to clone from
  - *"vm"* Name of target VM to be created
  
Optional parameters

  - *"datacenter"* Datacenter name of target cloned VM
  - *"vmfolder"* VM folder name of target cloned VM
  - *"datastore"* Datastore name of target cloned VM
  - *"cluster"* Cluster name of target cloned VM
  - *"rpool"* Resource Pool name of target cloned VM
  - *"power_on"* set to True to leave cloned VM on (to leave Off, dont include power_on in your json request data)

Example: clone 
```bash
curl -H 'Content-Type: application/json' -X POST http://localhost:8320/api/clone -d '{"vc":"NYC", "template":"ubuntu16_templ","datacenter":
"desw02a","vm":"myTestVM", "datastore":"ds-200", "cluster":"cl003", "rpool":"rp3", "power_on":"True"}' | jq .
```
Output
```json
{
  "RPOOL": "rp933",
  "POWER_ON": "True",
  "DATACENTER": "dc1",
  "TARGET NAME": "vm1",
  "VM TEMPLATE": "abc",
  "CLUSTER": "cl003",
  "DATASTORE": "ds9",
  "RESULT":  "clone done"
}
```

## To Do
package this into PyPI, add more Actions, add user auth