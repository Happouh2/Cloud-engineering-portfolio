# 02 -- Amazon Linux 2023 Server Hardening

## Problem
Fresh cloud servers ship with convenience-first defaults: password
SSH auth allowed, root login allowed, no firewall rules applied.
This hardens a fresh instance against the CIS Level 1 Benchmark.

## Controls applied
- [x] All packages patched (dnf update)
- [x] Non-root admin user created via the wheel group
- [x] SSH: root login disabled, password auth disabled, MaxAuthTries 4
- [x] X11 forwarding disabled
- [x] firewalld installed, enabled, default deny, only ssh/http/https open

## Amazon Linux vs Ubuntu quick reference
| Task        | Ubuntu      | Amazon Linux 2023 |
|-------------|-------------|--------------------|
| Updates     | apt update  | dnf update         |
| Admin group | sudo        | wheel              |
| Firewall    | ufw         | firewalld (install separately) |
| Default user| ubuntu      | ec2-user           |

## Reproduce it
1. Launch a t2.micro/t3.micro Amazon Linux 2023 instance
2. ssh -i key.pem ec2-user@YOUR_IP
3. bash harden_amazon_linux.sh

## What I learned
firewalld isn't pre-installed on Amazon Linux 2023's minimal AMI --
had to add dnf install -y firewalld before any firewall-cmd command
would work. Also learned the hard way to always check my prompt
before running a command, after repeatedly running server commands
in my own local WSL shell by mistake.
