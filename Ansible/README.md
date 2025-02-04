# Ansible Commands and Playbooks

This repository contains various **Ansible playbooks** and **commands** for automating server management and configurations.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Common Commands](#common-commands)
- [Usage Examples](#usage-examples)
- [Playbooks](#playbooks)
- [Troubleshooting](#troubleshooting)


## Requirements
- **Ansible**: You need Ansible installed on your local machine or control node.
  - To install Ansible:
    ```bash
    sudo apt update
    sudo add-apt-repository --yes --update ppa:ansible/ansible
    sudo apt install ansible
    ```
  - For other OS or package managers, refer to the [Ansible installation guide](https://docs.ansible.com/ansible/latest/installation_guide/index.html).

- **Python**: Ensure Python is installed on the target machines.
  - Python 2.x or 3.x can be used.

- **SSH Access**: Make sure SSH access is enabled between the control machine and the target machines.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ansible-commands.git
   cd ansible-commands
   ```
# Configure your hosts file
The default hosts file is located in the `inventory/` folder. You can customize it with your server IPs or hostnames.

## Common Commands

### Check Ansible Version
To check if Ansible is installed and view its version, run:

```bash
ansible --version
```

## Ping all hosts 
```bash
ansible all --key-file ~/.ssh/ansible -i inventory  -m ping 
```

## MISC Commands

- `ssh-keygen -t ed25119 -C "comment" `

- `ssh-copy-id -i ~/.ssh/ssh-comment.pub <ip to send>`

- create ansible.cfg set the defaults 
```bash
[defaults]
inventory = inventory
private_key_file = ~/.ssh/file 
```

- This lets us shorten the command to 
```bash
ansible all -m ping
```

- list all the hosts in inventory 
```bash
ansible all --list-hosts
ansible all -m gather_facts
ansible all -m gather_facts --limit <host eg. server1> #specific hosts to troubleshooting 
```

- To shorten the terminal directory path
```bash
nano ~/.bashrc 
replace 'w' in PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ ' with W
save and exit 
source ~/.bashrc
```

- Ansible commands 

```bash
$ ansible all -m apt -a update_cache=true --become --ask-become-pass # --become --> escalate privilege (sudo)

#Tell ansible to use sudo (become)
$ ansible all -m apt -a update_cache=true --become --ask-become-pass

#Install a package via the apt module
$ ansible all -m apt -a name=vim-nox --become --ask-become-pass

#Install a package via the apt module, and also make sure it’s the latest version available
$ ansible all -m apt -a "name=snapd state=latest" --become --ask-become-pass

#Upgrade all the package updates that are available
$ ansible all -m apt -a upgrade=dist --become --ask-become-pass

#search apt package 
$ apt search <package_name>

#run .yml file 
$ ansible-playbook --ask-become-pass <filename.yml> 

# 


