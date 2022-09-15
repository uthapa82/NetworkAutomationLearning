#!usr/bin/env python

ip_addr1 = "192.168.16.1"
ip_addr2 = "10.10.1.1"
ip_addr3 = "172.16.31.17"

def ip_addr():   
    ip_addr = input("Please enter an IP address: ")

    octets = ip_addr.split(".")
    print()
    print("{:^15}{:^15}{:^15}{:^15}".format("Octet1", "Octet2", "Octet3", "Octet4"))
    print("-" * 60)
    print("{:^15}{:^15}{:^15}{:^15}".format(*octets))
    print(
        "{:^15}{:^15}{:^15}{:^15}".format(
            bin(int(octets[0])),
            bin(int(octets[1])),
            bin(int(octets[2])),
            bin(int(octets[3])),
        )
    )

    print(
        "{:^15}{:^15}{:^15}{:^15}".format(
            hex(int(octets[0])),
            hex(int(octets[1])),
            hex(int(octets[2])),
            hex(int(octets[3])),
        )
    )

    print("-" * 60)
    print()

def arp_table():
    mac_address = []
    ip_address = []
    
    mac_addr = [
        "Internet  10.220.88.29           94   5254.abbe.5b7b  ARPA   FastEthernet4", 
        "Internet  10.220.88.30            3   5254.ab71.e119  ARPA   FastEthernet4", 
        "Internet  10.220.88.32          231   5254.abc7.26aa  ARPA   FastEthernet4"
    ]

    for address in mac_addr:
        fields = address.split()
        ip_addr = fields[1]
        mac1 = fields[3]
        
        print("{:>20}{:>20}".format("IP ADDR", "MAC ADDRESS"))
        print("{:>20} {:>20}".format("-" * 20, "-" * 20))
        print("{:>20} {:>20}".format(str(ip_addr), str(mac1)))
        print()
        
def main():
    ip_addr()
    arp_table()
    
if __name__ == "__main__":
    main()
