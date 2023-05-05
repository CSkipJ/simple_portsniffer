import argparse
import socket
import time
import random
import sys


def is_port_open(target_ip, port) -> bool:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(1)
    result = client.connect_ex((target_ip, port))
    client.close()
    return result == 0


def get_range(_port_range):
    if '-' in _port_range:
        return map(int, _port_range.split('-'))
    else:
        return (int(_port_range), int(_port_range))


def get_ports(_port_range) -> list:
    ranges = _port_range.split(',')

    _ports_list = []
    for rng in ranges:
        _start_port, _end_port = get_range(rng)
        for port in range(_start_port, _end_port+1):
            _ports_list.append({'port':port, 'is_open':None})
    return _ports_list


def sequential_scan(args):
    for port in get_ports(args.port_range):
        if is_port_open(args.target_ip, port['port']):
            port['is_open'] = 'open'
            print(f"Port {port['port']} is {port['is_open']}")
        elif args.all:
            port['is_open'] = 'closed'
            print(f"Port {port['port']} is {port['is_open']}")
        time.sleep(random.uniform(0.01, float(args.delay)))


def random_scan(args):
    ports = get_ports(args.port_range)
    rports = ports.copy()
    random.shuffle(rports)

    for port in rports:
        if is_port_open(args.target_ip, port['port']):
            port['is_open'] = 'open'
            print(f"Port {port['port']} is {port['is_open']}")
        elif args.all:
            port['is_open'] = 'closed'
            print(f"Port {port['port']} is {port['is_open']}")
        time.sleep(random.uniform(0.01, float(args.delay)))


def main(args):
    if not args.randomize:
        sequential_scan(args)
    else:
        random_scan(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port scanner")
    parser.add_argument("target_ip", type=str, help="IP address to scan")
    parser.add_argument("port_range", type=str, help="Port range to scan (e.g. 1-65535). Also accepts a single port.")
    parser.add_argument("-o", "--out_file", type=str, help="The destination file for scanned port information.")
    parser.add_argument("-r", "--randomize", action='store_true', help="Will randomize the order in which ports are scanned.")
    parser.add_argument("-d", "--delay", default=0.01, help="Turns on randomized delay, where the max possible delay value is the value given.")
    parser.add_argument("-a", "--all", action='store_true', help="Prints every port scanned. If not used only open ports will be printed.")

    args = parser.parse_args()

    if args.out_file:
        with open(args.out_file, 'w') as sys.stdout:
            main(args)
    else:
        main(args)
