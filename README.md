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

### Usage
```./pyvc (vCenter) (action) (additional)```

**Actions:**

- **INFO** (*returns information on all VMs in datacenter*)
  - Example: ```./pyvc -vc NYC -a infoall```
    ```bash
    getting info for all VMs..
    Name       :  nycdb06
    Path       :  [nycesx-vol7] nyc_build/win2008r2.vmx
    Guest      :  Microsoft Windows Server 2008 R2 (64-bit)
    State      :  poweredOn
    IP         :  12.125.20.129
    
    Name       :  nycapp01
    Path       :  [nycesx-vol6] nyc_build/win2008r2.vmx
    Guest      :  Microsoft Windows Server 2008 R2 (64-bit

    et
    ```
    pyvc -a infoall -vc NJO --get json | jq .

- **CLONE** (*clone an existing VM or Template*)
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




## PyVC API
in progress


## To Do
package this into PyPI