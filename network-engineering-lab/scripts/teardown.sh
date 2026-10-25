#!/usr/bin/env bash
# scripts/teardown.sh -- run with sudo
pkill dnsmasq 2>/dev/null || true
pkill -f "http.server 80" 2>/dev/null || true
for ns in lan-a lan-b r1; do ip netns del "$ns" 2>/dev/null || true; done
ip link del veth-w 2>/dev/null || true
nft delete table ip labhost 2>/dev/null || true
rm -rf /etc/netns/lan-a /etc/netns/lan-b /var/lib/misc/lab-r1.leases
echo "lab removed"
