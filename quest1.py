from netmiko import ConnectHandler
from time import sleep


def interface_flap(device_handler):
    output = device_handler.send_command("show running-config interface fa1/0")

    configcmds = ["interface fastEthernet 1/0", "shutdown", "desc test interface"]
    device_handler.send_config_set(configcmds)
    print("fastEthernet 1/0 down")

    sleep(5)

    configcmds = ["interface fastEthernet 1/0", "no shutdown", "desc test interface"]
    device_handler.send_config_set(configcmds)
    print("fastEthernet 1/0 up")

    output = device_handler.send_command("show running-config interface fastEthernet1/0")

def print_all_interfaces(device_handler):
    print("\n=====Interfaces on "+device_handler.send_command("sh run | i hostname").split(" ")[1])
    for line in device_handler.send_command("show interfaces summary | i Ethernet").split("\n"):
        print (  " ".join(line.split(" ")[:3]))
    for line in device_handler.send_command("show interfaces summary | i Loopback").split("\n"):
        print (  " ".join(line.split(" ")[:3]))
    print("\n")

def print_device_info(device_handler):
    print("\n=====Info of "+device_handler.send_command("sh run | i hostname").split(" ")[1])
    print("hostname : "+device_handler.send_command("sh run | i hostname").split(" ")[1])
    print (device_handler.send_command("show version | i Version").split("\n")[0])
    print(device_handler.send_command("show version | i uptime") + "\n")

if __name__ == '__main__':

    device1 = ConnectHandler(device_type='cisco_ios', ip='192.168.200.11', username='cisco', password='cisco', secret='cisco')
    print ("connected to the device"+" 192.168.200.11")
    device2 = ConnectHandler(device_type='cisco_ios', ip='192.168.200.12', username='cisco', password='cisco',secret='cisco')
    print("connected to the device" + " 192.168.200.12")
    device1.enable()
    device2.enable()

    #interface_flap(device)
    print_all_interfaces(device1)
    print_all_interfaces(device2)

    print_device_info(device1)
    print_device_info(device2)


    device1.disconnect()
    print ("all connections closed ")

'''
'''

