#!/usr/bin/env bash
# scripts/build-lab.sh -- run with sudo
set -euo pipefail
UPLINK=$(ip route show default | awk '{print $5}' | head -1)
# three pretend machines: a client, a server, and the router
for ns in lan-a lan-b r1; do ip netns add "$ns"; ip -n "$ns" link set lo up; done
# virtual cables (each has two ends)
ip link add veth-a type veth peer name r1-a
ip link add veth-b type veth peer name r1-b
ip link add veth-w type veth peer name r1-w
ip link set veth-a netns lan-a; ip link set r1-a netns r1
ip link set veth-b netns lan-b; ip link set r1-b netns r1
ip link set r1-w netns r1
# addresses
ip -n r1 addr add 10.10.1.1/24 dev r1-a
ip -n r1 addr add 10.10.2.1/24 dev r1-b
ip -n r1 addr add 10.10.0.2/30 dev r1-w
ip -n lan-b addr add 10.10.2.10/24 dev veth-b
ip addr add 10.10.0.1/30 dev veth-w

# plug everything in
for d in r1-a r1-b r1-w; do ip -n r1 link set "$d" up; done
ip -n lan-a link set veth-a up
ip -n lan-b link set veth-b up
ip link set veth-w up
# routes, and let the router pass traffic between streets
ip -n r1 route add default via 10.10.0.1
ip -n lan-b route add default via 10.10.2.1
ip netns exec r1 sysctl -qw net.ipv4.ip_forward=1
sysctl -qw net.ipv4.ip_forward=1
# let the router's traffic out to the internet through the VM
nft add table ip labhost
nft add chain ip labhost post '{ type nat hook postrouting priority 100; }'
nft add rule ip labhost post ip saddr 10.10.0.0/30 oifname "$UPLINK" masquerade
# each pretend machine gets its own DNS settings file
mkdir -p /etc/netns/lan-a /etc/netns/lan-b
echo "nameserver 10.10.1.1" > /etc/netns/lan-a/resolv.conf
echo "nameserver 10.10.2.1" > /etc/netns/lan-b/resolv.conf
echo "lab built; uplink=$UPLINK"
