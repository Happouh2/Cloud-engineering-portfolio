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

## Ticket 2: "The website won't load and I get Network is unreachable" (user on LAN A)

**Symptom:** ping says "Network is unreachable" and curl fails instantly (web: 000).

**Checks, in order:**
1. Name: dig web.lab.internal returned 10.10.2.10, so DNS was fine.
2. Route: ip route get 10.10.2.10 said "Network is unreachable", and ip route showed only 10.10.1.0/24, with no default route.

**Root cause:** the laptop's default route was missing, so it had no way to reach anything outside its own network.

**Fix:** renewed the DHCP lease with udhcpc. The lease brought back "default via 10.10.1.1", and the website returned 200.

**Lesson:** DNS can still work when the route is broken, as long as the DNS server is on the same network. Check each layer in order.

**Prevention:** hand out gateways by DHCP rather than typing them in, and check the gateway whenever a static address is set.

## Ticket 3: "The website loads forever, then fails" (user on LAN A)

**Symptom:** curl hangs and times out (web: 000).

**Checks, in order:**
1. Name: dig returned 10.10.2.10.
2. Route: ip route get showed the path via 10.10.1.1.
3. Reach: skipped ping, because ping is blocked on purpose.
4. Port: nc to port 80 timed out, which points at a firewall.
5. Proof: captured both sides of the router at the same time. The LAN A side showed the same SYN 5 times, the LAN B side showed nothing, and the drop counter went up to 8.

**Root cause:** the firewall rule allowing LAN A to reach the web server on ports 80 and 443 had been removed.

**Fix:** reloaded the saved rule book (scripts/router-firewall.nft). The website returned 200.

**Lesson:** a timeout points at a firewall, but a capture on both sides plus the rule counter proves it.

**Prevention:** keep firewall rules in version-controlled files and compare them before and after every change.

## Ticket 4: "The server can reach the laptop. It shouldn't be able to." (security review)

**Symptom:** a ping from the server (LAN B) to the laptop succeeded, with 0% packet loss.

**Checks, in order:**
1. Listed the rules with their handle numbers (nft -a list chain ip lab forward).
2. Found an "accept everything from r1-b" rule at the top of the chain, with its counter going up. It had been added twice by accident (handles 10 and 11).

**Root cause:** the firewall stops at the first rule that matches, so the lazy rule at the top let LAN B through before the careful rules were ever checked.

**Fix:** deleted both bad rules by their handle numbers. The ping from the server failed again with 100% packet loss, as it should.

**Lesson:** rule order matters as much as the rules themselves.

**Prevention:** review firewall changes before they go live, and never put a broad allow rule above specific ones.
