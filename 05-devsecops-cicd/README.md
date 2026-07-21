# 05 -- DevSecOps CI/CD Pipeline

## What this does
On every push, GitHub Actions automatically:
1. Scans Terraform with tfsec for security misconfigurations
2. Scans Python with Bandit for common code security issues

Both run in parallel, on disposable VMs, entirely free on a
public repo.

## Why it matters
Catching a misconfigured security group at commit time costs
minutes. Catching the same misconfiguration in production, after
an incident, costs a great deal more.

## Proof it works
This pipeline caught a deliberately introduced open-SSH rule
during testing -- see the commit history for the intentional
"break" and the follow-up revert, both flagged and confirmed
by the same tfsec check that runs on every push.

## Reproduce it
Fork the repo, push any change to infra/ or scripts/, check
the Actions tab.

