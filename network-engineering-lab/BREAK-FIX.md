# Break-fix log

## Ticket 1: "I cannot reach web.lab.internal" (user on LAN A)

**Symptom:** ping web.lab.internal fails with "Temporary failure in name resolution".

**Checks, in order:**
1. Name: dig web.lab.internal got "connection refused" from 10.10.1.1 port 53.
2. Route: ip route get 10.10.2.10 showed the path through the router, 10.10.1.1.
3. Reach: ping 10.10.2.10 worked, so the server and the route were fine.
4. DNS server: ss -ulnp on the router showed nothing listening on port 53.

**Root cause:** the DNS service (dnsmasq) on the router had stopped.

**Fix:** restarted dnsmasq on the router. The first restart failed with "cannot open log: Permission denied" because the old log file in /tmp belonged to the dnsmasq user. Removed the old log, restarted, and confirmed from the client side: dig returned 10.10.2.10 and ping by name worked.

**Lesson:** "connection refused" means the machine is up but nothing is listening on that port. A firewall drop would time out instead.

**Prevention:** run DNS as a monitored service that restarts on failure and alerts someone, and always confirm a restart actually worked.
