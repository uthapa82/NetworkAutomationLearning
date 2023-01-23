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

### Juniper 

```
FreeBSD/amd64(Amnesiac)(ttyu0)

login: root

root@:~# cli
root> configure
Entering configuration mode

[edit]
root# 
set system host-name rt73gnelab14115AQ-P2
set system root-authentication plain-text-password
New password:
Retype new password:

set system login user admin uid 2000
set system login user admin class super-user
set system login user admin authentication plain-text-password
New password: 


set system services ssh root-login allow
set system syslog user * any emergency
set system syslog file messages any notice 

set system syslog file messages authoriation info
set system syslog file interactive-commands interactive-commands any


set interfaces fxp0 unit 0 family inet address 10.210.1.244/20
set routing-options static route 0.0.0.0/0 next-hop 10.210.0.1

# commit

command to check the display of the configs 

root@hostname# show | display set 

Can only ping when in User EXEC mode 

show configuration system login | display set 

# banner motd # Bannner ,...\n#
# show chassi hardware 
#delete <statement> <id>

```

