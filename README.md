# Cloud & Security Engineering Portfolio

Hands-on cloud, security and DevOps projects by Henry Appouh (PMP). Every project folder is self-contained: what it builds, how to reproduce it, what broke, and how it was torn down.

**Focus:** AWS (plus GCP/Azure foundations), Terraform, CI/CD security, detection and compliance automation, Kubernetes.

## Projects

Status values: `Done` (built, verified, torn down), `In progress`, `Planned`. Update the Status column only when the project's README is complete.

| # | Project | Stack | Status |
|---|---|---|---|
| 03 | [Terraform VPC + web server](03-terraform-basics/) | Terraform, AWS | Done |
| 04 | [Python security audit](04-python-security-audit/) | boto3 | Planned |
| 05 | [DevSecOps CI/CD](05-devsecops-cicd/) | GitHub Actions, tfsec, Bandit, Trivy | Planned |
| 06 | [Vulnerability management pipeline](06-vulnerability-management-pipeline/) | Nessus, ServiceNow, Python | Planned |
| 07 | [Self-healing infrastructure](07-self-healing-infrastructure/) | CloudWatch, SNS, Lambda, ASG | Planned |
| 08 | [Splunk security dashboard](08-splunk-security-dashboard/) | Splunk, HEC, SPL | Planned |
| 09 | [Kubernetes platform engineering](09-kubernetes-platform-engineering/) | kind, EKS, IRSA | Planned |
| 10 | [IAM federation and governance](10-iam-federation-identity-governance/) | Keycloak, OIDC, SAML, SCIM | Done |

Folders not listed here are not yet published.

## How every project is documented

1. What it does and why (one paragraph)
2. Architecture (diagram or short list)
3. Reproduce it (exact commands)
4. Proof it works (output, screenshots with identifiers redacted)
5. Troubleshooting (`troubleshooting.md`)
6. Lessons learned (`lessons-learned.md`)
7. Cost and cleanup (what costs money, how it was destroyed)
8. Security notes (known shortcuts and the production fix)

## Security hygiene

- No credentials in the repo. `.env`, `*.tfvars`, `*.tfstate*`, keys and tokens are ignored; `.env.example` files show variable names only.
- Secrets are scanned before pushing (see `.gitignore` notes and the leak-check commands in the Field Manual).
- Lab shortcuts (for example `verify=False` against local self-signed certs, open ports in throwaway labs) are labelled in each project README.

## Contact

GitHub: [happouh2](https://github.com/happouh2)
