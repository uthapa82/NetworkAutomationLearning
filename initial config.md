## Initial Configs 

### ARISTA 
```
# conf t
# username admin privilege 15 role network-admin secret sha512 
# username cvpadmin privilege 15 role network-admin secret sha512 
# vrf definition management 
 rd 0:1

# management api http-commands
    vrf management
    no shutdown

interface Management1
    vrf forwarding management
    ip address 10.210.1.17/20

ip routing vrf management 
ip routing vrf management 0.0.0.0/0 10.210.0.1

```

* [arista](https://www.arista.com/en.um-eos/eos-section-2-1-initial-switch-access#ww1128630)

### CISCO IOS-XE

<font size='18'>

```
device # conf t 
device(config) # username admin secret *secret*
device(config) # hostname {{hostname}}
device(config) # ip route vrf Mgmt-intf 0.0.0.0 0.0.0.0 10.210.0.1
device(config) # ip domain-name gnetest.com
device(config) # crypto key generate rsa 
device(config) # line vty 0 4 
device(config) # login local 

```
</font>

### Juniper 

