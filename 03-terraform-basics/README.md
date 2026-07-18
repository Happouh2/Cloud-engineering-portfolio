# 03 -- Terraform VPC + Web Server

## What this builds
A VPC with a public subnet, internet gateway, route table,
security group, and an EC2 instance running nginx -- entirely
from Terraform, with SSH locked to a single IP and HTTP/HTTPS open.

## Files
- main.tf -- the infrastructure
- variables.tf -- configurable inputs (instance type, allowed SSH
  CIDRs, an existing EC2 key pair name)
- outputs.tf -- what Terraform reports back after apply

## Reproduce it
terraform init
terraform apply \
  -var='allowed_ssh_cidrs=["YOUR_IP/32"]' \
  -var='instance_type=t3.micro' \
  -var='key_pair_name=YOUR_KEY_PAIR_NAME'

## What I learned
Two real bugs showed up building this that a plan/apply preview
alone didn't catch: a hardcoded AMI ID had gone stale and silently
pointed at Amazon Linux 2 instead of 2023, which broke the dnf-based
setup script with zero Terraform error -- fixed by looking the AMI
up dynamically with a data "aws_ami" block instead of hardcoding an
ID. Separately, the security group only opened port 443 while nginx
served plain HTTP on port 80 with no certificate configured, which
produced a silent connection timeout rather than a clear error,
since AWS security groups drop disallowed traffic instead of
rejecting it. Debugging both meant reading the EC2 console output
directly (aws ec2 get-console-output) since the instance had no
SSH key pair attached to log in and check directly -- fixed by
adding a key_name to the instance going forward.
