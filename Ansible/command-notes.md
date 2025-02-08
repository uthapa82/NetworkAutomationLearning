## Command Notes

```bash
ssh-keygen -t ed25119 -C "comment" 
ssh-copy-id -i ~/.ssh/ssh-comment.pub <ip to send>

#tcpdump to see incoming icmp ping
tcpdump -i <interface> icmp and icmp[0] == 8 
- icmp[0] == 8 to filter icmp request, icmp echo request pkt have a type 8

#without installing thirdparty packages 
python -m venv <env-name> 
    - light weight 
    - only work with Python3.3+
    - Simpler, basic virtual env 
    - works consistently across platforms (windows, macOS, Linux)

#virtual env setup 
pip3 install virtualenv
virtualenv <name-of-env> eg. ansible-env 
    - Python 2.x and Python 3.x
    - Advanced features and customization options 
    - Feature-rich but can add some overhead 
    - works accorss platforms, but may have some differences depending on the version installed 


source name-of-env/bin/activate 

#create virtual env with specific python version 
virtualenv -p /usr/bin/python2.6 <env-name> 

#export all the requirement packages to a file 
pip freeze --local > requirements.txt

#check what persion of python pip is using 
pip --version 
which pip 
where pip (for windows)

#global environment 
deactivate 

#installing all the requirememts 
pip install -r requirements.txt


```


