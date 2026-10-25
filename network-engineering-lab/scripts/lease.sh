#!/bin/sh
case "$1" in
  bound|renew)
    ip addr flush dev "$interface"
    ip addr add "$ip/$mask" dev "$interface"
    [ -n "$router" ] && ip route replace default via "${router%% *}" dev "$interface"
    [ -n "$dns" ] && echo "nameserver ${dns%% *}" > /etc/resolv.conf
    ;;
esac
