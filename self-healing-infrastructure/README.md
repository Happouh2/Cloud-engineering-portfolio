# 07 -- Self-Healing Infrastructure

## What this does
A CloudWatch alarm watches average CPU across an Auto Scaling Group.
When it crosses 80%, it publishes to an SNS topic, which triggers a
Lambda function that scales the ASG up and logs a ServiceNow incident
documenting exactly what happened -- no human paged.

## Stack
AWS (EC2, Auto Scaling, CloudWatch, SNS, Lambda, IAM), Terraform,
ServiceNow Table API

## Proof it works
Forced a real CPU spike via `stress` on the running instance and
confirmed all three signals independently:
- CloudWatch alarm transitioned OK -> ALARM -> OK
- Lambda logs showed `Scaled self-healing-asg to desired capacity 2`
  and `ServiceNow response: 201`
- A real ServiceNow incident (INC0010004) was created automatically

## Real issues hit building this (and how they were fixed)
- **Wrong active AWS credentials**: `aws configure` from Project 04
  had silently overwritten the default profile with a read-only
  auditor identity, blocking every create action. Fixed by
  re-configuring the admin IAM user and keeping the auditor as a
  separate named profile going forward.
- **Free-tier instance type restriction**: `t2.micro` wasn't
  free-tier eligible on this account; `describe-instance-types
  --filters Name=free-tier-eligible,Values=true` found `t3.micro`
  as the actual eligible type.
- **No SSH access at all**: the launch template originally had no
  `key_name` or security group, so nothing could reach the instance.
  Added both, least-privilege (SSH from my IP only).
- **The alarm never fired even under real load**: `period = 120`
  assumed 1-2 minute metric granularity, but EC2's default "basic
  monitoring" only reports every 5 minutes. Fixed by matching the
  alarm's period to 300 seconds instead of paying for detailed
  monitoring.

