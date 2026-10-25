#!/usr/bin/env bash
rm -f /tmp/dnsmasq-r1.log
ip netns exec r1 dnsmasq --conf-file=/etc/dnsmasq.d/lab-r1.conf --pid-file= --log-facility=/tmp/dnsmasq-r1.log
