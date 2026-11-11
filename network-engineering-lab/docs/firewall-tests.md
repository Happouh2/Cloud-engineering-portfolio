## Before the firewall

Test: from lan-a, nc -zv -w 3 10.10.2.10 22
Result: Connection refused, instantly. Nothing listens on port 22.

## After the firewall

| Test | Expected | Result |
| --- | --- | --- |
| Laptop opens the website | 200 | web: 200 |
| Laptop to server SSH (22) | Times out (blocked) | timed out |
| Laptop to the internet | 200 through NAT | internet: 200 |
| Server pings the laptop | Blocked | 100% packet loss |
| Laptop pings the server | Blocked (not web traffic) | 100% packet loss |
Timeout means a firewall dropped it. Refused means the port is closed.
