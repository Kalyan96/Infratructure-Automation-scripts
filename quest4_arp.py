from napalm import get_network_driver
import json

fname_arp = "arp.txt"

driver = get_network_driver('ios')
device = driver('192.168.200.11', 'cisco', 'cisco',optional_args={'secret': "cisco"})
device.open()
# print(device.get_facts())
# print(device.get_arp_table() )

#ARP output extract
fil = open(fname_arp,"w")
fil.write ("    IP     |      MAC      | AGE\n")
for element in device.get_arp_table():
    fil.write (element['ip']+"  "+element['mac']+"  "+str(element['age']) +"\n")
fil.close()
print ("ARP output written to arp.txt file")

