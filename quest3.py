from netmiko import ConnectHandler
from time import sleep
import random


def push_conf(device_handler, config):
    configcmds = config.split("\n")
    device_handler.send_config_set(configcmds)
    print ("pushed config >>"+str(configcmds)+" to :"+device_handler.send_command("sh run | i hostname").split(" ")[1])

def connect_to_device(ip,uname,pwd,secret):
    device_handler = ConnectHandler(device_type='cisco_ios', ip=ip, username=uname, password=pwd, secret=secret)
    device_handler.enable()
    temp = device_handler.send_command("terminal pager 0")
    print ("connected to the IP: "+ip+" | name: "+device_handler.send_command("sh run | i hostname").split(" ")[1])
    return device_handler

def get_interfaces_down(device_handler):
    print("\n=====Interfaces DOWN on " + device_handler.send_command("sh run | i hostname").split(" ")[1])
    orignal_arr = device_handler.send_command("show interfaces summary | i Ethernet").split("\n")
    for line in device_handler.send_command("show interfaces summary | i Loopback").split("\n"):
        orignal_arr.append(line)
    #print (orignal_arr)
    output_arr = []
    # print (orignal_arr)
    for line in orignal_arr:
        #print(str(line))
        if line == " " or line == "":
            continue
        elif line.split(" ")[0] != "*":
            output_arr.append(line.split(" ")[2])
            #print (line.split(" ")
    if len(output_arr) == 0:
        print ("all interfaces are UP")
        return output_arr
    else :
        print ("\n".join(output_arr)+"\n")
        return output_arr

def get_interfaces_up(device_handler):
    print("\n=====Interfaces UP on " + device_handler.send_command("sh run | i hostname").split(" ")[1])
    orignal_arr = device_handler.send_command("show interfaces summary | i Ethernet").split("\n")
    for line in device_handler.send_command("show interfaces summary | i Loopback").split("\n"):
        orignal_arr.append(line)
    #print (orignal_arr)
    output_arr = []
    for line in orignal_arr:
        if line == " " or line == "":
            continue
        elif line.split(" ")[0] == "*":
            output_arr.append(line.split(" ")[1])
            #print (line.split(" "))
    if len(output_arr) == 0:
        print ("all interfaces are DOWN")
        return output_arr
    else :
        print ("\n".join(output_arr)+"\n")
        return output_arr

def make_interface_up(device_handler,int_name):
    config = """interface """+int_name+"""
no shutdown"""
    push_conf(device_handler, config)
    print ("moved interface "+int_name+" to UP ")

def write_to_file(fname,text):
    fi = open(fname,'a')
    fi.write(text+"\n")
    fi.close()

def clear_file(fname):
    fi = open(fname,'w')
    fi.write(" ")
    fi.close()

def get_interface_info(device_handler,int_name):
    temp = device_handler.send_command("terminal pager 0")
    output = device_handler.send_command("show interface "+int_name)
    #print(output.split("\n"))
    output_arr = []
    if output.split("\n")[0] == "": # sometimes the first line is returned as null and causing errors
        n=1
    else :
        n=0
    name = output.split("\n")[n].split(" ")[0]
    if output.split("\n")[n+2].split(" ")[5] == "BW":
        ip = "<no ip configured>"
    else :
        # print(output.split("\n"))
        ip = output.split("\n")[n+2].split(" ")[5]
    status = output.split("\n")[n].split(" ")[2]
    proto = output.split("\n")[n].split(" ")[6]
    #print (name +" "+ip +" "+ status +" "+ proto)
    output_arr.append("interface:"+name +" IP:"+ip +" status:"+ status +" protocol:"+ proto)
    return output_arr

def get_ecmp_routes(device_handler):
    print("\n=====ECMP routes on " + device_handler.send_command("sh run | i hostname").split(" ")[1])
    sleep(1)
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

    clear_file('interfaces.txt')
    connected_devices = []

    connected_devices.append(connect_to_device("192.168.200.11",'cisco','cisco','cisco'))
    connected_devices.append(connect_to_device("192.168.200.12",'cisco','cisco','cisco'))
    # connected_devices.append(connect_to_device("192.168.200.13",'cisco','cisco','cisco'))
    # connected_devices.append(connect_to_device("192.168.200.14",'cisco','cisco','cisco'))

    #part1
    for dev in connected_devices:
        int_down_list = get_interfaces_down(dev)
        if len(int_down_list) != 0:
            ch = random.choice(int_down_list)
            make_interface_up(dev,ch)
            int_down_list.pop(int_down_list.index(ch))
            ch = random.choice(int_down_list)
            make_interface_up(dev, ch)
        sleep(1)

    #part2
    for dev in connected_devices:
        int_down_list = get_interfaces_up(dev)
        write_to_file('interfaces.txt', "\ndevice : "+dev.send_command("sh run | i hostname").split(" ")[1])
        for interf in int_down_list:
            write_to_file('interfaces.txt',"".join(get_interface_info(dev,interf)))
    print ("\ninterface details written to interfaces.txt file\n")

    # part3 :
    for dev in connected_devices:
        get_ecmp_routes(dev)

    #write_to_file('interfaces.txt',str(int_down_list) )

    for dev in connected_devices:
        dev.disconnect()
    print ("\nall connections closed ")


"""
int fa3/0
shutdown
int fa4/0
shutdown
int fa5/0
shutdown
int fa6/0
shutdown

do sh ip inter br
"""



