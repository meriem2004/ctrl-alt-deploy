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

```bash
ctrl-alt-deploy/
├── bin/                 # Node.js binary wrappers
│   └── deploy.js        # Main CLI entry point
├── src/                 # Core Python source code
│   ├── models/          # Pydantic data models for specs
│   ├── validators/      # Semantic & syntactic verification logic
│   ├── orchestrator.py  # Main deployment controller
│   └── cli.py           # Python CLI implementation
├── examples/            # Sample specification files
├── templates/           # Jinja2 templates for Terraform generation
├── test_app/            # Next.js example application for deployment testing
├── tests/               # Comprehensive test suite
├── requirements.txt     # Python dependencies
└── package.json         # Node.js CLI configuration
```

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.11+**
- **Node.js & npm** (for the CLI wrapper)
- **Terraform** (installed and in PATH)
- **AWS CLI** (configured with credentials)

### 1. Backend Setup (Python)
Install the required Python packages for the core logic.
```bash
# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup (CLI)
Link the Node.js binary to make the `deploy` command globally available.
```bash
# From the project root
npm link
```

---

## 🚀 Usage

### 1. Define your Specification
Create a `spec.yaml` or `spec.json` file. Example:

```yaml
spec_version: "1.0.0"

aws:
  region: "us-east-1"
  # Credentials can also be loaded from environment variables

infrastructure:
  scalability: "MED"      # LOW, MED, HIGH
  machine_size: "M"       # S, M, L, XL

application:
  repository_url: "https://github.com/your/repo.git"
  services:
    - name: "backend"
      type: "EC2"
      ports: [8080]
      scaling: { min: 1, max: 3 }
    
    - name: "database"
      type: "RDS"
      ports: [3306]
      image: "mysql:8.0"
```

### 2. Validate the Specification
Run the validator ensures your config is correct before touching any cloud resources.
```bash
deploy validate examples/sample-spec.yaml
```
*Checks performed: Syntax, data types, logic consistency, circular dependencies, port conflicts, security best practices.*

### 3. Deploy
Launch the deployment pipeline.
```bash
deploy run examples/sample-spec.yaml
```
*Step-by-step: Validates spec → Generates Terraform code → Initializes Terraform → Applies configuration → returns active resource endpoints.*

---

## 🧪 Testing & Quality Assurance

The project maintains a high standard of code quality with >80% coverage.

### Running Tests
You can run the full suite or specific segments using `pytest` or the helper script.

```bash
# Run all tests
python run_tests.py

# Run only unit tests (Mappers)
python run_tests.py --unit

# Run with coverage report
python run_tests.py --coverage
```

### Test Categories
- **Unit Tests (`tests/test_mappers.py`)**: Verify that abstract sizes (S, M, L) correctly map to AWS instance types (e.g., `t3.medium`).
- **Integration Tests (`tests/test_terraform_generator.py`)**: Ensure Terraform files are valid and correctly generated from specs.
- **End-to-End Tests (`tests/test_end_to_end.py`)**: Simulate the full `validate` -> `generate` pipeline to ensure system integrity.

---

## 🛠 Features

- **Multi-Format Support**: Works native with JSON and YAML.
- **Smart Abstractions**: Uses T-shirt sizing (S, M, L, XL) for infrastructure, automatically mapping to the best cost/performance AWS instances.
- **Security First**: Enforces secure defaults (no open ports 0.0.0.0/0 unless specified, encrypted storage).
- **Dependency Management**: Handles service start order based on `depends_on` fields.
- **Extensible**: Designed to support ECS, Lambda, and other providers in the future.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---
*Generated by Antigravity*