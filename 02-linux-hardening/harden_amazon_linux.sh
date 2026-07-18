#!/bin/bash
# harden_amazon_linux.sh
# Hardens a fresh Amazon Linux 2023 EC2 instance against the CIS Level 1 Benchmark
set -e

# Patch everything
sudo dnf update -y
# Reboot manually after this to apply kernel updates, then reconnect before continuing

# Create a named, non-root admin user
sudo adduser cloudadmin
sudo usermod -aG wheel cloudadmin

# Harden SSH
sudo tee -a /etc/ssh/sshd_config > /dev/null << 'SSHEOF'
PermitRootLogin no
PasswordAuthentication no
X11Forwarding no
MaxAuthTries 4
SSHEOF
sudo systemctl restart sshd

# Configure the firewall (not pre-installed on Amazon Linux 2023 -- install it first)
sudo dnf install -y firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
