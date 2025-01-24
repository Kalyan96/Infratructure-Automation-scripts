from netmiko import ConnectHandler
from time import sleep
import random


'''
- show cmds :
output = device_handler.send_command("show running-config interface fa1/0")

- configure commands :
configcmds = ["interface fastEthernet 1/0", "desc test interface"]
device_handler.send_config_set(configcmds)

'''

def flap_ospf(device_handler):
    conf = """router ospf 1
shutdown
no shutdown"""
    push_conf(device_handler,conf)

def push_conf(device_handler, config):
    configcmds = config.split("\n")
    device_handler.send_config_set(configcmds)
    print ("pushed config >>"+str(configcmds)+" to :"+device_handler.send_command("sh run | i hostname").split(" ")[1])

def connect_to_device(ip,uname,pwd,secret):
    device_handler = ConnectHandler(device_type='cisco_ios', ip=ip, username=uname, password=pwd, secret=secret)
    device_handler.enable()
    print ("connected to the IP: "+ip+" | name: "+device_handler.send_command("sh run | i hostname").split(" ")[1])
    return device_handler

#def save_config_name(device_handler, save_name):
def get_interfaces_down(device_handler):
    print("\n=====Interfaces DOWN on " + device_handler.send_command("sh run | i hostname").split(" ")[1])
    orignal_arr = device_handler.send_command("show interfaces summary | i Ethernet").split("\n")
    for line in device_handler.send_command("show interfaces summary | i Loopback").split("\n"):
        orignal_arr.append(line)
    #print (orignal_arr)
    output_arr = []
    for line in orignal_arr:
        if line.split(" ")[0] != "*":
            output_arr.append(line.split(" ")[2])
            #print (line.split(" "))

    print ("\n".join(output_arr))
    return output_arr

def make_interface_up(device_handler,int_name):
    config = """interface """+int_name+"""
no shutdown"""
    push_conf(device_handler, config)
    print ("moved interface "+int_name+" to UP ")

def save_config_nvram(device_handler):
    device_handler.fast_cli = False
    device_handler.send_command("write memory\n\n\n\n\n")
    device_handler.fast_cli = True
    print ("config saved for : "+device_handler.send_command("sh run | i hostname").split(" ")[1]+ " | ")

def get_ecmp_routes(device_handler):
    output = device_handler.send_command("show ip route ").split("\n")
    route_lines = []
    ecmp_lines = []
    for line in output:
        if line.find("connected") != -1 or line.find("via") != -1:
            route_lines.append(line)
    i=0
    for line in route_lines:
        if line[0] == " ":
            ecmp_lines.append(route_lines[i-1])
            ecmp_lines.append(line)
        i+=1
   # print ("routes are :"+"\n".join(route_lines))
    if len(ecmp_lines) != 0:
        print ("the ECMP routes are as follows :\n"+"\n".join(ecmp_lines))
    else :
        print ("there are no ECMP routes")

if __name__ == '__main__':

    connected_devices = []

    connected_devices.append(connect_to_device("192.168.200.11",'cisco','cisco','cisco'))
    # connected_devices.append(connect_to_device("192.168.200.12",'cisco','cisco','cisco'))
    # connected_devices.append(connect_to_device("192.168.200.13",'cisco','cisco','cisco'))
    # connected_devices.append(connect_to_device("192.168.200.14",'cisco','cisco','cisco'))

    # for dev in connected_devices:
    #     int_down_list = get_interfaces_down(dev)
    #     make_interface_up(dev,random.choice(int_down_list))

    # for dev in connected_devices:
    #     save_config_nvram(dev)

    for dev in connected_devices:
        get_ecmp_routes(dev)

    for dev in connected_devices:
        dev.disconnect()
    print ("\nall connections closed ")
