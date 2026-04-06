# Airflow Data Pipeline with IaC

> **AI-Assisted DevOps POC**: Demonstrates AI-accelerated data pipeline development with Airflow, Terraform, and CI/CD.

## Overview

This project builds an end-to-end analytics pipeline:
- **Airflow DAGs** for CSV ingestion, transformation, and S3 upload
- **Terraform** for Airflow infrastructure (EC2/ECS, S3, IAM)
- **CI/CD** for DAG linting, testing, and deployment

## Architecture

```
┌──────────┐    ┌──────────────┐    ┌──────────┐
│  CSV     │───▶│  Airflow     │───▶│   S3     │
│  Input   │    │  DAG         │    │  Output  │
└──────────┘    │  (Transform) │    └──────────┘
                └──────────────┘
                      │
                      ▼
                ┌──────────────┐
                │  Monitoring  │
                │  + Alerts    │
                └──────────────┘
```

## Quick Start

### Deploy Infrastructure
```bash
cd infra/terraform
terraform init
terraform apply -var-file="dev.tfvars"
```

### Run DAG Locally
```bash
# Install dependencies
pip install apache-airflow pandas boto3

# Test DAG
cd dags
python csv_to_s3_dag.py

# Run with Airflow
airflow dags test csv_to_s3 $(date +%Y-%m-%d)
```

### CI/CD Pipeline
```bash
# Lint DAGs
flake8 dags/

# Run tests
pytest tests/

# Deploy to Airflow server
./ci/deploy.sh
```

## AI-Assisted Components

| Component | AI Role | Human Refinement |
|-----------|---------|------------------|
| DAG boilerplate | Generated task structure | Added error handling, retries, SLAs |
| IAM policies | Drafted S3/EC2 policies | Scoped to specific buckets, added conditions |
| Terraform modules | Generated resource blocks | Added VPC networking, security hardening |
| Test scaffolds | Created test templates | Added integration tests, mock data |

See [AI-usage.md](./AI-usage.md) for detailed breakdown.

## License

MIT
