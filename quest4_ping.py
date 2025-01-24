from napalm import get_network_driver
import json

fname_ping = "ping.txt"

driver = get_network_driver('ios')
device = driver('192.168.200.11', 'cisco', 'cisco',optional_args={'secret': "cisco"})
device.open()
# print(device.get_facts())
# print(device.get_arp_table() )

#ping output extract
fil = open(fname_ping,"w")
ip = "20.0.1.1"
out_dict = device.ping(ip)
fil.write ("ping to "+ip+"\n")
avg = str(out_dict['success']['rtt_avg'])
max = str(out_dict['success']['rtt_max'])
min = str(out_dict['success']['rtt_min'])
fil.write ("average RTT = "+avg+", max RTT = "+max+", min RTT = "+min)
fil.close()
print ("PING output written to ping.txt file")



