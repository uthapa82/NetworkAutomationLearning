from jnpr.junos import Device

connection = Device(host='sampleFirewall.dmz.home', user='automation', password='juniper123')

connection.open()
show_version = connection.rpc.get_software_information({'format': 'json'})
connection.close()

print(show_version)