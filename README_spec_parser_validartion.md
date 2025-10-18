# 🚀 **Deployment Specification Parser & Validator**

## **Overview**

This project provides a robust **deployment specification parser and validator** for AWS cloud infrastructure. It validates YAML/JSON configuration files that describe complete multi-service applications, ensuring they are syntactically correct, logically consistent, and secure before deployment.

The system performs comprehensive validation including:
- **Syntactic validation** (structure, types, required fields)
- **Semantic validation** (business logic, dependencies, security)
- **Circular dependency detection**
- **AWS configuration validation**
- **Security best practices checking**

## **🎯 Current Status**

This is the **parsing and validation layer** of a larger deployment automation system. It ensures deployment specifications are valid before they proceed to infrastructure provisioning.

## **📋 Features**

### **Validation Capabilities**
- ✅ **YAML/JSON Support**: Parse both YAML and JSON specification files
- ✅ **Syntactic Validation**: Pydantic-based structure and type validation
- ✅ **Semantic Validation**: Business logic and consistency checks
- ✅ **Dependency Analysis**: Detect circular dependencies between services
- ✅ **AWS Configuration**: Validate regions, credentials, and service configurations
- ✅ **Security Checks**: Identify potential security issues and best practices
- ✅ **Port Conflict Detection**: Prevent services from using conflicting ports
- ✅ **Service Type Validation**: Ensure EC2, RDS, ECS configurations are logical

### **User Experience**
- 🎨 **Rich Console Output**: Beautiful tables and colored formatting
- 📊 **Detailed Error Messages**: Clear explanations of validation failures
- ⚠️ **Security Warnings**: Proactive security issue identification
- ✓ **Progress Indicators**: Visual feedback during validation process

---

## **🛠️ Installation & Setup**

### **Prerequisites**
- Python 3.11+ (tested with Python 3.11.0)
- pip (Python package manager)

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd ctrl-alt-deploy
```

### **2. Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Verify Installation**
```bash
python test_parser.py
```

You should see all 3 tests pass:
- ✅ TEST 1: Valid Specification
- ✅ TEST 2: Invalid Specification  
- ✅ TEST 3: Circular Dependency Detection

---

## **🧪 Testing**

### **Run All Tests**
```bash
python test_parser.py
```

### **Test Descriptions**

#### **Test 1: Valid Specification**
- Parses `examples/sample-spec.yaml`
- Validates correct YAML structure and content
- Displays formatted service summary with tables
- **Expected**: ✅ All validations pass

#### **Test 2: Invalid Specification** 
- Tests error handling with intentionally invalid data:
  - AWS keys too short (< 16 characters)
  - Invalid scalability value ("INVALID")
  - Port number out of range (99999)
- **Expected**: ❌ Validation fails with detailed error messages

#### **Test 3: Circular Dependency Detection**
- Creates services with circular dependencies (A → B → C → A)
- Tests dependency graph analysis
- **Expected**: ❌ Circular dependency detected and reported

### **Manual Testing**

You can also test individual specifications:

```python
from src.validators.parser import parse_deployment_spec

# Test your own specification
try:
    spec = parse_deployment_spec("your-spec.yaml")
    print("✅ Specification is valid!")
except Exception as e:
    print(f"❌ Validation failed: {e}")
```

---

## **📁 Project Structure**

```
ctrl-alt-deploy/
├── src/
│   ├── models/
│   │   ├── __init__.py          # Model exports
│   │   └── models.py            # Pydantic data models
│   ├── validators/
│   │   ├── __init__.py          # Validator exports  
│   │   ├── parser.py            # Main parser orchestrator
│   │   └── semantic_validator.py # Business logic validation
│   └── utils/
│       └── __init__.py          # Utility functions (future)
├── examples/
│   └── sample-spec.yaml         # Example deployment specification
├── test_parser.py               # Comprehensive test suite
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

---

## **📝 Specification Format**

### **Basic Structure**
```yaml
spec_version: "1.0.0"

aws:
  access_key: "YOUR_AWS_ACCESS_KEY"
  secret_key: "YOUR_AWS_SECRET_KEY" 
  region: "us-east-1"

infrastructure:
  scalability: "MED"        # LOW, MED, HIGH
  machine_size: "M"         # S, M, L, XL
  key_pair: "my-ssh-key"
  dns_enabled: false

application:
  repository_url: "https://github.com/user/repo.git"
  services:
    - name: "backend"
      dockerfile_path: "./backend/Dockerfile"
      ports: [8080]
      type: "EC2"           # EC2, RDS, ECS
      depends_on: ["database"]
      scaling:
        min: 1
        max: 3
      environment:
        DB_HOST: "database"
        API_KEY: "secret123"
    
    - name: "database"
      image: "mysql:8.0"
      ports: [3306]
      type: "RDS"
      environment:
        MYSQL_ROOT_PASSWORD: "password123"
        MYSQL_DATABASE: "myapp"
```

### **Supported Service Types**
- **EC2**: Virtual machines for application services
- **RDS**: Managed database services  
- **ECS**: Container orchestration services

### **Validation Rules**
- AWS access keys must be 16+ characters
- Ports must be in range 1-65535
- Service names must be unique
- Dependencies must reference existing services
- No circular dependencies allowed
- RDS services cannot have scaling configuration

---

## **🔧 Dependencies**

This project uses the following key dependencies:

- **pydantic** (2.12.3): Data validation and parsing
- **PyYAML** (6.0.3): YAML file parsing
- **rich** (14.2.0): Beautiful console output and formatting
- **typer** (0.19.2): CLI framework (for future CLI implementation)

See `requirements.txt` for complete dependency list with versions.

---

## **🚀 Future Roadmap**

This parser is designed to integrate with:

1. **Terraform Generator**: Convert validated specs to Terraform configurations
2. **Docker Builder**: Automated Docker image building and pushing  
3. **AWS Provisioner**: Infrastructure deployment and management
4. **CLI Interface**: Command-line tool for easy deployment
5. **Web Dashboard**: Visual deployment management interface

---

## **🤝 Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python test_parser.py`
5. Commit changes: `git commit -m "Add feature"`
6. Push to branch: `git push origin feature-name`
7. Submit a pull request

---

## **📄 License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

## **🐛 Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
ModuleNotFoundError: No module named 'src'
```
**Solution**: Make sure you're running from the project root directory.

#### **Virtual Environment Issues**
```bash
# Deactivate and recreate virtual environment
deactivate
rm -rf venv  # or rmdir /s venv on Windows
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### **Test Failures**
If tests fail, check:
1. All dependencies are installed: `pip list`
2. Python version is 3.11+: `python --version`
3. You're in the correct directory: `ls` should show `test_parser.py`

### **Getting Help**

If you encounter issues:
1. Check the error message carefully
2. Verify your Python and pip versions
3. Ensure all dependencies are installed
4. Try running tests in a fresh virtual environment

---

**Happy Validating! 🎉**