# Ctrl-Alt-Deploy

## Overview

Ctrl-Alt-Deploy automates AWS deployments from a single spec file. It validates configuration, generates Terraform, and provisions infrastructure (EC2, RDS, VPC, networking). The project targets a one-command experience while keeping the internal architecture modular and testable.

## Goals

- Reduce manual Terraform and AWS setup for small teams and startups
- Enforce consistent, validated deployment specs
- Speed up time-to-deploy with a repeatable workflow
- Keep infrastructure modeling extensible for new services

## High-Level Workflow

1. Parse and validate the spec (syntax and semantics)
2. Map abstract sizes and scalability into AWS resource types
3. Generate Terraform files with Jinja2 templates
4. Run Terraform to plan and apply
5. Surface outputs (instance IDs, public DNS/IP, RDS endpoints)

## Architecture (5 Layers)

1. Input and Validation
   - Pydantic models for structure
   - Semantic validation (service types, ports, dependencies)
2. Infrastructure Mapping
   - Maps S/M/L/XL to instance types
   - Maps LOW/MED/HIGH to scaling policies
3. Core Orchestration
   - Sequencing validation, build, generate, deploy
   - Logging and error handling
4. Infrastructure Automation
   - Terraform CLI execution and output parsing
   - Environment and state handling
5. CLI Interface
   - User-facing commands: validate, run, destroy
   - Progress reporting and summaries

## Specification Format

Supported formats: JSON and YAML.

Minimal example:

```json
{
  "aws": {
    "access_key": "YOUR_AWS_ACCESS_KEY",
    "secret_key": "YOUR_AWS_SECRET_KEY",
    "region": "us-east-1"
  },
  "infrastructure": {
    "scalability": "LOW",
    "machine_size": "S",
    "vpc_id": null,
    "key_pair": null,
    "dns_enabled": true
  },
  "application": {
    "repository_url": "https://github.com/user/app.git",
    "services": [
      {
        "name": "frontend",
        "image": "myorg/frontend:latest",
        "ports": [3000],
        "environment": { "NODE_ENV": "production" },
        "type": "EC2"
      }
    ]
  }
}
```

### Service Types

- EC2: compute services running Docker images
- RDS: managed database services
- ECS: container services (reserved for future expansion)

### Validation Rules (examples)

- Ports must be 1-65535 and non-conflicting
- Service names must be unique
- RDS services cannot define EC2-only scaling
- Dependencies must reference existing services

## Scalability Model

The spec can define global scalability (LOW, MED, HIGH) and optional per-service overrides. The mapper controls how many instances are created. For LOW, a single EC2 instance is used and no ASG/ALB is created.

## Outputs

Terraform outputs include:

- Instance IDs for EC2 services
- Public IP/DNS for EC2 services (requires VPC DNS hostnames)
- VPC, subnet IDs, and RDS endpoints where applicable

## Project Structure

```
ctrl-alt-deploy/
  src/
    models/                # Pydantic models
    validators/            # Parser and semantic checks
    infrastructure/
      mappers/             # Instance and RDS mapping logic
      templates/           # Jinja2 Terraform templates
      generators/          # Terraform file generation
  examples/                # Sample specs
  tests/                   # Test suite
  generate_tf.py           # CLI entry point for generation
```

## Setup

Prerequisites:
- Python 3.11+
- Terraform CLI

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Validate a spec:

```bash
python -m src.cli validate spec.json
```

Generate Terraform:

```bash
python generate_tf.py spec.json
```

Deploy with Terraform:

```bash
cd terraform_output
terraform init
terraform apply
```

## Troubleshooting

- If public DNS is empty, ensure VPC DNS hostnames are enabled (`dns_enabled: true` for new VPCs).
- If a service is not reachable, confirm the correct port is open in the generated security group.
- Use `terraform output` to verify the instance IP/DNS after apply.

## Security Notes

Never commit real AWS keys. Use environment variables or a secrets manager. Rotate any leaked keys immediately.

## Roadmap

- IDE integration for spec editing and deployment
- Multi-cloud support (Azure/GCP)
- CI/CD integration
- Cost optimization recommendations
