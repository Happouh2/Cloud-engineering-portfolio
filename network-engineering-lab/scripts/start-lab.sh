#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
sudo scripts/teardown.sh 2>/dev/null || true
sudo scripts/build-lab.sh
sudo bash scripts/start-dns.sh
sleep 1
sudo ip netns exec lan-a busybox udhcpc -i veth-a -n -q -s "$(pwd)/scripts/lease.sh"
sudo ip netns exec r1 nft flush ruleset
sudo ip netns exec r1 nft -f scripts/router-firewall.nft
sudo ip netns exec lan-b setsid -f python3 -m http.server 80 --bind 10.10.2.10 > /tmp/web-b.log 2>&1
sleep 1
echo "Lab is up."
