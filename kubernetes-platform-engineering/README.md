# 09 -- Kubernetes Platform Engineering

## What this does
Deploys a containerized version of Project 04's security audit
script to Kubernetes -- first locally via kind, with autoscaling
and a documented network policy, then to a real AWS EKS cluster
with IRSA so the pod reaches AWS using a scoped IAM role instead
of static keys.

## Stack
Docker, Kubernetes (kind + EKS), kubectl, Helm, Terraform, AWS IAM/OIDC, ECR

## Files
- app/Dockerfile -- containerizes Project 04's script
- manifests/ -- Deployment, Service, NetworkPolicy, ServiceAccount
- terraform/ -- EKS cluster, node group, OIDC provider, IRSA role

## What ran where
| Concept | Local (kind, free) | Cloud (EKS, billed) |
|---|---|---|
| Deployment / Service | Yes | Yes |
| HPA | Yes -- watched replicas scale 2 -> 5 under real load | Not re-tested |
| NetworkPolicy | Written, not enforced (kindnet) | Would be enforced (AWS VPC CNI) |
| IRSA | N/A | Yes -- verified get_caller_identity() returned the scoped role |

## Real issues hit building this
- Default VPC subnets spanned an availability zone (us-east-1e)
  EKS doesn't support for its control plane -- fixed by filtering
  subnets to only EKS-supported AZs.
- EKS can't pull images from a local Docker daemon the way kind
  can -- had to push the image to ECR before pods would start.

