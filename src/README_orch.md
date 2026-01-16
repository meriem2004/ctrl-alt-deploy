# Orchestrator Module

The core Python logic for parsing, validating, and orchestrating deployments, wrapped in a Node.js CLI.

## Structure
- `cli.py`: Python entry point, called by the Node.js wrapper.
- `orchestrator.py`: Main controller logic.
- `validators/`: Parser and semantic validation rules.
- `models/`: Pydantic data models.
- `../bin/deploy.js`: Node.js wrapper script exposing the `deploy` command.

## ⚙️ Setup

### 1. Python Environment (Backend)
The CLI relies on Python. Ensure dependencies are installed:

```bash
# From project root
pip install -r requirements.txt
```

### 2. CLI Installation (Frontend)
Link the binary globally using npm to enable the `deploy` command:

```bash
# From project root
npm link
```

## 🚀 Usage

Once linked, you can use the `deploy` command directly from your terminal.

### 1. Validate a Specification
Check if a spec file is syntactically and semantically valid.

```bash
deploy validate examples/sample-spec.yaml
```

### 2. Run Deployment
Execute the full deployment pipeline.

```bash
deploy run examples/sample-spec.yaml
```

### Debugging
If the `deploy` command fails, you can run the Python script directly for debugging:
```bash
python src/cli.py validate examples/sample-spec.yaml
```

## 🧪 Testing

Run the parser test suite to verify validation logic:

```bash
python test_parser.py
```
