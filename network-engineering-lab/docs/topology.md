```mermaid
flowchart LR
  A["lan-a client<br>DHCP"] --- R{{"r1 router<br>DHCP DNS NAT firewall"}}
  B["lan-b server<br>10.10.2.10"] --- R
  R --- H["host / internet"]
```
