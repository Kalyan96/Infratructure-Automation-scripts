from netmiko import ConnectHandler
from time import sleep

'''
- show cmds :
output = device_handler.send_command("show running-config interface fa1/0")

- configure commands :
configcmds = ["interface fastEthernet 1/0", "desc test interface"]
device_handler.send_config_set(configcmds)

'''

r3_conf = """interface fa2/0
ip address 20.0.1.1 255.255.255.0
ip ospf 1 area 1
no shutdown

interface fa1/0
ip address 20.0.4.2 255.255.255.0
ip ospf 1 area 4
no shutdown

int lo1
ip address 3.3.3.3 255.255.255.255
ip ospf 1 area 0

router ospf 1
router-id 3.3.3.3"""

def push_conf(device_handler, config):
    configcmds = config.split("\n")
    device_handler.send_config_set(configcmds)
    print ("pushed config >>"+str(configcmds)+" to :"+device_handler.send_command("sh run | i hostname").split(" ")[1])

def print_all_interfaces(device_handler):
    print("\n=====Interfaces on "+device_handler.send_command("sh run | i hostname").split(" ")[1])
    print (device_handler.send_command("show interfaces summary | i Ethernet")+"\n")

if __name__ == '__main__':

    # device1 = ConnectHandler(device_type='cisco_ios', ip='192.168.200.11', username='cisco', password='cisco', secret='cisco')
    # device1.enable()
    # print ("connected to the IP: "+" 192.168.200.11 | name: "+device1.send_command("sh run | i hostname").split(" ")[1])
    #
    # device2 = ConnectHandler(device_type='cisco_ios', ip='192.168.200.12', username='cisco', password='cisco', secret='cisco')
    # device2.enable()
    # print("connected to the IP: " + " 192.168.200.12 | name: " + device2.send_command("sh run | i hostname").split(" ")[1])

    device3 = ConnectHandler(device_type='cisco_ios', ip='192.168.200.13', username='cisco', password='cisco', secret='cisco')
    device3.enable()
    print("connected to the IP: " + " 192.168.200.13 | name: " + device3.send_command("sh run | i hostname").split(" ")[1])

    # device4 = ConnectHandler(device_type='cisco_ios', ip='192.168.200.14', username='cisco', password='cisco', secret='cisco')
    # device4.enable()
    # print("connected to the IP: " + " 192.168.200.14 | name: " + device4.send_command("sh run | i hostname").split(" ")[1])

    #interface_flap(device)
    # print_all_interfaces(device1)
    # print_all_interfaces(device2)
    # print_all_interfaces(device3)
    # print_all_interfaces(device4)

    push_conf(device3,r3_conf)

    device3.disconnect()
    print ("all connections closed ")

'''
'''

