import argparse
import socket
import time
import random

def scan_port(target_ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(1)

    retval = f'Port {port} is '
    try:
        client.connect((target_ip, port))
        retval += 'open'
    except socket.error:
        retval += 'closed'
    finally:
        client.close()
        return retval

def arrange_ports(args):
    target_ip = args.target_ip
    port_range = args.port_range
    out_file = args.out_file
    randomize = args.randomize
    max_delay = float(args.delay)

    if '-' in port_range:
        start_port, end_port = map(int, port_range.split('-'))
    else:
        start_port = int(port_range)
        end_port = int(port_range)

    if not out_file:
        for port in range(start_port, end_port+1):
            print(scan_port(target_ip, port))
            if max_delay:
                time.sleep(random.uniform(0.1, max_delay))
    else: 
        with open(out_file, 'w') as f:
            for port in range(start_port, end_port+1):
                f.write(scan_port(target_ip, port))
                if max_delay:
                    time.sleep(random.uniform(0.1, max_delay))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port scanner")
    parser.add_argument("target_ip", type=str, help="IP address to scan")
    parser.add_argument("port_range", type=str, help="Port range to scan (e.g. 1-65535). Also accepts a single port.")
    parser.add_argument("-o", "--out_file", type=str, help="The destination file for scanned port information.")
    parser.add_argument("-r", "--randomize", action='store_true', help="Will randomize the order in which ports are scanned. Not implemented.")
    parser.add_argument("-d", "--delay", help="Turns on randomized delay, where the max possible delay value is the value given.")

    args = parser.parse_args()

    arrange_ports(args)
