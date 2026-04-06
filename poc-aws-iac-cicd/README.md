# AI-Accelerated AWS IaC + CI/CD

> **AI-Assisted DevOps POC**: Demonstrates how AI accelerates Terraform generation, CI/CD pipeline setup, and monitoring for a production-ready API on AWS.

## Overview

This project provisions a minimal REST API on AWS using:
- **Terraform** for infrastructure (VPC, EC2, S3, RDS, IAM)
- **GitHub Actions** for CI/CD (lint, plan, apply, deploy)
- **Prometheus + Grafana** for monitoring
- **AI-assisted** generation of initial IaC, pipeline configs, and monitoring rules

## Architecture

```
┌─────────────────────────────────────────────────┐
│                     AWS                         │
│  ┌─────────┐    ┌──────────┐    ┌────────────┐ │
│  │   VPC   │───▶│  EC2     │───▶│   RDS      │ │
│  │         │    │ (API)    │    │ (Postgres) │ │
│  └─────────┘    └──────────┘    └────────────┘ │
│       │              │                           │
│       ▼              ▼                           │
│  ┌─────────┐    ┌──────────┐                    │
│  │   S3    │    │  CloudWatch│                   │
│  │ (Logs)  │    │ + Prom    │                   │
│  └─────────┘    └──────────┘                    │
└─────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- AWS CLI configured with credentials
- Terraform >= 1.5
- Python 3.10+ (for the API)

### Deploy Infrastructure
```bash
cd infra/terraform
terraform init
terraform plan -var-file="dev.tfvars"
terraform apply -var-file="dev.tfvars"
```

### Run API Locally
```bash
cd app/api
pip install -r requirements.txt
python main.py
curl http://localhost:5000/health
```

## AI-Assisted Components

| Component | AI Role | Human Refinement |
|-----------|---------|------------------|
| Terraform modules | Generated initial resource blocks | Hardened security groups, added lifecycle rules |
| CI/CD pipeline | Scaffolded workflow YAML | Added approval gates, environment variables |
| Monitoring rules | Generated PromQL queries | Tuned thresholds, added SLO definitions |
| IAM policies | Drafted least-privilege policies | Scoped resource ARNs, added conditions |

See [AI-usage.md](./AI-usage.md) for detailed breakdown.

## Project Structure
```
├── infra/terraform/       # AWS infrastructure as code
│   ├── main.tf           # Root module
│   ├── variables.tf      # Input variables
│   ├── outputs.tf        # Output values
│   └── modules/          # Reusable modules
├── app/api/              # Minimal Flask API
├── monitoring/           # Prometheus rules + Grafana dashboards
├── .github/workflows/    # CI/CD pipeline
└── scripts/              # Utility scripts
```

## License

MIT
