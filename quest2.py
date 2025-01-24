from netmiko import ConnectHandler
from time import sleep

def configure_from_file(device_handler, filename):
    fi = open(filename,'r')
    configcmds = fi.readlines()
    fi.close()
    device_handler.send_config_set(configcmds)
    print ("pushed config >>"+str(configcmds)+" to :"+device_handler.send_command("sh run | i hostname").split(" ")[1])

def print_all_interfaces(device_handler):
    print("\n=====Interfaces on "+device_handler.send_command("sh run | i hostname").split(" ")[1])
    print (device_handler.send_command("show interfaces summary | i Ethernet")+"\n")

if __name__ == '__main__':

    device1 = ConnectHandler(device_type='cisco_ios', ip='192.168.200.11', username='cisco', password='cisco', secret='cisco')
    device1.enable()
    temp = device1.send_command("terminal pager 0")
    print ("connected to the IP: "+" 192.168.200.11 | name: "+device1.send_command("sh run | i hostname").split(" ")[1])

    device2 = ConnectHandler(device_type='cisco_ios', ip='192.168.200.12', username='cisco', password='cisco', secret='cisco')
    device2.enable()
    temp = device2.send_command("terminal pager 0")
    print("connected to the IP: " + " 192.168.200.12 | name: " + device2.send_command("sh run | i hostname").split(" ")[1])

    configure_from_file(device1,'R1_ospf_config.txt')
    configure_from_file(device2,'R2_ospf_config.txt')

    device1.disconnect()
    device2.disconnect()
    print ("all connections closed ")

'''
'''

