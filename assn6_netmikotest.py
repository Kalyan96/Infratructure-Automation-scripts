from netmiko import ConnectHandler, SCPConn
import sys

if __name__ == "__main__":
    print("sending to " + str(sys.argv[1]))
    params = ConnectHandler(device_type='linux', ip=str(sys.argv[1]), username="iadt", password="iadt")
    ssh_conn = ConnectHandler(**params)
    scp_conn = SCPConn(ssh_conn)
    print("connected tp remote host")
    s_file = 'index.html'
    d_file = '/home/iadt/playbooks/copied_index.html'
    scp_conn.scp_transfer_file(s_file, d_file)
    print("transferred the file")
    scp_conn.close()