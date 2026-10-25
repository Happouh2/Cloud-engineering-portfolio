| Segment | Subnet | Router address | Notes |
|---|---|---|---|
| LAN A (clients) | 10.10.1.0/24 | 10.10.1.1 | clients get 10.10.1.50-100 by DHCP |
| LAN B (server) | 10.10.2.0/24 | 10.10.2.1 | server fixed at 10.10.2.10 |
| WAN link | 10.10.0.0/30 | 10.10.0.2 (router) / 10.10.0.1 (host) | router reaches the internet through the host |
