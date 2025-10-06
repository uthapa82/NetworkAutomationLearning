from telnetlib import Telnet
tn = Telnet("192.168.1.100")
tn.write('cisco\n')
tn.write('term length 0\n')
tn.write('show ver\n')
tn.write('exit\n')
print(tn.read_all())