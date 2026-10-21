# Cloud & Security Engineering Portfolio

Hands-on cloud, security and DevOps projects by Henry Appouh (PMP). Each project is built, broken on purpose, fixed, documented, evidenced with screenshots, and torn down.

**Focus:** AWS, Terraform, CI/CD, Kubernetes, security automation and cost-aware cloud engineering.

Projects are independent: read them in any order.

## Featured projects
Start here. These show the strongest evidence of building, breaking and fixing real systems.

| Project | What it demonstrates | Evidence |
|---|---|---|
| [Self-healing infrastructure](self-healing-infrastructure/) | CloudWatch alarm to SNS to Lambda remediation, proven with a real CPU spike, plus four real issues diagnosed | [screenshots](self-healing-infrastructure/screenshots/) |
| [Kubernetes platform engineering](kubernetes-platform-engineering/) | kind and EKS, autoscaling, network policy, IRSA | [screenshots](kubernetes-platform-engineering/screenshots/) |
| [IAM federation and governance](iam-federation-identity-governance/) | OIDC flow by hand, SAML, and joiner/mover/leaver automation | [screenshots](iam-federation-identity-governance/screenshots/) |

## All projects
Docs: R = README, A = architecture diagram, S = screenshots, T = troubleshooting log, B = break/fix write-up, E = explain-it page. Tick only what really exists.

| Project | Stack | Status | R | A | S | T | B | E |
|---|---|---|---|---|---|---|---|---|
| [Linux hardening](linux-hardening/) | Amazon Linux, SSH, firewalld | Done | x | | | | | |
| [Terraform VPC + web server](terraform-basics/) | Terraform, AWS | Done | x | | | | | |
| [Python security audit](python-security-audit/) | boto3 | Done | | | | | | |
| [DevSecOps CI/CD](devsecops-cicd/) | GitHub Actions, tfsec, Bandit | Done | | | | | | |
| [Vulnerability management pipeline](vulnerability-management-pipeline/) | Nessus, ServiceNow, Python | Done | | | | | | |
| [Self-healing infrastructure](self-healing-infrastructure/) | CloudWatch, SNS, Lambda, ASG | Done | x | | | | | |
| [Splunk security dashboard](splunk-security-dashboard/) | Splunk, HEC, SPL | Done | x | | | | | |
| [Kubernetes platform engineering](kubernetes-platform-engineering/) | kind, EKS, IRSA | Done | x | | | | | |
| [IAM federation and governance](iam-federation-identity-governance/) | Keycloak, OIDC, SAML, SCIM | Done | x | | | | | |

## Screenshot gallery
Add one headline image per featured project here once the files exist (a broken image link looks worse than none):

<!--
![Alarm transitions to ALARM](self-healing-infrastructure/screenshots/05-alarm-in-alarm.png)
![Pod assumes a scoped IAM role](kubernetes-platform-engineering/screenshots/09-pod-irsa-identity.png)
![Decoded ID token claims](iam-federation-identity-governance/screenshots/05-jwt-claims.png)
-->

## How every project is documented
1. Overview and architecture diagram
2. Proof it works: named screenshots with identifiers removed (in each project's `screenshots/` folder)
3. Break/fix scenarios: failures introduced on purpose, with the diagnosis steps
4. Why I configured it this way (decisions and rejected alternatives)
5. Troubleshooting log with exact error text
6. Reproduce it, cost and cleanup, security notes

## Security hygiene
- No credentials in the repo. `.env`, `*.tfvars` and state files are ignored, and `.env.example` shows names only.
- Lab shortcuts are labelled in each README with the production fix.

## Contact
GitHub: [happouh2](https://github.com/happouh2)
