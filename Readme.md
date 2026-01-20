# 🚀 Ctrl-Alt-Deploy

**Ctrl-Alt-Deploy** is a powerful cloud deployment automation platform that radically simplifies the process of deploying applications on AWS. By replacing thousands of lines of complex infrastructure code with a single, intuitive specification file, it democratizes cloud access for developers and organizations.

---

## 🎯 Project Overview

### The Problem
Traditional cloud deployment requires deep expertise in tools like Terraform, Docker, AWS SDKs, and networking. This creates a bottleneck where developers depend on OPS/DevOps teams for every deployment, slowing down time-to-market and increasing the risk of configuration errors.

### The Solution
**Ctrl-Alt-Deploy** introduces a layer of abstraction that handles the complexity for you.
- **Simplicity**: Define your entire infrastructure in one readable `spec.json` or `spec.yaml` file.
- **Speed**: Deploy full-stack applications with a single command.
- **Reliability**: Built-in validation ensures configurations are logical and secure before any resource is created.
- **Standardization**: Enforce best practices automatically across all deployments.

### Use Cases
- **Startups**: Launch products rapidly without hiring a dedicated DevOps engineer.
- **Dev Teams**: Focus on application code while the platform handles the infrastructure.
- **Training**: valid environments for learning cloud concepts without the configuration headache.

---

## 🏗️ Technical Architecture

This project utilizes a robust 5-layer architecture to transform high-level specifications into running AWS infrastructure.

### Technology Stack
| Layer | Technologies | Role |
|-------|-------------|------|
| **Interface** | Node.js, Typer/Click | User CLI experience |
| **Orchestration** | Python | Control logic & sequencing |
| **Validation** | Pydantic, JSONSchema | Syntax & Semantic checks |
| **Generation** | Terraform, Jinja2 | Dynamic IaC generation |
| **Automation** | Terraform CLI, AWS SDK | Infrastructure provisioning |

### Architecture Layers
```mermaid
graph TD
    L5[5. User Interaction Layer (CLI)] -->|deploy run spec.json| L4
    L4[4. Infrastructure Automation Layer] -->|Terraform CLI, AWS SDK| L3
    L3[3. Core Control Logic] -->|Orchestrator| L2
    L2[2. Infrastructure Layer] -->|Jinja2 Templates| L1
    L1[1. Input & Validation Layer] -->|Pydantic Models| Cloud[AWS Cloud]
```

### Modeling Concepts
The system uses a sophisticated meta-modeling approach:
- **Level 2 (Meta-Meta-Models)**: Languages used to define the system (Python/Pydantic, HCL, JSONSchema).
- **Level 1 (Meta-Models)**: The schemas defining what an invalid spec looks like (Spec File Schema, Validation Rules).
- **Level 0 (Models)**: The actual data instances (Your `spec.json`, the generated `.tf` files, the active AWS resources).

---

## 📂 Project Structure

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
