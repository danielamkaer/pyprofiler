import pickle
import sys
import re
import os
import binascii

ipv4re = re.compile('^(\d+)\.(\d+)\.(\d+)\.(\d+)$')

def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def fatal(*args, **kwargs):
    error("FATAL:", *args, **kwargs)
    sys.exit(1)

try:
    filename = sys.argv[1]
    ipaddress = sys.argv[2]
except IndexError:
    fatal(f"Please specify filename and ip address.\n\n{sys.argv[0]} <filename> <ip>\n")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    fatal(f"File {filename} not found.\n")

try:
    devices = data["devices"]
except KeyError:
    fatal(f"Empty file supplied.\n")

profile = None

for device in devices:
    if device["host"] == ipaddress:
        profile = device
        break
else:
    fatal(f"Device with {ipaddress} not found.\n")

print("#!/bin/bash")
print(f"# Generated profile for device {ipaddress} - Hostname: {device['name']}")
print(f"ipt=/usr/sbin/iptables")
print(f"ips=/usr/sbin/ipset")
print()
print(f"$ipt -N IN_{ipaddress} # creates a new chain for incoming traffic")
print(f"$ipt -A FORWARD -d {ipaddress} -j IN_{ipaddress} # filter for incoming traffic")
print(f"$ipt -A IN_{ipaddress} -m state --state ESTABLISHED,RELATED -j ACCEPT # accept established connections")
print(f"$ipt -A IN_{ipaddress} -p icmp -j ACCEPT # accept incoming ICMP")
print()

for server in profile["servers"]:
    print(f"$ipt -A IN_{ipaddress} -p {server['proto']} --dport {server['port']} -j ACCEPT # allow traffic on {server['proto']}/{server['port']}")
    print()
        
print(f"$ipt -A IN_{ipaddress} -j DROP # drop unmatched traffic")

print()
print()


print(f"$ipt -N OUT_{ipaddress} # creates a new chain for outgoing traffic")
print(f"$ipt -A FORWARD -s {ipaddress} -j OUT_{ipaddress} # filter for outgoing traffic")
print(f"$ipt -A OUT_{ipaddress} -m state --state ESTABLISHED,RELATED -j ACCEPT # accept established connections")
for client in profile["clients"]:
    if ipv4re.match(client['dest']):
        print(f"$ipt -A OUT_{ipaddress} -d {client['dest']} -p {client['proto']} --dport {client['port']} -j ACCEPT # allow traffic to {client['dest']}:{client['proto']}/{client['port']}")
    else:
        setname = "set_" + binascii.b2a_hex(os.urandom(4)).decode()
        print(f"$ips create {setname} hash:ip # create ipset, where dnsmasq will add resolved ips for host name")
        print(f'echo "ipset=/{client["dest"][:-1]}/{setname}" >> /etc/dnsmasq.d/{ipaddress}.conf')
        print(f"$ipt -A OUT_{ipaddress} -m set --match-set {setname} dst -p {client['proto']} --dport {client['port']} -j ACCEPT # allow traffic to {client['dest']}:{client['proto']}/{client['port']}")
    print()

print(f"$ipt -A OUT_{ipaddress} -j DROP # drop unmatched traffic")
