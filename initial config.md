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


### Cumulus

```

net add interface eth0 ip address <id addr>/24

net add interface eth0 ip gatewat 10.210.0.1

net pending 

net commit

net add hostname

net pending

net commit 

ssh-key gen 

net show interface all 

```

### Cisco NS-OS

```

config t 

hostname {{hostname}}

interface mgmt0

vrf member management 

ip address {{mgmt-ip}}

vrf context management 

ip route 0.0.0.0/0 10.210.0.1

Not Required SSH and telnet 

```

### Cisco IOS 

```

R1(config)# vrf definition Mgmt-intf 

R1(config-vrf)# address-family ipv4

R1(config-vrf-af)# ip route vrf Mgmt-intf 0.0.0.0 0.0.0.0 10.210.0.1 

R1(config)# int gi0/0

R1(config-if)# vrf forwarding Mgmt-intf

R1(config-if)# ip address 10.210.1.5 255.255.240.0

R1(config)# 

```

### Cisco IOS-XR

```
hostname <hostname>

telnet vrf default ipv4 server max-servers 10

username admin

group root-lr

group cisco-support 

secret <password>

interface MgmtEth0/RP0/CPU0/0

ipv4 address 10.210.1.85 255.255.240.0

no shut 

router static address-family ipv4 unicast 0.0.0.0/0 10.210.0.1

```

### Cisco (ASR) IOS-XR 

```
hostname <hostname>

#admin 

# config 
#username admin 
group root-system 
group cisco-support 
secret 0 <secret>

interface MgmtEth0/RP0/CPU0/0
ipv4 address 10.210.1.85 255.255.240.0 
no shut 

router statci address-family ipv4 unicast 0.0.0.0/0 10.210.0.1

ssh server v2

```

### Bypass Ixia 

```
IXIA Config:

IBPDUO[admin@IXIA](config)# system hostname <hostname>

IBPDUO[admin@IXIA](config)# user admin password <password>

IBPDUO[admin@IXIA](config)# device interface eth0 address 10.210.1.94 netmask 255.255.240.0 gateway 10.210.0.1

IBPDUO[admin@IXIA](config-device-interface-eth0)# description <121/1/4> 

```



